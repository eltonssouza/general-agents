# -*- coding: utf-8 -*-
"""
sbr_common.py - utilities shared by the spring-boot-reference-expert scripts.

Source: "Spring Boot Reference Documentation, Version 2.7.18" (SBR). Page convention: N = PDF page
(printed = N - 20 for N >= 21). Stdlib only; no network; does not run anything from the target.

Contents:
- load_index(): loads scripts/sbr_index.json
- parse_properties(text) / parse_yaml(text): tolerant readers (subset) -> documents with flattened keys
- load_config_file(path): detects the type, splits into documents and returns a list of Doc
- KeyMatcher: matches keys (simplified relaxed binding) against the documented keys
"""
import difflib
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
INDEX_PATH = os.path.join(HERE, "sbr_index.json")
OFFSET = 20


def load_index(path=None):
    with open(path or INDEX_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def printed(pdf_page):
    return pdf_page - OFFSET if pdf_page >= 21 else None


def cite(pages):
    """formats '(SBR p.N)' with PDF pages."""
    if not pages:
        return ""
    ps = sorted(set(pages))
    return "(SBR p.%s)" % ",".join(str(p) for p in ps[:6])


# --------------------------------------------------------------------------------------
# Reading configuration files
# --------------------------------------------------------------------------------------
class Doc(object):
    def __init__(self, index, kind, source):
        self.index = index
        self.kind = kind            # 'properties' | 'yaml'
        self.source = source        # path
        self.items = []             # (key, value, lineno)
        self.issues = []            # (severity, id, line, message)
        self.activation = {}        # e.g. {'on-profile': 'prod'}
        self.start_line = 1

    def get(self, key):
        for k, v, _ in self.items:
            if k == key:
                return v
        return None

    def keys(self):
        return [k for k, _, _ in self.items]


def _strip_inline_comment(s):
    out = []
    q = None
    for i, ch in enumerate(s):
        if q:
            if ch == q:
                q = None
        elif ch in ("'", '"'):
            q = ch
        elif ch == "#" and (i == 0 or s[i - 1] in " \t"):
            break
        out.append(ch)
    return "".join(out).rstrip()


def _unquote(v):
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in ("'", '"'):
        return v[1:-1]
    return v


def parse_properties(text):
    """Splits into documents by '#---' or '!---' lines and returns a list of Doc."""
    docs = []
    cur = Doc(0, "properties", None)
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        raw = lines[i]
        lineno = i + 1
        i += 1
        s = raw.strip()
        if re.match(r"^\s+[#!]---\s*$", raw):
            cur.issues.append(("ALERT", "P13", lineno, "document separator with a leading space is not recognized (SBR p.100)"))
            continue
        if raw.startswith("#---") or raw.startswith("!---"):
            if raw.strip() in ("#---", "!---"):
                docs.append(cur)
                cur = Doc(len(docs), "properties", None)
                cur.start_line = lineno + 1
                continue
            cur.issues.append(("ALERT", "P13", lineno, "separator must have exactly three hyphens (SBR p.100)"))
            continue
        if not s or s[0] in "#!":
            continue
        while raw.rstrip().endswith("\\") and i < len(lines):
            raw = raw.rstrip()[:-1] + lines[i].strip()
            i += 1
        m = re.match(r"^\s*([^=:\s]+)\s*[=:]?\s*(.*)$", raw)
        if not m:
            continue
        key, val = m.group(1), m.group(2).strip()
        cur.items.append((key, val, lineno))
    docs.append(cur)
    for d in docs:
        _set_activation(d)
    return docs


def _set_activation(d):
    for k, v, _ in d.items:
        if k.startswith("spring.config.activate."):
            d.activation[k[len("spring.config.activate."):]] = v


def parse_yaml(text):
    """Tolerant YAML reader (subset: maps, lists, scalars, '---' documents, simple flow lists)."""
    raw_docs = []
    cur = []
    start = 1
    for n, line in enumerate(text.splitlines(), 1):
        if re.match(r"^---\s*(#.*)?$", line):
            if cur:
                raw_docs.append((start, cur))
            cur = []
            start = n + 1
            continue
        if re.match(r"^---\s+\S", line):  # '--- spring:' on the same line (PDF extraction)
            if cur:
                raw_docs.append((start, cur))
            cur = [(n, line[3:].lstrip())]
            start = n
            continue
        cur.append((n, line))
    if cur or not raw_docs:
        raw_docs.append((start, cur))
    docs = []
    for di, (start, lines) in enumerate(raw_docs):
        d = Doc(di, "yaml", None)
        d.start_line = start
        _parse_yaml_doc(lines, d)
        _set_activation(d)
        docs.append(d)
    return docs


def _parse_yaml_doc(lines, d):
    stack = []  # (indent, path_list, is_list_container, list_counter)
    block_indent = None
    for lineno, raw in lines:
        if "\t" in raw[: len(raw) - len(raw.lstrip())]:
            d.issues.append(("ERROR", "P04", lineno, "tab in the indentation: YAML does not accept tabs"))
            continue
        line = _strip_inline_comment(raw)
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(" "))
        if block_indent is not None:
            if indent > block_indent:
                continue
            block_indent = None
        s = line.strip()
        is_item = s.startswith("- ") or s == "-"
        # closes levels (list items may have the same indentation as the parent key)
        if is_item:
            while stack and indent < stack[-1][0]:
                stack.pop()
        else:
            while stack and indent <= stack[-1][0]:
                stack.pop()
        if is_item:
            body = s[2:].strip() if s != "-" else ""
            # list container: uses the parent path
            if stack and stack[-1][2] and stack[-1][0] == indent:
                cont = stack[-1]
            else:
                parent_path = stack[-1][1] if stack else []
                cont = [indent, parent_path, True, 0]
                stack.append(cont)
            idx = cont[3]
            cont[3] += 1
            path = cont[1] + ["[%d]" % idx]
            if not body:
                continue
            m = re.match(r"^([^\s:'\"][^:]*?|\"[^\"]*\"|'[^']*')\s*:(?:\s+(.*))?$", body)
            if m and not body.startswith(("{", "[")):
                k = _unquote(m.group(1))
                v = m.group(2)
                sub_indent = indent + 2
                stack.append([sub_indent - 1, path, False, 0])
                _emit(d, path + [k], v, lineno, stack, sub_indent - 1)
            else:
                _add_item(d, path, _unquote(_strip_inline_comment(body)), lineno)
            continue
        m = re.match(r"^(\"[^\"]*\"|'[^']*'|[^\s:#][^:]*?)\s*:(?:\s+(.*))?$", s)
        if not m:
            d.issues.append(("INFO", "P00", lineno, "line not interpreted by the simplified reader: %r" % s[:60]))
            continue
        k = _unquote(m.group(1))
        v = m.group(2)
        parent_path = stack[-1][1] if stack else []
        # if the parent is a list container, the path already includes the index
        _emit(d, parent_path + [k], v, lineno, stack, indent)
        if v is not None and v.strip() in ("|", ">", "|-", ">-", "|+", ">+"):
            block_indent = indent


