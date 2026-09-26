from regress.compare import compare, holm, mcnemar


def rec(task, correct, answer="x"):
    return {"task": task, "subtask": "", "question": "q", "correct": correct, "answer": answer, "output_tokens": 5}


def test_mcnemar_is_symmetric_and_calm_on_ties():
    assert mcnemar(0, 0) == 1.0 and mcnemar(10, 10) == 1.0
    assert mcnemar(30, 5) < 0.001 and abs(mcnemar(30, 5) - mcnemar(5, 30)) < 1e-12


def test_holm_never_lowers_a_pvalue_and_keeps_order():
    adj = holm([0.01, 0.04, 0.03])
    assert all(a >= p for a, p in zip(adj, [0.01, 0.04, 0.03]))
    assert abs(adj[0] - 0.03) < 1e-12


def test_a_hidden_regression_is_caught_while_overall_accuracy_holds():
    base, cand = {}, {}
    for i in range(200):          # task a: 60 answers break
        base[f"a{i}"], cand[f"a{i}"] = rec("a", 1), rec("a", 0 if i < 60 else 1)
    for i in range(200):          # task b: 60 answers get fixed
        base[f"b{i}"], cand[f"b{i}"] = rec("b", 0 if i < 60 else 1), rec("b", 1)
    overall, results = compare(base, cand)
    assert overall["base"] == overall["candidate"]
    verdicts = {r.task: r.verdict for r in results}
    assert verdicts == {"a": "regressed", "b": "improved"}


def test_small_noisy_changes_do_not_block_a_release():
    base = {f"q{i}": rec("t", i % 2) for i in range(400)}
    cand = {f"q{i}": rec("t", (i + (1 if i < 8 else 0)) % 2) for i in range(400)}
    _, results = compare(base, cand)
    assert results[0].verdict == "same"
