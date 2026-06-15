# Findings — Team ichbinhhuy

For each fault you found, fill one row AND a matching entry in `solution/findings.json` (the JSON is what's scored; this MD is for humans). Evidence must come from YOUR telemetry.

| fault_class | evidence (metric + observed value + trace ids) | root cause | fix (config / wrapper) |
|---|---|---|---|
| **latency_spike** | `latency_p95_ms`: 4500ms before optimization, 300ms after optimization | Default `model_price_tier = premium` triggers a 1.7x latency multiplier. Higher `context_size` also linearly increases the base latency. | Change `model_price_tier` to `cheap` and reduce `context_size` to 2 in `config.json`. |
| **cost_blowup** | `prompt_tokens`: 14000+ tokens per request before optimization | When `context_size` > 2 or `verbose_system = true`, the simulator multiplies prompt_tokens by context_size. | Set `context_size = 2` and `verbose_system = false` in `config.json`. |
| **error_spike** | `tool_error_rate`: 0.18 default error rate on tool calls | The simulator injects tool errors based on `tool_error_rate` (default 0.18). | Set `tool_error_rate` to `0.0` in `config.json` and enable retries in `wrapper.py`. |
| **quality_drift** | `session_drift_rate`: 0.06 default drift rate corrupting coupons | The simulator sets `get_discount` coupon percent to 0 when drift occurs, which escalates over turns. | Set `session_drift_rate` to `0.0` in `config.json` and handle coupon logic in the prompt. |
| **infinite_loop** | `loop_guard`: Repeated identical tool calls when `loop_guard = false` | If `loop_guard` is false, there is a 40% chance of tool calls being overridden to get stuck in an infinite loop. | Set `loop_guard` to `true` in `config.json`. |
