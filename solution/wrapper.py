"""YOUR mitigation + observability layer. The simulator calls mitigate() around the
opaque agent (a REAL LLM) for every request. This is the ONLY place observability can
live -- the agent is silent. Legal moves: retry / cache / route / guardrail / sanitize
/ fallback / session-reset / PROMPT ROUTING, plus your own logging/tracing/metrics.
Illegal: hardcoding answers, importing the agent internals, reading instructor files,
network exfiltration.

  call_next(question, config) -> result   # the only way to reach the black box
  context = {"session_id","turn_index","qid","cache": <shared dict>, "cache_lock": <Lock>}
  result  = {"answer","status","steps","trace","meta":{latency_ms,usage,...}}

PROMPT ROUTING: you can override the agent's system prompt PER REQUEST by setting it in
the config you pass to call_next, e.g.:
    conf = dict(config); conf["system_prompt"] = my_better_prompt
    result = call_next(question, conf)
(Or just edit solution/prompt.txt for a single static prompt used on every request.)
"""
from __future__ import annotations
import sys
import os

# Ensure the workspace directory is in sys.path
workspace_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(workspace_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
if workspace_dir not in sys.path:
    sys.path.insert(0, workspace_dir)

try:
    import time
    from solution.instrument import observed_call
    from telemetry.redact import redact
except Exception as e:
    print(f"IMPORT ERROR IN WRAPPER: {e}", file=sys.stderr)
    sys.stderr.flush()
    raise e







def get_ctx_val(ctx, key):
    if ctx is None:
        return None
    try:
        return ctx[key]
    except (TypeError, KeyError, IndexError):
        return getattr(ctx, key, None)

def mitigate(call_next, question, config, context):
    debug_file_path = os.path.join(parent_dir, "debug_wrapper.txt")
    
    try:
        # 1. Caching: check if the answer is already cached (thread-safe)
        cache_key = question.strip()
        cache = get_ctx_val(context, "cache")
        cache_lock = get_ctx_val(context, "cache_lock")
        qid = get_ctx_val(context, "qid")
        
        if cache is not None and cache_lock is not None:
            with cache_lock:
                if cache_key in cache:
                    cached_res = cache[cache_key]
                    from telemetry.logger import logger
                    if logger:
                        logger.log_event("CACHE_HIT", {"qid": qid, "question": question})
                    return cached_res

        # 2. Cấu hình retry & call agent qua observed_call (để ghi log telemetry)
        max_attempts = 3
        result = None
        
        for attempt in range(max_attempts):
            try:
                result = observed_call(call_next, question, config, context)
                if result and result.get("status") == "ok":
                    break
            except Exception as e:
                from telemetry.logger import logger
                if logger:
                    logger.log_event("AGENT_ERROR", {"qid": qid, "error": str(e), "attempt": attempt})
                if attempt == max_attempts - 1:
                    raise e
            time.sleep(0.1)

        if not result:
            result = {"answer": "Error occurred", "status": "wrapper_error", "steps": 0, "trace": [], "meta": {}}

        # 3. PII Redaction: lọc bỏ email, số điện thoại từ câu trả lời trước khi trả về
        ans = result.get("answer")
        if ans:
            redacted_ans, num_redactions = redact(ans)
            if num_redactions > 0:
                result["answer"] = redacted_ans
                from telemetry.logger import logger
                if logger:
                    logger.log_event("PII_REDACTED", {"qid": qid, "num_redactions": num_redactions})

        # 4. Cache successful responses
        if result.get("status") == "ok" and cache is not None and cache_lock is not None:
            with cache_lock:
                cache[cache_key] = result

        return result
    except Exception as e:
        import traceback
        with open(debug_file_path, "a", encoding="utf-8") as f:
            f.write(f"Error for question: {question}\n")
            traceback.print_exc(file=f)
            f.write("="*40 + "\n")
        raise e
