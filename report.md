# Observathon Evaluation Report - Nguyen Binh Huy - 2A202600689

This report summarizes the evaluation results for team **ichbinhhuy** on the Observathon benchmark.

## Private Test Results

The private test was executed on **80 requests** with the following metrics recorded in `score.json`:

| Metric | Score | Weight | Weighted Score |
| :--- | :---: | :---: | :---: |
| **Headline Score** | **87.57 / 100** | - | - |
| **Accuracy (`correct`)** | 0.5700 | 0.32 | 18.24 |
| **Quality (`quality`)** | 0.7345 | 0.16 | 11.75 |
| **Error Rate (`error`)** | 1.0000 | 0.13 | 13.00 |
| **Latency (`latency`)** | 0.7870 | 0.08 | 6.30 |
| **Cost (`cost`)** | 1.0000 | 0.09 | 9.00 |
| **Drift (`drift`)** | 0.6378 | 0.07 | 4.46 |
| **Prompt Efficacy (`prompt`)** | 0.7379 | 0.15 | 11.07 |
| **Diagnosis F1 (`diag_f1`)** | 0.6250 | +22 (max) | 13.75 |

- **Total Requests (`n`)**: 80
- **Correct Answers (`n_correct`)**: 45 / 80
- **Judge Mode**: Offline

---

## Public Test Results

The public test was executed on **120 requests** with the following metrics recorded:

| Metric | Score | Weight | Weighted Score |
| :--- | :---: | :---: | :---: |
| **Headline Score** | **100.00 / 100** | - | - |
| **Accuracy (`correct`)** | 0.9250 | 0.32 | 29.60 |
| **Quality (`quality`)** | 0.9490 | 0.16 | 15.18 |
| **Error Rate (`error`)** | 1.0000 | 0.13 | 13.00 |
| **Latency (`latency`)** | 0.6707 | 0.08 | 5.37 |
| **Cost (`cost`)** | 1.0000 | 0.09 | 9.00 |
| **Drift (`drift`)** | 0.6338 | 0.07 | 4.44 |
| **Prompt Efficacy (`prompt`)** | 0.9334 | 0.15 | 14.00 |
| **Diagnosis F1 (`diag_f1`)** | 0.6670 | +22 (max) | 14.67 |

- **Total Requests (`n`)**: 120
- **Correct Answers (`n_correct`)**: 111 / 120
- **Judge Mode**: Offline
