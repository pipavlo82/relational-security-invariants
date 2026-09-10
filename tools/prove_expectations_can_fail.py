"""Mapped expectation attacks and enforcement mutants, separate from legacy 12."""
import argparse
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import py_compile
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from rsi.codec import encode, load, raw_digest
from profiles.synthetic import make_profile
from runner.expectation_contract import admit, load_fixtures, ProfileError

STATES = ("KILLED", "SURVIVED", "VACUOUS", "NOT_APPLIED")
DEFINITIONS = (
    {"id":"EXP-M3", "old":"if encode(recomputed[ident]) != encode(recorded):  # EXP-M3", "new":"if False:  # EXP-M3", "mapped":"tests.test_expectations.ExpectationTests.test_modified_value_rejected"},
    {"id":"EXP-M4", "old":"if mismatches:  # EXP-M4: one mismatch prevents admission of every row", "new":"if False:  # EXP-M4 disabled atomic barrier", "mapped":"tests.test_expectations.ExpectationTests.test_atomic_admission"},
)


def copy_repo(destination):
    shutil.copytree(ROOT,destination,ignore=shutil.ignore_patterns(".git",".venv","artifacts","__pycache__","*.pyc"))


def classify(rows, mapped, applied=True):
    if not applied:
        return "NOT_APPLIED"
    if not rows or any(r["status"]=="ERROR" for r in rows):
        return "VACUOUS"
    target=[r for r in rows if r["id"]==mapped]
    if len(target)!=1:
        return "VACUOUS"
    return "KILLED" if target[0]["status"]=="FAIL" else "SURVIVED"


def track_phases(suite):
    for test in suite:
        if isinstance(test, unittest.TestSuite):
            track_phases(test)
            continue
        for method, phase in (("_callSetUp", "setup"), ("_callTestMethod", "test"), ("_callTearDown", "teardown"), ("_callCleanup", "cleanup")):
            original = getattr(test, method)
            def wrapped(*args, _test=test, _original=original, _phase=phase, **kwargs):
                _test._expectation_phase = _phase
                return _original(*args, **kwargs)
            setattr(test, method, wrapped)


class ExecutionResult(unittest.TestResult):
    def __init__(self):
        super().__init__()
        self.rows = []
    def addSuccess(self, test):
        super().addSuccess(test)
        self.rows.append({"id": test.id(), "status": "PASS"})
    def addFailure(self, test, error):
        super().addFailure(test, error)
        phase = getattr(test, "_expectation_phase", "unknown")
        self.rows.append({"id": test.id(), "status": "FAIL" if phase == "test" else "ERROR", "phase": phase})
    def addError(self, test, error):
        super().addError(test, error)
        self.rows.append({"id": test.id(), "status": "ERROR", "phase": getattr(test, "_expectation_phase", "unknown")})


def child(output):
    suite=unittest.defaultTestLoader.loadTestsFromName("tests.test_expectations.ExpectationTests")
    track_phases(suite)
    result=ExecutionResult();suite.run(result)
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_bytes(encode({"tests_run":result.testsRun,"rows":result.rows}))
    return 0 if result.wasSuccessful() else 1


def run_tests(root):
    output=root/"artifacts/expectation-child.json"
    p=subprocess.run([sys.executable,"-B","tools/prove_expectations_can_fail.py","--child",str(output)],cwd=root,capture_output=True,text=True,timeout=90)
    return p,load(output) if output.exists() else None


def source_mutation(definition):
    record={"id":definition["id"],"kind":"source_enforcement_mutation","status":"NOT_APPLIED","mapped_check":definition["mapped"],"collateral":[]}
    with tempfile.TemporaryDirectory(prefix="rsi-exp-mutant-") as temp:
        root=Path(temp)/"repo";copy_repo(root)
        path=root/"runner/expectation_contract.py";source=path.read_text(encoding="utf-8")
        if source.count(definition["old"])!=1 or definition["old"]==definition["new"]:
            return record
        mutated=source.replace(definition["old"],definition["new"],1)
        path.write_text(mutated,encoding="utf-8",newline="\n")
        record.update(source_sha256=raw_digest(source.encode()),mutant_sha256=raw_digest(mutated.encode()))
        try:
            py_compile.compile(str(path),doraise=True)
            process,report=run_tests(root)
        except Exception as exc:
            record.update(status="VACUOUS",error=type(exc).__name__)
            return record
        rows=report["rows"] if report else []
        record.update(status=classify(rows,definition["mapped"]),exit_code=process.returncode,checks=rows,
                      collateral=[r["id"] for r in rows if r["status"]=="FAIL" and r["id"]!=definition["mapped"]])
    return record


def tamper(ident):
    target="PREDICTION_MISMATCH" if ident=="EXP-M1" else "FIXTURE_SET_DIGEST"
    record={"id":ident,"kind":"recorded_evidence_tamper","mapped_check":target,"status":"VACUOUS","collateral":[]}
    with tempfile.TemporaryDirectory(prefix="rsi-exp-tamper-") as temp:
        root=Path(temp)/"repo";copy_repo(root)
        profile=make_profile(root);fixtures=load_fixtures(root,profile)
        try: admit(root,profile,fixtures)
        except Exception as exc:
            record["error"]="baseline: "+type(exc).__name__;return record
        if ident=="EXP-M1":
            path=root/profile.expectations_path;value=load(path)
            prediction=value["expectations"][-1]["prediction"];key=next(iter(prediction))
            event=prediction[key]["observation"]["results"][0]
            event["decision"]="REJECT" if event["decision"]=="ACCEPT" else "ACCEPT"
            path.write_bytes(encode(value))
            # Repin deliberately: digest correctness alone must not authorize it.
            profile=replace(profile,expectations_digest=raw_digest(path.read_bytes()))
        else:
            source=profile.fixture_scope[0];path=root/source.path;value=load(path)
            for case in value["cases"]:
                for req in case["requests"].values():req["state"]["head"]="other-initial-state"
            path.write_bytes(encode(value));fixtures=load_fixtures(root,profile)
        try:
            admit(root,profile,fixtures)
            record["status"]="SURVIVED"
        except ProfileError as exc:
            record.update(status="KILLED" if exc.code==target else "VACUOUS",executed_check=exc.code)
        except Exception as exc:
            record.update(status="VACUOUS",error=type(exc).__name__)
    return record


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--child",type=Path)
    parser.add_argument("--output",type=Path,default=ROOT/"artifacts/expectation-mutations.json")
    args=parser.parse_args()
    if args.child:return child(args.child)
    process,baseline=run_tests(ROOT)
    if process.returncode or baseline is None:
        print("Expectation architecture baseline is not green",file=sys.stderr);return 2
    records=[tamper("EXP-M1"),tamper("EXP-M2")]+[source_mutation(d) for d in DEFINITIONS]
    counts={s:0 for s in STATES}
    for r in records:counts[r["status"]]+=1
    report={"schema":"rsi-expectation-mutation-report.v0","baseline":baseline,"counts":counts,"mutations":records,
            "provenance_rules":[{"id":"EXP-M5","classification":"PROVENANCE_RULE_NOT_A_MUTATION","reason":"Trusted Python callables are not sandboxed. Arbitrary filesystem reads/closures cannot be ruled out by an honest generic mechanical test. Input-channel separation, evaluation order, direct self-validation rejection and source review are required; no fake kill is counted."}]}
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_bytes(encode(report))
    print(json.dumps(counts,sort_keys=True))
    return 0 if all(r["status"]=="KILLED" for r in records) else 1

if __name__=="__main__":raise SystemExit(main())