def _emit(d, path, v, lineno, stack, indent):
    if v is None or v.strip() == "":
        stack.append([indent, path, False, 0])
        return
    v = v.strip()
    if v in ("|", ">", "|-", ">-", "|+", ">+"):
        _add_item(d, path, "", lineno)
        return
    if v.startswith("*") and not v.startswith(("*\"", "*'")):
        d.issues.append(("ERROR", "P05", lineno, "unquoted '*' value in YAML is an alias, invalid; use quotes (SBR p.445)"))
    if v.startswith("[") and v.endswith("]"):
        inner = v[1:-1]
        parts = [_unquote(x) for x in inner.split(",") if x.strip()]
        for i, x in enumerate(parts):
            _add_item(d, path + ["[%d]" % i], x, lineno)
        return
    _add_item(d, path, _unquote(v), lineno)


def _add_item(d, path, value, lineno):
    key = ""
    for seg in path:
        if seg.startswith("["):
            key += seg
        else:
            key += ("." if key else "") + seg
    d.items.append((key, value, lineno))


def load_config_file(path):
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()
    low = path.lower()
    if low.endswith((".yml", ".yaml")):
        docs = parse_yaml(text)
    else:
        docs = parse_properties(text)
    for d in docs:
        d.source = path
    return docs


def profile_from_filename(path):
    base = os.path.basename(path)
    m = re.match(r"^application-(.+)\.(properties|ya?ml)$", base)
    return m.group(1) if m else None


# --------------------------------------------------------------------------------------
# Key matching
# --------------------------------------------------------------------------------------
def _norm_seg(seg):
    return re.sub(r"[-_]", "", seg.lower())


def norm_key(k):
    k = re.sub(r"\[[^\]]*\]", "", k)  # removes map indexes/brackets
    return ".".join(_norm_seg(s) for s in k.split(".") if s != "")


