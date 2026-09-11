const inScope = (e, v) => e.admitted && e.rootId.toLowerCase() === v.rootId.toLowerCase() && e.periodIndex === v.periodIndex;
function rootKeyedSum(v) {
  return v.log.filter((e) => inScope(e, v)).reduce((a, e) => a + BigInt(e.amount), 0n);
}
function maxEdgeSubtotal(v) {
  const byEdge = /* @__PURE__ */ new Map();
  for (const e of v.log) if (inScope(e, v)) byEdge.set(e.edge, (byEdge.get(e.edge) ?? 0n) + BigInt(e.amount));
  let max = 0n;
  for (const s of byEdge.values()) if (s > max) max = s;
  return max;
}
function valueFor(v, tamper) {
  const sum = tamper ? maxEdgeSubtotal(v) : rootKeyedSum(v);
  return { admittedSum: sum.toString(), conserves: sum <= BigInt(v.cap) };
}
if (import.meta.main) {
  const tamper = Bun.argv.includes("--tamper");
  if (Bun.argv.includes("--grade")) {
    const fx2 = JSON.parse(await Bun.stdin.text());
    const out = {};
    for (const v of fx2.vectors) out[v.name] = valueFor(v, tamper);
    console.log(JSON.stringify(out));
    process.exit(0);
  }
  const fx = JSON.parse(await Bun.file(`${import.meta.dir}/aggregate-budget-v0.vectors.json`).text());
  let fails = 0;
  for (const v of fx.vectors) {
    const got = valueFor(v, tamper);
    const ok = JSON.stringify(got) === JSON.stringify(v.expected);
    if (!ok) fails++;
    console.log(`${ok ? "\u2713" : "\u2717"} ${v.name.padEnd(34)} sum=${got.admittedSum.padStart(5)} cap=${String(v.cap).padStart(5)} conserves=${got.conserves}`);
  }
  console.log(`${fx.vectors.length - fails}/${fx.vectors.length} reproduced${tamper ? " (tamper: wrong per-edge method \u2014 mismatches are expected)" : ""}`);
  process.exit(fails ? 1 : 0);
}
export {
  valueFor
};
