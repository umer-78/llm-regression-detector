import { $, diverge, esc, fail, int, kpis, load, pct, pts, select, table } from './kit.js';

const verdict = (v) => `<span class="pill ${v === 'regressed' ? 'no' : v === 'improved' ? 'ok' : 'mid'}">${esc(v)}</span>`;
const pair = (u) => `${u.base_model} → ${u.candidate_model}`;

try {
  const data = await load();
  const hidden = data.filter((u) => u.regressed.length && u.candidate - u.base > -0.01);
  kpis($('#kpis'), [
    { label: 'Real upgrades tested', value: String(data.length), note: 'same vendor, old version against new' },
    { label: 'Broke at least one task', value: `${data.filter((u) => u.regressed.length).length} of ${data.length}`, note: 'significant after Holm correction' },
    { label: 'Hidden by the average', value: String(hidden.length), note: 'a task regressed while overall moved less than a point down, or went up' },
    { label: 'Questions per upgrade', value: int(Math.max(...data.map((u) => u.questions))), note: 'GSM8K, LegalBench, MATH, MMLU, OpenBookQA' },
  ]);
  const show = (i) => {
    const u = data[+i];
    $('#overall').innerHTML = `<div>Overall accuracy<b>${pct(u.base)} → ${pct(u.candidate)}</b><span class="muted small">${pts(u.candidate - u.base)} points</span></div>` +
      `<div>Questions compared<b>${int(u.questions)}</b><span class="muted small">${int(u.broke)} broke, ${int(u.fixed)} fixed</span></div>` +
      `<div>Release gate<b>${u.regressed.length ? `fails: ${esc(u.regressed.join(', '))}` : 'passes'}</b><span class="muted small">${u.improved.length ? `improved: ${esc(u.improved.join(', '))}` : 'no task improved significantly'}</span></div>`;
    diverge($('#change'), u.tasks.map((t) => ({
      label: t.task, value: t.candidate - t.base, text: pts(t.candidate - t.base),
      color: t.verdict === 'regressed' ? 'var(--bad)' : t.verdict === 'improved' ? 'var(--good)' : 'var(--c6)',
      title: `${t.task}: ${pct(t.base)} → ${pct(t.candidate)}, ${t.verdict}`,
    })), { max: Math.max(0.05, ...u.tasks.map((t) => Math.abs(t.candidate - t.base))) });
    table($('#tasks'), [
      { key: 'task', label: 'Task' },
      { key: 'questions', label: 'Questions', num: true, fmt: int },
      { key: 'base', label: 'Before', num: true, fmt: (v) => pct(v) },
      { key: 'candidate', label: 'After', num: true, fmt: (v) => pct(v) },
      { key: 'broke', label: 'Broke', num: true, fmt: int },
      { key: 'fixed', label: 'Fixed', num: true, fmt: int },
      { key: 'p_adjusted', label: 'p (Holm)', num: true, fmt: (v) => (v >= 0.001 ? v.toFixed(3) : v.toExponential(1)) },
      { key: 'verdict', label: 'Verdict', html: true, fmt: verdict },
    ], u.tasks, { cls: (t) => ({ regressed: 'bad', improved: 'good' })[t.verdict] || '' });
  };
  select($('#pair'), data.map((u, i) => [i, pair(u)]), data.findIndex((u) => u.regressed.length) >= 0 ? data.findIndex((u) => u.regressed.length) : 0, show);
  table($('#all'), [
    { key: 'name', label: 'Upgrade' },
    { key: 'change', label: 'Overall', num: true, fmt: (v) => `${pts(v)} pts` },
    { key: 'regressed', label: 'Regressed', fmt: (v) => v.join(', ') || '–' },
    { key: 'improved', label: 'Improved', fmt: (v) => v.join(', ') || '–' },
    { key: 'gate', label: 'Gate', html: true, fmt: (v) => `<span class="pill ${v ? 'no' : 'ok'}">${v ? 'fail' : 'pass'}</span>` },
  ], data.map((u) => ({ name: pair(u), change: u.candidate - u.base, regressed: u.regressed, improved: u.improved, gate: u.regressed.length > 0 })));
} catch (err) {
  fail(err);
}
