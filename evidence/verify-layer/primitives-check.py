#!/usr/bin/env python3
"""Recompute every primitives.json entry against its AUTHORITY and report drift.

primitives.json is the discovery/index surface — NOT a source of truth. Authority is:
  • contract        → the on-chain bytecode (eth_getCode on the named chain)
  • repo / note     → the repository state (github.com/trustless-ai/<name>)
  • recompute-recipe→ the conformance package (recompute-kit/conformance/<name>)
  • erc             → the ERC PR / assets (index-only here; author verifies at the PR)

A mismatch means the ENTRY is stale, not that the registry is truth. Exit 1 if any entry
drifts, so CI catches a stale index before anyone trusts it.

Env: ALCHEMY_KEY (or ~/.claude/alchemy_key) for eth_getCode; `gh` for GitHub authority checks.
"""
import json, os, sys, time, subprocess, urllib.request, pathlib

HERE = pathlib.Path(__file__).parent
REG = json.loads((HERE / "primitives.json").read_text())

def alchemy_key():
    k = os.environ.get("ALCHEMY_KEY")
    if k: return k.strip()
    p = pathlib.Path.home() / ".claude" / "alchemy_key"
    return p.read_text().strip() if p.exists() else None

KEY = alchemy_key()
NET = {"mainnet": "eth-mainnet", "sepolia": "eth-sepolia"}
# An RPC is a resolution TRANSPORT, not chain-state AUTHORITY. A single RPC's word must never
# silently decide an entry — an untrusted node once returned "0 bytes" for a live contract. So we
# query >=2 DISTINCT-PROVIDER RPCs and only decide PASS/STALE when they AGREE; on disagreement we
# emit UNRESOLVED rather than pick a side; if <2 answer we emit CANNOT_CHECK (fail closed, never
# a silent pass). NOTE: "distinct provider" is by endpoint, NOT a formal independence criterion —
# these providers may share upstream data sources, so agreement is corroboration bounded by that.
# Two RPCs agreeing is CORROBORATION, not independently re-derived consensus — full header
# verification (eth_getProof / light client) is a further leg the verify-layer repo carries.
# (Rule from Pavlo; boundary named by babyblueviper1; fail-closed edge caught by Pavlo, WG 2026-09-03.)
PUBLIC = {
    "mainnet": ["https://ethereum-rpc.publicnode.com", "https://eth.drpc.org",
                "https://rpc.mevblocker.io", "https://1rpc.io/eth"],
    "sepolia": ["https://ethereum-sepolia-rpc.publicnode.com", "https://eth-sepolia.public.blastapi.io",
                "https://sepolia.gateway.tenderly.co", "https://1rpc.io/sepolia"],
}

def _endpoints(chain):
    eps = []
    env = os.environ.get(f"RPC_URL_{chain.upper()}")
    if env: eps.append(env)
    if KEY and chain in NET: eps.append(f"https://{NET[chain]}.g.alchemy.com/v2/{KEY}")
    eps += PUBLIC.get(chain, [])
    seen, out = set(), []
    for e in eps:
        if e not in seen: seen.add(e); out.append(e)
    return out

def _label(url):
    if "alchemy" in url: return "alchemy"
    if "publicnode" in url: return "publicnode"
    return url.split("//",1)[-1].split("/",1)[0][:20]

def _getcode_one(url, addr, retries=2):
    """One endpoint -> (has_code:bool | None, detail). None means no usable answer. Retries on transient fail."""
    body = json.dumps({"jsonrpc":"2.0","id":1,"method":"eth_getCode","params":[addr,"latest"]}).encode()
    hdr = {"Content-Type":"application/json", "User-Agent":"trustless-ai-primitives-check/1.0"}
    for attempt in range(retries + 1):
        req = urllib.request.Request(url, data=body, headers=hdr)
        try:
            r = json.loads(urllib.request.urlopen(req, timeout=20).read())
            code = r.get("result")
            if not isinstance(code, str): return None, "err"
            return (code != "0x" and len(code) > 2), ("code" if code != "0x" else "empty")
        except Exception:
            if attempt < retries: time.sleep(0.6 * (attempt + 1)); continue
            return None, "fail"

