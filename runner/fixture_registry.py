"""Explicit corpus discovery and opaque canonical fixture identities."""
from dataclasses import dataclass
from pathlib import Path
import re
from rsi.codec import decode, raw_digest
from runner.expectation_contract import safe_path

ID_PATTERN = r"[a-z0-9][a-z0-9._-]{0,63}:[A-Za-z0-9][A-Za-z0-9._-]{0,127}"
NAME_PATTERN = r"[a-z0-9][a-z0-9._-]{0,63}"

class CorpusError(ValueError):
    pass


def identity(value):
    if type(value) is not str or re.fullmatch(ID_PATTERN, value) is None:
        raise CorpusError("invalid canonical fixture identity")
    return value


def scan_json(directory):
    pending, found = [directory], set()
    while pending:
        current = pending.pop()
        for path in sorted(current.iterdir()):
            if path.is_symlink() or path.is_junction():
                raise CorpusError("filesystem link in registered corpus")
            if path.is_dir():
                pending.append(path)
            elif path.is_file() and path.suffix.lower() == ".json":
                found.add(path)
    return found


@dataclass(frozen=True)
class Corpus:
    corpus_id: str
    manifest_path: str
    manifest_digest: str
    validate_fixture: object


class FixtureRegistry:
    def __init__(self, corpora=()):
        self._corpora = {}
        for corpus in corpora:
            self.register(corpus)

    def register(self, corpus):
        if not isinstance(corpus, Corpus) or not callable(corpus.validate_fixture):
            raise CorpusError("trusted corpus validator required")
        if type(corpus.corpus_id) is not str or re.fullmatch(NAME_PATTERN, corpus.corpus_id) is None:
            raise CorpusError("invalid corpus identity")
        if corpus.corpus_id in self._corpora:
            raise CorpusError("duplicate corpus identity")
        if type(corpus.manifest_digest) is not str or re.fullmatch(r"[0-9a-f]{64}", corpus.manifest_digest) is None:
            raise CorpusError("invalid manifest digest")
        self._corpora[corpus.corpus_id] = corpus

    def discover(self, root):
        if not self._corpora:
            return {"fixtures":[],"errors":[{"corpus_id":"","status":"INVALID_FIXTURE","diagnostic_kind":"CORPUS_ERROR","error":"empty corpus registry"}]}
        records, errors, identities = [], [], set()
        inventories, all_declared = [], set()
        for corpus_id, corpus in sorted(self._corpora.items()):
            try:
                raw = safe_path(root, corpus.manifest_path).read_bytes()
                if raw_digest(raw) != corpus.manifest_digest:
                    raise CorpusError("manifest digest mismatch")
                manifest = decode(raw, canonical=True)
                required = {"schema", "corpus_id", "namespace", "fixture_directory", "fixtures"}
                if type(manifest) is not dict or set(manifest) != required or manifest["schema"] != "rsi-fixture-corpus.v0" or manifest["corpus_id"] != corpus_id:
                    raise CorpusError("invalid corpus manifest")
                namespace = manifest["namespace"]
                if type(namespace) is not str or re.fullmatch(NAME_PATTERN, namespace) is None:
                    raise CorpusError("invalid namespace")
                directory = safe_path(root, manifest["fixture_directory"])
                if not directory.is_dir():
                    raise CorpusError("missing fixture directory")
                entries = manifest["fixtures"]
                if type(entries) is not list or not entries:
                    raise CorpusError("explicit nonempty fixture declarations required")
                declared, pending = set(), []
                for entry in entries:
                    keys = {"fixture_id", "fixture_source_id", "path", "expectation_profile_id", "adapter_bindings"}
                    if type(entry) is not dict or set(entry) != keys:
                        raise CorpusError("invalid fixture registration")
                    ident = identity(entry["fixture_id"])
                    # Namespace parsing validates identity syntax only; it selects no behavior.
                    if ident.split(":", 1)[0] != namespace:
                        raise CorpusError("namespace declaration differs from identity")
                    if ident in identities:
                        raise CorpusError("duplicate canonical fixture identity")
                    identities.add(ident)
                    for field in ("fixture_source_id", "expectation_profile_id"):
                        if type(entry[field]) is not str or not entry[field] or not entry[field].isascii():
                            raise CorpusError("invalid registration identity")
                    bindings = entry["adapter_bindings"]
                    if type(bindings) is not dict or not bindings or any(type(k) is not str or not k or type(v) is not str or not v or not k.isascii() or not v.isascii() for k,v in bindings.items()):
                        raise CorpusError("invalid adapter bindings")
                    path = safe_path(root, entry["path"])
                    if not path.is_relative_to(directory) or path.suffix.lower() != ".json" or path in declared:
                        raise CorpusError("duplicate or out-of-corpus fixture path")
                    declared.add(path)
                    pending.append((entry, path))
                inventories.append((corpus_id, directory))
                all_declared.update(declared)
                for entry, path in sorted(pending, key=lambda item: item[0]["fixture_id"]):
                    record = dict(entry, corpus_id=corpus_id, manifest_sha256=corpus.manifest_digest)
                    try:
                        data = path.read_bytes()
                        value = decode(data, canonical=True)
                        if type(value) is not dict or value.get("id") != entry["fixture_source_id"]:
                            raise ValueError("source fixture identity mismatch")
                        corpus.validate_fixture(value)
                        record.update(status="READY", fixture_sha256=raw_digest(data))
                    except Exception as exc:
                        record.update(status="INVALID_FIXTURE", error=type(exc).__name__)
                    records.append(record)
            except Exception as exc:
                errors.append({"corpus_id":corpus_id,"status":"INVALID_FIXTURE","diagnostic_kind":"CORPUS_ERROR","error":str(exc)})
        # A nested corpus explicitly declares its own files. Parent directories
        # cannot silently consume them, nor reject them merely for being nested.
        for corpus_id, directory in inventories:
            try:
                observed = scan_json(directory)
            except Exception as exc:
                errors.append({"corpus_id":corpus_id,"status":"INVALID_FIXTURE","diagnostic_kind":"CORPUS_ERROR","error":str(exc)})
                continue
            extras = observed - all_declared
            if extras:
                errors.append({"corpus_id":corpus_id,"status":"INVALID_FIXTURE","diagnostic_kind":"CORPUS_ERROR",
                               "error":"undeclared fixture JSON: " + ",".join(sorted(p.as_posix() if not p.is_relative_to(Path(root).resolve()) else p.relative_to(Path(root).resolve()).as_posix() for p in extras))})
        return {"fixtures":sorted(records,key=lambda row:row["fixture_id"]),"errors":sorted(errors,key=lambda row:(row["corpus_id"],row["error"]))}