class KeyMatcher(object):
    def __init__(self, index):
        self.index = index
        self.exact = {}      # norm -> canonical
        self.wild = []       # (prefix_norm, canonical)   [trailing wildcard '*' from Appendix A or curated dynamic prefixes]
        self.templates = []  # (list of normalized segments with None = any, canonical)
        for k, v in index["props"].items():
            self._add(k, bool(v.get("apendice_a")))
        # dynamic prefixes documented in the text (free-form maps)
        for p in ("spring.jpa.properties", "spring.kafka.properties", "spring.kafka.admin.properties",
                  "spring.kafka.consumer.properties", "spring.kafka.producer.properties", "spring.kafka.streams.properties",
                  "spring.mail.properties", "spring.activemq.properties", "spring.quartz.properties",
                  "management.metrics.tags", "management.metrics.enable", "management.metrics.distribution",
                  "logging.level", "logging.group", "info", "spring.profiles.group", "spring.application.json",
                  "management.endpoint.jolokia.config", "management.metrics.export.humio.tags",
                  "spring.security.oauth2.client.registration", "spring.security.oauth2.client.provider",
                  "spring.security.saml2.relyingparty.registration", "management.endpoints.web.path-mapping",
                  "spring.mvc.contentnegotiation.media-types", "spring.datasource.hikari",
                  "spring.datasource.tomcat", "spring.datasource.dbcp2", "spring.datasource.oracleucp"):
            self.wild.append((norm_key(p), p + ".*"))

    def _add(self, k, from_appendix):
        if "[" in k:
            return  # examples with an index/map key; the curated dynamic prefixes cover these cases
        if "*" in k or "<" in k:
            segs = k.split(".")
            if segs[-1] in ("*",) and not any(("<" in x or "*" in x) for x in segs[:-1]):
                if from_appendix:
                    pre = ".".join(segs[:-1])
                    if pre:
                        self.wild.append((norm_key(pre), k))
                return
            tpl = []
            for sg in segs:
                if "<" in sg or sg == "*":
                    tpl.append(None)
                else:
                    tpl.append(norm_key(sg) if sg else "")
            self.templates.append((tpl, k))
            return
        self.exact.setdefault(norm_key(k), k)

    def match(self, key):
        n = norm_key(key)
        if n in self.exact:
            return self.exact[n], "exact"
        for pre, canon in self.wild:
            if n == pre or n.startswith(pre + "."):
                return canon, "prefix"
        segs = n.split(".")
        for tpl, canon in self.templates:
            if tpl[-1] is None:       # trailing wildcard inside a template (e.g. a.<id>.*)
                if len(segs) >= len(tpl) and all(t is None or t == s for t, s in zip(tpl[:-1], segs)):
                    return canon, "template"
            elif len(segs) == len(tpl) and all(t is None or t == s for t, s in zip(tpl, segs)):
                return canon, "template"
        return None, None

    def suggest(self, key, n=3):
        parts = key.split(".")
        head = ".".join(parts[:2]) if len(parts) > 2 else parts[0]
        pool = [k for k in self.exact.values() if k.startswith(head)]
        if not pool:
            pool = list(self.exact.values())
        return difflib.get_close_matches(key, pool, n=n, cutoff=0.85)


ADDITIONAL_PATH_KEY = re.compile(r"^management\.endpoint\.health\.group\.([^.\[\]]+)\.additional-path$")


def check_additional_path(value):
    """Rule P19 (SBR p.462): health group additional-path = MANDATORY prefix `server:` (main port) or
    `management:` (management port, if configured) + path of a SINGLE segment. Returns None if compliant, or
    (severity, message). Accepts the value with or without quotes."""
    v = (value or "").strip().strip("\"'").strip()
    m = re.match(r"^([A-Za-z]+):(.*)$", v)
    if not m:
        return "ERROR", "no prefix: the `server:` or `management:` prefix is mandatory (e.g. server:/healthz) (SBR p.462)"
    pre, path = m.group(1), m.group(2)
    if pre not in ("server", "management"):
        return "ERROR", "invalid prefix '%s:': only `server:` (main port) or `management:` (management port) (SBR p.462)" % pre
    segs = [s for s in path.split("/") if s]
    if not segs:
        return "ERROR", "empty path after the prefix: provide one segment, e.g. %s:/healthz (SBR p.462)" % pre
    if len(segs) > 1:
        return "ERROR", "the path must be a single segment (here %d: %s); e.g. %s:/%s (SBR p.462)" % (len(segs), "/".join(segs), pre, segs[0])
    if not path.startswith("/") or path.endswith("/"):
        return "ALERT", "[inference] the book only exemplifies `%s:/segment` (leading slash, no trailing slash); the form '%s' is not exemplified (SBR p.462)" % (pre, v)
    return None