def eth_getcode(addr, chain):
    """(state, detail) in {PASS, STALE, UNRESOLVED, SKIP}. Queries independent RPCs, short-circuits at 2 valid."""
    answers, notes = [], []
    for url in _endpoints(chain):
        ok, info = _getcode_one(url, addr)
        notes.append(f"{_label(url)}:{info}")
        if ok is not None:
            answers.append(ok)
            if len(answers) >= 2: break   # 2 independent answers is enough to decide/disagree
    n = len(answers)
    ctx = "; ".join(notes)
    if n < 2:
        # A required check that couldn't obtain enough observations must NOT pass silently
        # (availability failure would weaken the gate). Fail closed, not open.
        return "CANNOT_CHECK", f"only {n} RPC answered — need >=2 to corroborate ({ctx})"
    if all(answers): return "PASS", f"{n} RPCs agree: has code ({ctx})"
    if not any(answers): return "STALE", f"{n} RPCs agree: EMPTY ({ctx})"
    return "UNRESOLVED", f"RPCs DISAGREE — not deciding ({ctx})"

def gh_exists(path):
    """gh api <path> → True if 200, False if 404, None on other error."""
    try:
        p = subprocess.run(["gh","api",path,"--silent"], capture_output=True, text=True, timeout=25)
        if p.returncode == 0: return True, "200"
        if "404" in (p.stderr or ""): return False, "404"
        return None, (p.stderr or "").strip()[:60]
    except Exception as e:
        return None, str(e)[:60]

def ref_repo(ref):  # "github.com/trustless-ai/verify-layer" -> "repos/trustless-ai/verify-layer"
    tail = ref.split("github.com/",1)[-1].strip("/")
    return "repos/" + tail

def check(e):
    pf = e.get("proof",{}); t = pf.get("type")
    if t == "contract":
        return eth_getcode(pf["address"], pf.get("chain") or e.get("chain"))
    if t == "recompute-recipe":
        # ref: trustless-ai/recompute-kit/conformance/<name>. True=exists PASS, False=404 STALE,
        # None=transport error CANNOT_CHECK (a failed lookup must not read as verified — silent-skip class).
        tail = pf["ref"].split("recompute-kit/",1)[-1]  # conformance/<name>
        ok, detail = gh_exists(f"repos/trustless-ai/recompute-kit/contents/{tail}")
        return ("PASS" if ok else "STALE" if ok is False else "CANNOT_CHECK"), f"recompute-kit/{tail} {detail}"
    if t == "repo":
        ok, detail = gh_exists(ref_repo(pf["ref"]))
        return ("PASS" if ok else "STALE" if ok is False else "CANNOT_CHECK"), f"{pf['ref']} {detail}"
    if t == "surface":
        url = pf["url"]
        hdr = {"User-Agent":"trustless-ai-primitives-check/1.0"}
        try:
            code = urllib.request.urlopen(urllib.request.Request(url, headers=hdr), timeout=15).getcode()
            return ("PASS" if code == 200 else "STALE"), f"GET {url} -> {code}"
        except Exception as e:
            return "CANNOT_CHECK", f"GET {url} failed: {str(e)[:60]}"
    if t == "erc":
        return "INDEX", f"{pf['ref']} (verify at the ERC PR)"
    if e.get("optional") is True:
        return "SKIP", f"explicitly declared non-required (proof type {t!r})"
    # Unknown/unsupported proof type on a non-optional entry must NOT become a silent pass — a typo
    # like 'contrcat' would otherwise downgrade a required check to exit-0 SKIP. Fail closed; SKIP is
    # reserved for entries that explicitly set "optional": true.
    return "CANNOT_CHECK", f"unsupported proof type {t!r} — not a known required check (typo? or set optional:true)"

def main():
    rows, counts = [], {}
    for e in REG["primitives"]:
        state, detail = check(e)
        counts[state] = counts.get(state,0)+1
        rows.append((state, e["name"], detail))
    icon = {"PASS":"✅","STALE":"❌","UNRESOLVED":"🟠","CANNOT_CHECK":"🚫","SKIP":"⚠️","INDEX":"📄"}
    for state, name, detail in rows:
        print(f"{icon.get(state,'?')} {state:12} {name[:44]:44} {detail}")
    print("\n" + "  ".join(f"{k}:{v}" for k,v in sorted(counts.items())))
    stale = counts.get("STALE",0); unresolved = counts.get("UNRESOLVED",0); cannot = counts.get("CANNOT_CHECK",0)
    if stale:
        print(f"\n{stale} STALE entr{'y' if stale==1 else 'ies'} — the INDEX drifted from AUTHORITY. Fix primitives.json.")
        return 1
    if unresolved or cannot:
        # A required check that disagreed OR couldn't run must fail closed — availability/consistency
        # failure must never leave the success signal untouched (silent-skip class). SKIP (non-required) is fine.
        print(f"\n{unresolved} UNRESOLVED (RPCs disagreed) + {cannot} CANNOT_CHECK (couldn't corroborate a required "
              f"entry) — gate fails closed, investigate before trusting these (exit 2).")
        return 2
    print("\nNo drift: every required entry corroborated against its authority.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
