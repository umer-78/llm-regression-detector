"""Comparing two versions on the same questions.

Accuracy alone hides regressions: a new version can score the same overall while breaking
one task and fixing another. So every question is paired: it either stayed right, stayed
wrong, broke (right before, wrong now) or got fixed. Per task, McNemar's exact test asks
whether broken outnumbers fixed by more than chance; Holm's correction keeps the chance of
any false alarm across tasks under 5%. A task regresses when the drop is significant and at
least MIN_DROP points; that is what fails CI.
"""
import math
from dataclasses import dataclass, field

import numpy as np
from scipy.stats import binomtest

ALPHA = 0.05
MIN_DROP = 0.02    # below two points a drop is not worth blocking a release for, however significant


@dataclass
class TaskResult:
    task: str
    questions: int
    base: float
    candidate: float
    broke: int
    fixed: int
    p: float = 1.0
    p_adjusted: float = 1.0
    verdict: str = "same"
    examples: list = field(default_factory=list)

    @property
    def change(self):
        return self.candidate - self.base


def mcnemar(broke, fixed):
    """Two-sided exact test on the discordant pairs."""
    n = broke + fixed
    return 1.0 if n == 0 else float(binomtest(broke, n, 0.5).pvalue)


def holm(pvalues):
    order = np.argsort(pvalues)
    adjusted, running = np.empty(len(pvalues)), 0.0
    for rank, i in enumerate(order):
        running = max(running, min(1.0, (len(pvalues) - rank) * pvalues[i]))
        adjusted[i] = running
    return adjusted


def compare(base, candidate, by="task", examples=3):
    """base, candidate: {question key: record} from data.load. Returns (overall, [TaskResult])."""
    keys = sorted(set(base) & set(candidate))
    groups = {}
    for k in keys:
        groups.setdefault(base[k][by], []).append(k)
    results = []
    for name, ks in sorted(groups.items()):
        b = np.array([base[k]["correct"] for k in ks])
        c = np.array([candidate[k]["correct"] for k in ks])
        broke, fixed = int(((b == 1) & (c == 0)).sum()), int(((b == 0) & (c == 1)).sum())
        r = TaskResult(name, len(ks), float(b.mean()), float(c.mean()), broke, fixed, mcnemar(broke, fixed))
        r.examples = [{"question": base[k]["question"][:300], "was": base[k]["answer"][:160], "now": candidate[k]["answer"][:160]}
                      for k in ks if base[k]["correct"] and not candidate[k]["correct"]][:examples]
        results.append(r)
    for r, adj in zip(results, holm([r.p for r in results])):
        r.p_adjusted = float(adj)
        if adj < ALPHA and abs(r.change) >= MIN_DROP:
            r.verdict = "regressed" if r.change < 0 else "improved"
    b = np.array([base[k]["correct"] for k in keys])
    c = np.array([candidate[k]["correct"] for k in keys])
    overall = {"questions": len(keys), "base": float(b.mean()), "candidate": float(c.mean()),
               "broke": int(((b == 1) & (c == 0)).sum()), "fixed": int(((b == 0) & (c == 1)).sum()),
               "output_tokens": {"base": float(np.mean([base[k]["output_tokens"] for k in keys])),
                                 "candidate": float(np.mean([candidate[k]["output_tokens"] for k in keys]))}}
    return overall, results


def report(base_name, cand_name, overall, results):
    pct = lambda x: f"{100 * x:.1f}%"
    lines = [f"## {base_name} → {cand_name}", "",
             f"Overall: {pct(overall['base'])} → {pct(overall['candidate'])} on {overall['questions']:,} questions "
             f"({overall['broke']} broke, {overall['fixed']} fixed). Mean output tokens "
             f"{overall['output_tokens']['base']:.0f} → {overall['output_tokens']['candidate']:.0f}.", "",
             "| Task | Questions | Before | After | Broke | Fixed | p (Holm) | Verdict |", "|---|---|---|---|---|---|---|---|"]
    for r in results:
        lines.append(f"| {r.task} | {r.questions} | {pct(r.base)} | {pct(r.candidate)} | {r.broke} | {r.fixed} | "
                     f"{r.p_adjusted:.3g} | {'**' + r.verdict + '**' if r.verdict != 'same' else 'same'} |")
    for r in results:
        if r.verdict == "regressed" and r.examples:
            lines += ["", f"Broken in {r.task}, for example:"]
            lines += [f"- {e['question'][:140]!r}: was {e['was'][:60]!r}, now {e['now'][:60]!r}" for e in r.examples]
    return "\n".join(lines)
