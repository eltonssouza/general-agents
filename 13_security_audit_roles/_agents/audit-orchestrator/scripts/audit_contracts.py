# -*- coding: utf-8 -*-
"""
audit_contracts.py - gate G2 (contracts) of the multi-agent audit: validates JSON against the package contracts
and checks the invariants the schema does not cover, reopening the evidence in the snapshot when --repo is given.

Schema validation with the standard library (the subset of Draft 2020-12 used by the contracts: type, enum,
const, required, properties, additionalProperties, items, minItems, minLength, pattern, minimum, maximum,
$ref, oneOf, allOf, if/then). Extra invariants:
  - line_end >= line_start;                                        (quality-gates, invariant 2)
  - every repository_revision equals --revision, if given;         (invariant 6)
  - CONFIRMED with validation.independent_review = true and checked_evidence_refs that exist in the finding; (invariant 1)
  - excerpt_redacted without an apparent clear-text secret;        (invariant 9)
  - with --repo: the evidence file exists in the snapshot, without escaping it, and the lines exist; file_sha256 matches;
    the excerpt, when not masked, appears in the cited lines (warning).                                (G2/G3)
Reads files as DATA; never executes anything from the repository. Read-only, no network, stdlib.

Usage:
  python -I audit_contracts.py result.json [other.json ...] [--kind auto|agent-result|finding|findings|audit-run]
                               [--repo SNAPSHOT_PATH] [--revision REV] [--json]
Exit: 0 no errors (warnings allowed), 1 with errors, 2 usage/read error.
"""
import argparse
import hashlib
import json
import os
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
CONTRACTS = os.path.normpath(os.path.join(HERE, "..", "contracts"))
SECRET_PATTERNS = [
    (r"AKIA[0-9A-Z]{16}", "AWS access key"),
    (r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----", "private key"),
    (r"\bgh[pousr]_[A-Za-z0-9]{30,}", "GitHub token"),
    (r"\bxox[abprs]-[A-Za-z0-9-]{10,}", "Slack token"),
    (r"\bsk-[A-Za-z0-9]{20,}", "API key"),
    (r"(?i)\b(?:password|passwd|senha|secret|token|api_key)\s*[:=]\s*['\"][^'\"*•x]{6,}['\"]", "literal credential"),
]
MASK = re.compile(r"\*{3,}|•{3,}|<redacted>|<REDACTED>|\[REDACTED\]|x{6,}")
TYPES = {"string": str, "object": dict, "array": list, "boolean": bool, "null": type(None)}


def load_schemas():
    out = {}
    for name in ("finding", "agent-result", "audit-run"):
        path = os.path.join(CONTRACTS, name + ".schema.json")
        if os.path.isfile(path):
            with open(path, encoding="utf-8") as f:
                out[name + ".schema.json"] = json.load(f)
    return out


def type_ok(v, t):
    if t == "boolean":
        return isinstance(v, bool)
    if isinstance(v, bool):  # in Python bool is an int; in JSON Schema it is neither an integer nor a number
        return False
    if t == "integer":
        return isinstance(v, int)
    if t == "number":
        return isinstance(v, (int, float))
    return isinstance(v, TYPES[t])


class Validator:
    def __init__(self, schemas):
        self.schemas = schemas

    def resolve(self, ref, root):
        if ref.startswith("#/"):
            node = root
            for part in ref[2:].split("/"):
                node = node[part]
            return node, root
        doc = self.schemas[ref.split("#")[0]]
        return doc, doc

    def errors(self, v, s, root, path="$"):
        errs = []
        if "$ref" in s:
            target, troot = self.resolve(s["$ref"], root)
            errs += self.errors(v, target, troot, path)
        if "type" in s:
            ts = s["type"] if isinstance(s["type"], list) else [s["type"]]
            if not any(type_ok(v, t) for t in ts):
                return errs + ["%s: expected type %s" % (path, "/".join(ts))]
        if "const" in s and v != s["const"]:
            errs.append("%s: must be %r" % (path, s["const"]))
        if "enum" in s and v not in s["enum"]:
            errs.append("%s: value %r outside %s" % (path, v, s["enum"]))
        if isinstance(v, str):
            if len(v) < s.get("minLength", 0):
                errs.append("%s: text too short" % path)
            if "pattern" in s and not re.search(s["pattern"], v):
                errs.append("%s: %r does not match %s" % (path, v, s["pattern"]))
        if isinstance(v, (int, float)) and not isinstance(v, bool):
            if "minimum" in s and v < s["minimum"]:
                errs.append("%s: less than %s" % (path, s["minimum"]))
            if "maximum" in s and v > s["maximum"]:
                errs.append("%s: greater than %s" % (path, s["maximum"]))
        if isinstance(v, list):
            if len(v) < s.get("minItems", 0):
                errs.append("%s: needs at least %d item(s)" % (path, s["minItems"]))
            if "items" in s:
                for i, item in enumerate(v):
                    errs += self.errors(item, s["items"], root, "%s[%d]" % (path, i))
        if isinstance(v, dict):
            for k in s.get("required", []):
                if k not in v:
                    errs.append("%s: required field missing '%s'" % (path, k))
            props = s.get("properties", {})
            for k, val in v.items():
                if k in props:
                    errs += self.errors(val, props[k], root, "%s.%s" % (path, k))
                elif s.get("additionalProperties") is False:
                    errs.append("%s: unexpected field '%s'" % (path, k))
        for sub in s.get("allOf", []):
            if "if" in sub:
                if not self.errors(v, sub["if"], root, path):
                    errs += self.errors(v, sub.get("then", {}), root, path)
            else:
                errs += self.errors(v, sub, root, path)
        if "oneOf" in s:
            ok = [o for o in s["oneOf"] if not self.errors(v, o, root, path)]
            if len(ok) != 1:
                errs.append("%s: must match exactly one alternative (matched %d)" % (path, len(ok)))
        return errs


def detect(doc):
    if isinstance(doc, list):
        return "findings"
    if isinstance(doc, dict):
        if "specialist_id" in doc:
            return "agent-result"
        if "tasks" in doc and "authorization" in doc:
            return "audit-run"
        if isinstance(doc.get("findings"), list):
            return "findings"
    return "finding"


def findings_of(doc, kind):
    if kind == "finding":
        return [("$", doc)]
    if kind == "agent-result":
        return [("$.candidates[%d]" % i, f) for i, f in enumerate(doc.get("candidates", []))]
    if kind == "findings":
        items = doc if isinstance(doc, list) else doc.get("findings", [])
        return [("$[%d]" % i, f) for i, f in enumerate(items)]
    return []


def inside(repo, rel):
    full = os.path.realpath(os.path.join(repo, rel))
    base = os.path.realpath(repo)
    return full if (full == base or full.startswith(base + os.sep)) else None


def norm_ws(s):
    return re.sub(r"\s+", " ", s).strip()


def invariants(doc, kind, repo, revision):
    errs, warns = [], []
    revs = []
    if isinstance(doc, dict) and "repository_revision" in doc:
        revs.append(("$", doc["repository_revision"]))
    for loc, f in findings_of(doc, kind):
        if not isinstance(f, dict):
            continue
        fid = f.get("id", loc)
        if "repository_revision" in f and f is not doc:
            revs.append((loc, f["repository_revision"]))
        ev_ids = {e.get("id") for e in f.get("evidence", []) if isinstance(e, dict)}
        if f.get("status") == "CONFIRMED":
            val = f.get("validation") or {}
            if val.get("independent_review") is not True:
                errs.append("%s (%s): CONFIRMED without independent review" % (loc, fid))
            missing = [r for r in val.get("checked_evidence_refs", []) if r not in ev_ids]
            if missing:
                errs.append("%s (%s): checked_evidence_refs not present in the finding: %s" % (loc, fid, missing))
        for j, e in enumerate(f.get("evidence", [])):
            if not isinstance(e, dict):
                continue
            eloc = "%s.evidence[%d]" % (loc, j)
            ls, le = e.get("line_start"), e.get("line_end")
            if isinstance(ls, int) and isinstance(le, int) and le < ls:
                errs.append("%s: line_end (%d) < line_start (%d)" % (eloc, le, ls))
            ex = e.get("excerpt_redacted") or ""
            for rx, what in SECRET_PATTERNS:
                if re.search(rx, ex):
                    errs.append("%s: excerpt seems to contain a %s in clear text; mask it before recording" % (eloc, what))
            if repo and e.get("path") and e.get("source_kind") in ("repository_code", "repository_config"):
                full = inside(repo, e["path"])
                if not full:
                    errs.append("%s: path escapes the snapshot: %s" % (eloc, e["path"]))
                    continue
                if not os.path.isfile(full):
                    errs.append("%s: file does not exist in the snapshot: %s" % (eloc, e["path"]))
                    continue
                with open(full, "rb") as fh:
                    raw = fh.read()
                lines = raw.decode("utf-8", errors="replace").splitlines()
                if isinstance(le, int) and le > len(lines):
                    errs.append("%s: lines %s-%s do not exist in %s (%d lines)" % (eloc, ls, le, e["path"], len(lines)))
                    continue
                if e.get("file_sha256") and hashlib.sha256(raw).hexdigest() != e["file_sha256"].lower():
                    errs.append("%s: file_sha256 does not match %s" % (eloc, e["path"]))
                if ex and isinstance(ls, int) and isinstance(le, int) and le >= ls and not MASK.search(ex):
                    if norm_ws(ex) not in norm_ws("\n".join(lines[ls - 1:le])):
                        warns.append("%s: excerpt does not appear in lines %d-%d of %s (check; it may have been summarized)" % (eloc, ls, le, e["path"]))
    if revision:
        for loc, r in revs:
            if r != revision:
                errs.append("%s: repository_revision %r differs from the audited revision %r" % (loc, r, revision))
    elif len({r for _, r in revs}) > 1:
        errs.append("different revisions in the same file: %s" % sorted({r for _, r in revs}))
    return errs, warns


def check_file(path, kind, repo, revision, validator):
    with open(path, encoding="utf-8") as f:
        doc = json.load(f)
    k = detect(doc) if kind == "auto" else kind
    errs = []
    if k == "findings":
        items = doc if isinstance(doc, list) else doc.get("findings", [])
        for i, item in enumerate(items):
            errs += [e.replace("$", "$[%d]" % i, 1) for e in validator.errors(item, validator.schemas["finding.schema.json"], validator.schemas["finding.schema.json"])]
    else:
        schema = validator.schemas[k + ".schema.json"]
        errs += validator.errors(doc, schema, schema)
    e2, w2 = invariants(doc, k, repo, revision)
    return k, errs + e2, w2


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+")
    ap.add_argument("--kind", default="auto", choices=["auto", "agent-result", "finding", "findings", "audit-run"])
    ap.add_argument("--repo", help="root of the audited snapshot, used to reopen the evidence")
    ap.add_argument("--revision", help="audited revision; every repository_revision must be equal")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    validator = Validator(load_schemas())
    if len(validator.schemas) < 3:
        print("Error: contracts not found in %s" % CONTRACTS)
        return 2
    if a.repo and not os.path.isdir(a.repo):
        print("Error: --repo is not a directory: %s" % a.repo)
        return 2
    report, total_err = [], 0
    for path in a.files:
        try:
            k, errs, warns = check_file(path, a.kind, a.repo, a.revision, validator)
        except (OSError, ValueError) as e:
            print("Error reading %s: %s" % (path, e))
            return 2
        total_err += len(errs)
        report.append({"arquivo": path, "tipo": k, "erros": errs, "avisos": warns})
    if a.json:
        print(json.dumps(report, ensure_ascii=False, indent=1))
    else:
        for r in report:
            print("%s [%s]: %s" % (r["arquivo"], r["tipo"], "OK" if not r["erros"] else "%d error(s)" % len(r["erros"])))
            for e in r["erros"]:
                print("  ERROR  " + e)
            for w in r["avisos"]:
                print("  WARNING " + w)
        print("\nGate G2: %s." % ("PASSED" if not total_err else "FAILED (%d error[s]); return it to the specialist or mark NOT_VERIFIED" % total_err))
    return 1 if total_err else 0


if __name__ == "__main__":
    sys.exit(main())
