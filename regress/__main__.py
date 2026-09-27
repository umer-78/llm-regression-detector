"""python -m regress compare BASE CANDIDATE   report per-task changes; exit 1 if any task regressed
python -m regress bench                     every pair in versions.yaml, written to results/"""
import argparse
import json
import sys
from pathlib import Path

from . import data
from .compare import compare, report

RESULTS = Path(__file__).resolve().parent.parent / "results"


def run_pair(base, candidate):
    overall, results = compare(data.load(base), data.load(candidate))
    return overall, results, report(base, candidate, overall, results)


def main(argv=None):
    ap = argparse.ArgumentParser(prog="regress")
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("compare")
    c.add_argument("base")
    c.add_argument("candidate")
    sub.add_parser("bench")
    args = ap.parse_args(argv)
    if args.cmd == "compare":
        _, results, text = run_pair(args.base, args.candidate)
        print(text)
        return 1 if any(r.verdict == "regressed" for r in results) else 0
    RESULTS.mkdir(exist_ok=True)
    texts, summary = [], []
    for base, cand in data.config()["pairs"]:
        overall, results, text = run_pair(base, cand)
        texts.append(text)
        # overall's "base" and "candidate" are accuracies, so the model names get their own keys
        summary.append({"base_model": base, "candidate_model": cand, **overall,
                        "tasks": [{k: getattr(r, k) for k in ("task", "questions", "base", "candidate", "broke", "fixed", "p_adjusted", "verdict")}
                                  for r in results],
                        "regressed": [r.task for r in results if r.verdict == "regressed"],
                        "improved": [r.task for r in results if r.verdict == "improved"]})
    (RESULTS / "report.md").write_text("\n\n".join(texts) + "\n")
    (RESULTS / "summary.json").write_text(json.dumps(summary, indent=1))
    print("\n\n".join(texts))
    return 0


if __name__ == "__main__":
    sys.exit(main())
