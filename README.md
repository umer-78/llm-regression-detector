# LLM Regression Detector

[![CI](https://github.com/umer-78/llm-regression-detector/actions/workflows/ci.yml/badge.svg)](https://github.com/umer-78/llm-regression-detector/actions/workflows/ci.yml)

**Live demo:** https://umer-78.github.io/llm-regression-detector/ (pick an upgrade and see which tasks it broke)

Catches the tasks a model upgrade breaks before it ships. Every question is compared across the
old and new version (stayed right, broke, got fixed); per task, McNemar's exact test with Holm's
correction decides whether the breakage is more than chance, and CI fails if any task regressed
by 2+ points. Run on real model upgrades using [HELM Lite](https://crfm.stanford.edu/helm/lite/)'s
recorded answers (4,551 questions: GSM8K, MATH, MMLU, MedQA, OpenBookQA, LegalBench):

| Upgrade | Overall | Broke / fixed | Regressed | Improved |
|---|---|---|---|---|
| GPT-4o 2024-05-13 → 2024-08-06 | 77.3% → 77.5% | 157 / 164 | none | none |
| Gemini 1.5 Pro 001 → 002 | 77.8% → 78.6% | 263 / 302 | none | math, openbookqa |
| Gemini 1.5 Flash 001 → 002 | 70.8% → 62.6% | 688 / 314 | **gsm8k** | legalbench, math |
| Gemini 1.0 Pro 001 → 002 | 60.8% → 57.5% | 700 / 548 | **legalbench, mmlu, openbookqa** | gsm8k, math |
| Mistral Large 2402 → 2407 | 62.8% → 68.7% | 331 / 573 | **math** | gsm8k, mmlu, openbookqa |
| Llama 3 70B → 3.1 70B Instruct | 74.7% → 74.0% | 560 / 528 | **legalbench (69.2% → 58.3%)** | gsm8k, math |

The last row is the case this exists for: overall accuracy moved 0.7 points, and a whole task lost
11. Per-task tables and examples of broken answers: [`results/report.md`](results/report.md).

```bash
pip install -e '.[dev]'
pytest -q
python -m regress compare gpt-4o-2024-05-13 gpt-4o-2024-08-06   # exit 1 if any task regressed
python -m regress bench                                          # every pair in regress/versions.yaml
python -m regress.demo                                           # rebuild the live demo's data in docs/
```

Add a version to `regress/versions.yaml` to test it; the branch `demo/llama-upgrade` gates the
Llama upgrade and its CI fails. Answers here are HELM's recorded ones; a live runner is the next
step. MIT licence; HELM results keep their own licences and are downloaded, not redistributed.
