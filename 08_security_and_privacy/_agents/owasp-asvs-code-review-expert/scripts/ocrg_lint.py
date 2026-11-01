# -*- coding: utf-8 -*-
"""
ocrg_lint.py - SIMPLE STATIC linter for code snippets, based on the patterns the OWASP Code Review Guide v2.0
(OCRG) actually documents. It does NOT execute the analyzed code, does not use the network, and only reads files/stdin.
Standard library only. Run with `python -I`.

Usage:
  python -I scripts/ocrg_lint.py FILE_OR_FOLDER [...]            # text
  python -I scripts/ocrg_lint.py - < snippet.java                 # stdin (unknown language: applies all rules)
  python -I scripts/ocrg_lint.py src --format json --fail-on red_flag
  python -I scripts/ocrg_lint.py --rules                         # list the rules (id, class, origin, pages)
  python -I scripts/ocrg_lint.py --explain SQL-CONCAT           # detail of one rule
  options: --include-info (tracing/crawling points), --include-extrapolation (rules beyond the OCRG), --lang java|dotnet|php|js|c|python|asp|xml,
          --include-comments

Each finding carries: rule, class, ORIGIN, and page.
  class red_flag = the book calls it a red flag / says "never", "must not be used" or shows it as a bad example;
  class verify   = the book tells the reviewer to CHECK (heuristic; requires human judgment; legacy alias: verificar);
  class info     = tracing point (crawling/source-sink) - only appears with --include-info.
  ORIGIN [from source] = the pattern is documented on the cited OCRG page (PDF page; printed = PDF - 1);
  [inference]          = the regex is a package heuristic for a pattern the book describes in prose;
  [extrapolation]      = rule BEYOND the OCRG (e.g. an ASVS requirement or general practice) - off by default.
Limits: per-line matching (regex); no flow analysis; false positives and negatives are expected. The book states that
tools always need human verification (OCRG p.11). It does not replace review, a real SAST, or security testing.
The package does NOT provide exploit payloads; the messages point to the fix.
"""
import argparse
import json
import os
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

MAX_BYTES = 2_000_000
EXT_LANG = {
    ".java": "java", ".jsp": "java", ".jspx": "java", ".cs": "dotnet", ".vb": "dotnet", ".aspx": "dotnet", ".ascx": "dotnet",
    ".cshtml": "dotnet", ".asax": "dotnet", ".config": "dotnet", ".php": "php", ".js": "js", ".mjs": "js", ".ts": "js",
    ".html": "js", ".htm": "js", ".c": "c", ".h": "c", ".cpp": "c", ".cc": "c", ".cxx": "c", ".hpp": "c", ".py": "python",
    ".asp": "asp", ".xml": "xml",
}
ALL = None

# (id, class, origin, OCRG pages (PDF), asvs [inference], langs, regex, flags, message, note)
def R(id, cls, origin, pages, asvs, langs, rx, msg, note="", flags=re.I):
    return {"id": id, "class": cls, "origin": origin, "pages": pages, "asvs": asvs, "langs": langs,
            "rx": re.compile(rx, flags), "msg": msg, "note": note}


SQLKW = r"(?:select\b[^;\n]*\bfrom\b|insert\s+into\b|update\b[^;\n]*\bset\b|delete\s+from\b|exec(?:ute)?\s+\w+)"

RULES = [
    R("SQL-CONCAT", "red_flag", "[from source]", [45, 49, 50, 51], ["5.3.4"], ALL,
      r"(?=.*" + SQLKW + r")(?:.*[\"'`]\s*[+&.]\s*[$\w(@]|.*[$\w)\]]\s*[+&]\s*[\"'`])",
      "SQL built by concatenating a variable value: the parser cannot tell code from data. Use a parameterized query/framework API (OCRG p.45-46, 51).",
      "False positive if the concatenated part is an internal constant (fixed name) - confirm the origin."),
    R("SQL-PHP-CONCAT", "red_flag", "[from source]", [48], ["5.3.4"], ("php", None),
      r"(?=.*" + SQLKW + r").*[\"']\s*\.\s*\$\w+",
      "PHP query concatenating a variable (Sample 7.5 of the book). Use PDO/parameterized queries (OCRG p.48, 52)."),
    R("PHP-ESCAPE-FUNCS", "verify", "[from source]", [49], ["5.3.5"], ("php", None),
      r"\b(?:addslashes|mysql_real_escape_string)\s*\(",
      "addslashes()/mysql_real_escape_string() only protect if the value is quoted in the query; the book shows cases that are still vulnerable (OCRG p.49). Prefer parameterization. [DATED] the mysql_* extension is legacy."),
    R("HQL-CONCAT", "red_flag", "[from source]", [51, 53], ["5.3.4"], ("java", "dotnet", None),
      r"\bcreate(?:sql)?query\s*\(\s*[\"'][^\"']*[\"']\s*\+|\bCreateSQLQuery\s*\(\s*\w+\s*\)",
      "ORM/HQL is not immune to injection: concatenation in HQL/native SQL. Use parameterized HQL or the Criteria API (OCRG p.51, 53).",
      "CreateSQLQuery(var): confirm whether 'var' was built by concatenation (Bad .Net Code Example, OCRG p.53)."),
    R("SQL-EXEC", "verify", "[from source]", [51, 207], ["5.3.4"], ALL,
      r"\b(?:exec|execute)\s+(?:sp_|xp_|@)",
      "EXEC/EXECUTE call: the book says to review all code that calls EXEC/EXECUTE and SQL that reaches external resources/the command line (OCRG p.51)."),
    R("JS-EVAL", "red_flag", "[from source]", [52, 76, 191], ["5.2.4", "5.3.6", "5.5.4"], ("js", "unknown", None),
      r"\beval\s*\(",
      "eval(): a 'red flag' for the reviewer, especially for JSON (use JSON.parse); even escaping the data is not safe (OCRG p.52, 76, 191)."),
    R("JS-NEW-FUNCTION", "verify", "[from source]", [191], ["5.2.4"], ("js", None),
      r"\bnew\s+Function\s*\(",
      "new Function()/eval create dynamic execution risk; do not use for JSON (OCRG p.191)."),
    R("JS-HTML-SINK", "verify", "[from source]", [52, 72, 76, 155, 190, 191], ["5.3.3"], ("js", None),
      r"\.innerHTML\s*=|\bdocument\.write(?:ln)?\s*\(|\$\([^)]*\)\.html\s*\(\s*[^)\s]",
      "HTML/DOM sink: untrusted data must enter via textContent/createTextNode, not innerHTML/document.write/.html() (OCRG p.52, 72, 76, 155, 190-191)."),
    R("JS-TIMER-STRING", "red_flag", "[from source]", [76], ["5.2.4"], ("js", None),
      r"\bset(?:Interval|Timeout)\s*\(\s*[\"'`]",
      "setInterval/setTimeout with a string is a code sink: the book shows that even escaping the data there is XSS (OCRG p.76)."),
    R("JS-POSTMESSAGE-STAR", "verify", "[from source]", [155], ["14.5.2"], ("js", None),
      r"\.postMessage\s*\([^)]*,\s*[\"']\*[\"']\s*\)",
      "postMessage with origin '*': pass the expected origin as the 2nd argument (OCRG p.155)."),
    R("JS-ORIGIN-INDEXOF", "red_flag", "[from source]", [155], ["14.5.2"], ("js", None),
      r"\.or(?:i)?gin\s*\.\s*indexOf\s*\(",
      "Origin check via indexOf is 'very insecure' (www.owasp.org.attacker.com matches); compare the exact FQDN (OCRG p.155)."),
    R("CORS-WILDCARD", "verify", "[from source]", [156], ["14.5.3"], ALL,
      r"Access-Control-Allow-Origin[\"']?\s*[:=,(]\s*[\"']?\s*\*",
      "Access-Control-Allow-Origin '*': not for URLs with sensitive content; use a domain whitelist (OCRG p.156)."),
    R("CORS-REFLECT-ORIGIN", "verify", "[from source]", [156], ["14.5.3"], ALL,
      r"Access-Control-Allow-Origin[^\n]*(?:getHeader\(\s*[\"']Origin|headers\[[\"']Origin|request\.origin|\$_SERVER\[[\"']HTTP_ORIGIN)",
      "Echoing the Origin header without a check is equivalent to allowing any domain; use a whitelist (OCRG p.156)."),
    R("WEBSOCKET-WS", "verify", "[from source]", [157], ["9.1.1"], ("js", None),
      r"[\"'`]ws://",
      "Cleartext ws:// endpoint: use wss:// (OCRG p.157). Note: the book's own Sample 17.1 uses ws:// as an example."),
    R("REDIRECT-JAVA-PARAM", "red_flag", "[from source]", [152], ["5.1.5"], ("java", None),
      r"sendRedirect\s*\(\s*request\.getParameter",
      "Redirect whose destination comes from the request (Sample 16.1): use a whitelist or a relative path (OCRG p.151-152)."),
    R("REDIRECT-DOTNET-VAR", "verify", "[from source]", [152], ["5.1.5"], ("dotnet", None),
      r"Response\.Redirect\s*\(\s*(?!\s*[\"'])\w[\w.\[\]\"]*\s*\)",
      "Response.Redirect(variable): confirm the destination does not come from user input (Sample 16.3); whitelist/relative (OCRG p.152)."),
    R("REDIRECT-PHP-LOCATION", "verify", "[from source]", [152], ["5.1.5"], ("php", None),
      r"header\s*\(\s*[\"']Location:\s*[\"']\s*\.\s*\$",
      "header('Location: '.$var): destination possibly user-controlled (Sample 16.2); whitelist/relative (OCRG p.152)."),
    R("REDIRECT-NO-RETURN", "info", "[from source]", [153], [], ("java", None),
      r"\bsendRedirect\s*\(|\.forward\s*\(",
      "sendRedirect()/forward() do not stop execution: confirm there is a 'return' right after (OCRG p.153)."),
    R("ERR-PRINTSTACK-OUT", "red_flag", "[from source]", [167], ["7.4.1"], ("java", None),
      r"printStackTrace\s*\(\s*out\s*\)",
      "printStackTrace(out) returns the stack trace to the browser (leak); log it and show a generic message (OCRG p.167)."),
    R("ERR-PRINTSTACK", "verify", "[from source]", [167], ["7.4.1"], ("java", None),
      r"\.printStackTrace\s*\(\s*\)",
      "printStackTrace()/getStackTrace(): confirm the output does not reach the client; use log + generic message (OCRG p.167)."),
    R("ERR-CATCH-ALL", "verify", "[from source]", [165, 173], ["7.4.2"], ALL,
      r"catch\s*\(\s*(?:final\s+)?(?:java\.lang\.|System\.)?(?:Exception|Throwable|Error)\s+\w+\s*\)|catch\s*\(\s*\.\.\.\s*\)",
      "Generic catch (Exception/Throwable/catch(...)) should be avoided: catch specific types and handle them (OCRG p.165, 173).",
      "Acceptable in a central 'last resort' handler (ASVS V7.4.3), never to swallow errors."),
    R("ERR-SWALLOW", "verify", "[from source]", [115], ["7.4.2"], ALL,
      r"catch\s*(?:\([^)]*\))?\s*\{\s*\}",
      "Empty catch: the book says to identify code that swallows exceptions (OCRG p.115); log and handle."),
    R("ERR-RESPONSE-WRITE-LASTERROR", "red_flag", "[from source]", [169], ["7.4.1"], ("dotnet", None),
      r"Response\.Write\s*\([^)]*(?:GetLastError|StackTrace|Request\.Url)|GetLastError\(\)\.(?:ToString|StackTrace)",
      "Showing the error/stack trace/URL in the response is a bad example (Sample 20.6): it leaks details and opens XSS; use a generic error page (OCRG p.169)."),
    R("CFG-CUSTOMERRORS-OFF", "verify", "[from source]", [170], ["7.4.1"], ("dotnet", "xml", None),
      r"customErrors\s+mode\s*=\s*[\"']Off[\"']",
      "customErrors mode=Off shows detailed errors; use On or RemoteOnly (OCRG p.170)."),
    R("CFG-DEBUG-TRACE", "verify", "[from source]", [116, 210], ["14.3.2"], ("dotnet", "xml", None),
      r"<compilation\b[^>]*\bdebug\s*=\s*[\"']true[\"']|<trace\b[^>]*\benabled\s*=\s*[\"']true[\"']",
      "Compilation debug/trace enabled: FxCop rules DebugCompilationMustBeDisabled and TraceShouldBeDisabled (OCRG p.116)."),
    R("CFG-FORMS-CREDENTIALS", "red_flag", "[from source]", [95, 114, 116], ["2.10.4"], ("dotnet", "xml", None),
      r"passwordFormat\s*=\s*[\"']Clear[\"']|<\s*credentials\b",
      "Credentials in web.config/forms (the book itself says not to use <credentials> in production; OCRG p.114, 116). Keep secrets out of code/cleartext config."),
    R("CFG-COOKIE-FLAGS", "verify", "[from source]", [116, 121], ["3.4.1", "3.4.2"], ("dotnet", "xml", None),
      r"requireSSL\s*=\s*[\"']false[\"']|httpOnlyCookies\s*=\s*[\"']false[\"']|\bsetHttpOnly\s*\(\s*false\s*\)",
      "Cookie without Secure/HttpOnly: use requireSSL/httpOnlyCookies=true (FxCop, OCRG p.116; 'secure' and 'http-only' flags in OCRG p.121)."),
    R("CFG-VALIDATE-REQUEST-OFF", "red_flag", "[from source]", [73, 116], ["5.3.3"], ("dotnet", "xml", None),
      r"validateRequest\s*=\s*[\"']false[\"']|requestValidationMode\s*=\s*[\"']2\.0[\"']|enableViewStateMac\s*=\s*[\"']false[\"']",
      "Request validation/ViewState MAC turned off: the reviewer must ensure they are never turned off without justification (OCRG p.73, 116)."),
    R("CFG-SESSION-URL", "verify", "[from source]", [68, 70], ["3.1.1"], ("dotnet", "xml", "php", None),
      r"cookieless\s*=\s*[\"']?(?:true|UseUri)|use_trans_sid\s*=\s*1",
      "Cookieless session (ID in the URL): the book says IDs go in cookies, not in the URL (OCRG p.69-70). Note: the book's own Sample 8.5 uses cookieless=\"true\" (OCRG p.68)."),
    R("CFG-LOGIN-HTTP", "verify", "[from source]", [60], ["9.1.1"], ("js", "dotnet", "java", "php", None),
      r"<form\b[^>]*\baction\s*=\s*[\"']http://",
      "Form submitting to http://: the login page and the submit must be TLS-only (OCRG p.60, 121)."),
    R("LOG-PASSWORD", "verify", "[inference]", [61, 163, 209], ["7.1.1"], ALL,
      r"\b(?:log\w*|logger\w*|console\.writeline|system\.out\.print\w*|trace\.write\w*|debug\.write\w*|syslog|printf)\b[^\n]*\b(?:passw(?:or)?d|pswd|pwd)\b",
      "Possible password logging: the book says not to log passwords (valid or invalid), session IDs, keys, and connection strings (OCRG p.61, 163, 209)."),
    R("CRYPTO-DES", "red_flag", "[from source]", [124], ["6.2.5"], ALL,
      r"getInstance\s*\(\s*[\"']DES(?:/|[\"'])|\bDESCryptoServiceProvider\b|\bnew\s+DES\b",
      "DES and SHA-0 are insecure and must not be used (the book's Sample 12.1 is the bad example); use a strong approved algorithm (OCRG p.124)."),
    R("CRYPTO-MD5-SHA1", "red_flag", "[from source]", [124, 130], ["6.2.5"], ALL,
      r"getInstance\s*\(\s*[\"'](?:MD5|SHA-?1)[\"']|\bMD5(?:CryptoServiceProvider|Managed)?\b\s*(?:\.Create|\(|\.new)|\bSHA1(?:CryptoServiceProvider|Managed|Cng)?\b\s*(?:\.Create|\(|\.new)|hashlib\.(?:md5|sha1)\b|\bmd5\s*\(|\bsha1\s*\(",
      "MD5/SHA-1: the reviewer must raise a red flag and assess the risk of the use (OCRG p.130; avoid in new applications, p.124, 130). [DATED] current practice also avoids them for integrity/signatures."),
    R("CRYPTO-RC2-RANDOM", "verify", "[from source]", [124, 210], ["6.3.1"], ("java", "dotnet", None),
      r"\bRC2\b|\bnew\s+Random\s*\(|\bSystem\.Random\b|\bjava\.util\.Random\b",
      "RC2 / non-cryptographic PRNG: the book says to use SecureRandom/RNGCryptoServiceProvider for unpredictable values and to check the key size (OCRG p.123-124, 210)."),
    R("SECRET-IN-CODE", "verify", "[inference]", [105, 199], ["2.10.4", "6.4.1"], ALL,
      r"\b(?:passw(?:or)?d|pwd|secret|api[_-]?key|private[_-]?key|client[_-]?secret)\b\s*[:=]\s*[\"'][^\"'\s]{4,}[\"']",
      "Possible secret in code: the book lists 'Keys are not held in code' (checklist, OCRG p.199) and says to protect connection strings (p.105)."),
    R("AC-ALLOW-ANONYMOUS", "info", "[from source]", [137, 138], ["4.1.1"], ("dotnet", None),
      r"\[AllowAnonymous\]",
      "AllowAnonymous: confirm it only covers public pages (login/registration) under 'default deny' (OCRG p.137-138)."),
    R("BIND-UPDATEMODEL", "verify", "[from source]", [82], ["5.1.2"], ("dotnet", None),
      r"\b(?:Try)?UpdateModel\s*\(",
      "UpdateModel/mass assignment: use a model without forbidden fields, Bind with a whitelist, or exclude attributes (OCRG p.81-82)."),
    R("XSS-ECHO-REQUEST", "verify", "[from source]", [72, 212], ["5.3.3"], ALL,
      r"Response\.Write\s*\(\s*Request|<%=\s*request\.getParameter|\bout\.print(?:ln)?\s*\(\s*request\.getParameter|getWriter\(\)\.(?:print|println|write)\s*\(\s*request\.getParameter",
      "Request input going straight to the HTML output: apply context-aware encoding (OCRG p.72, 212)."),
    R("C-UNSAFE-STR", "verify", "[from source]", [185], ["5.4.1"], ("c", None),
      r"\b(?:strcpy|strcat|sprintf|vsprintf|gets)\s*\(",
      "C function without bounds checking: use strncpy/strncat/snprintf/fgets or the _s variants and validate the size (OCRG p.185)."),
    R("C-SCANF", "verify", "[from source]", [185], ["5.4.1"], ("c", None),
      r"\b(?:scanf|fscanf|sscanf)\s*\(",
      "The scanf family can cause buffer overflow (OCRG p.185); limit the fields."),
    R("C-FORMAT-STRING", "verify", "[from source]", [186, 187], ["5.4.2"], ("c", None),
      r"\b(?:printf|syslog)\s*\(\s*[A-Za-z_]\w*\s*[,)]|\b(?:fprintf|snprintf)\s*\(\s*\w+\s*,\s*(?:\w+\s*,\s*)?[A-Za-z_]\w*\s*[,)]",
      "Non-literal format string: user data as the format allows reading/writing via %x/%s/%n (OCRG p.186-187); use a constant format."),
    R("JNI-PUBLIC-NATIVE", "verify", "[from source]", [57], ["5.4.1"], ("java", None),
      r"\bpublic\b[^;{]*\bnative\b",
      "Public native method: declare it private and expose it through a wrapper that validates input (Sample 7.13; OCRG p.57)."),
    R("THREAD-STATIC-STATE", "verify", "[inference]", [183], ["1.11.2"], ("java", "dotnet", None),
      r"\bstatic\b[^;(=]*?\w*(?:session|user|request|token|principal)\w*\s*(?:=|;)",
      "Static state holding request/user data: do not keep one request's data in static members; static state must be thread-safe (OCRG p.183)."),
    R("SERIALIZATION-CRAWL", "verify", "[from source]", [210, 211], ["5.5.1", "5.5.3"], ("java", "dotnet", None),
      r"\bObjectInputStream\b|\bBinaryFormatter\b|\breadObject\s*\(|\bGetObjectData\b",
      "Crawling tracing point (serialization/input streams): treat as untrusted input (OCRG p.210-211; ASVS V5.5.1/V5.5.3 [inference])."),
    R("OS-COMMAND-CRAWL", "verify", "[from source]", [214, 217], ["5.3.8"], ("java", "c", None),
      r"\bRuntime\.(?:getRuntime\(\)\.)?exec\s*\(|\bpopen\s*\(|(?<![\w.])system\s*\(",
      "OS call: in the book's crawling this is a command/OS injection point; never build a command with unvalidated input (OCRG p.214, 217)."),
    R("HEADER-SPLITTING", "verify", "[from source]", [212], ["5.3.1"], ("java", None),
      r"\bset(?:Header|Status)\s*\([^)]*getParameter",
      "Request data in a response header: sanitize CR/LF (response splitting; OCRG p.212)."),
    R("JS-DOM-SOURCE", "info", "[from source]", [190, 191], ["5.3.3"], ("js", None),
      r"\bdocument\.(?:URL|location|referrer)\b|\bwindow\.location\b|\blocation\.(?:hash|search)\b",
      "Attacker-controllable source in the DOM: trace it to sinks (document.write, innerHTML, location.href) - taint (OCRG p.190-191)."),
    R("THREADING-CRAWL", "info", "[from source]", [182, 183], ["1.11.2"], ("java", "dotnet", None),
      r"\bsynchronized\b|System\.Threading|\bThreadPool\b|\bnew\s+Thread\s*\(",
      "Multithreaded code: look for race conditions and locks outside finally (OCRG p.182-183)."),
    R("ASP-ON-ERROR-RESUME", "verify", "[from source]", [168, 215], ["7.4.2"], ("asp", None),
      r"On\s+Error\s+Resume\s+Next",
      "Classic ASP: 'On Error Resume Next' without handling err is prone to design errors and leaks (OCRG p.168, 215)."),
    # ---- BEYOND THE OCRG ([extrapolation]); off by default ----
    R("X-PY-UNSAFE-DESERIALIZE", "verify", "[extrapolation]", [], ["5.5.3"], ("python", None),
      r"\bpickle\.loads?\s*\(|\byaml\.load\s*\((?![^)]*Loader\s*=\s*(?:yaml\.)?SafeLoader)",
      "[extrapolation] Insecure deserialization (ASVS V5.5.3, p.41). The OCRG only lists ObjectInputStream/Serializable as crawling points."),
    R("X-XML-PARSER-XXE", "verify", "[extrapolation]", [], ["5.5.2"], ("java", "dotnet", "python", None),
      r"\b(?:DocumentBuilderFactory|SAXParserFactory|XMLInputFactory|XmlDocument|XmlTextReader|etree\.XMLParser)\b",
      "[extrapolation] XML parser: confirm a restrictive config without external entities (ASVS V5.5.2, p.41). The OCRG only mentions XXE in reference links (p.51)."),
    R("X-TLS-VERIFY-OFF", "verify", "[extrapolation]", [], ["9.2.1", "1.9.2"], ALL,
      r"\bverify\s*=\s*False\b|TrustAllCerts|ServerCertificateValidationCallback\s*\+?=[^;\n]*true|ALLOW_ALL_HOSTNAME_VERIFIER|rejectUnauthorized\s*:\s*false",
      "[extrapolation] TLS certificate verification turned off (ASVS V9.2.1 p.51; V1.9.2 p.20). Not documented as a pattern by the OCRG."),
    R("X-WEAK-RANDOM-JS", "verify", "[extrapolation]", [], ["6.3.1"], ("js", None),
      r"\bMath\.random\s*\(",
      "[extrapolation] Math.random is not a CSPRNG; for unpredictable values use the cryptographic generator (ASVS V6.3.1 p.43)."),
    R("X-SHELL-TRUE", "verify", "[extrapolation]", [], ["5.3.8"], ("python", None),
      r"subprocess\.\w+\([^)]*shell\s*=\s*True|\bos\.system\s*\(",
      "[extrapolation] Execution via shell (ASVS V5.3.8 p.40). The OCRG only documents Runtime.exec/system/popen as crawling points."),
]
RULE_BY_ID = {r["id"]: r for r in RULES}


def lang_of(path, override=None):
    if override:
        return override
    if path == "-":
        return "unknown"
    return EXT_LANG.get(os.path.splitext(path)[1].lower(), "unknown")


def applies(rule, lang):
    ls = rule["langs"]
    if ls is None:
        return True
    return lang in ls or (lang == "unknown" and (None in ls or "unknown" in ls))


def is_comment(line):
    s = line.strip()
    return s.startswith(("//", "#", "*", "/*", "--", "<!--")) or (s.startswith("'") and len(s) > 1 and s[1] == " ")


def lint_text(text, path="-", lang="unknown", include_info=False, include_extra=False, include_comments=False):
    out = []
    for ln, line in enumerate(text.splitlines(), 1):
        if not include_comments and is_comment(line):
            continue
        if len(line) > 2000:
            line = line[:2000]
        for r in RULES:
            if r["class"] == "info" and not include_info:
                continue
            if r["origin"] == "[extrapolation]" and not include_extra:
                continue
            if not applies(r, lang):
                continue
            if r["rx"].search(line):
                out.append({"file": path, "line": ln, "rule": r["id"], "class": r["class"], "origin": r["origin"],
                            "ocrg_pages": r["pages"], "asvs_inference": ["V" + a for a in r["asvs"]],
                            "message": r["msg"], "note": r["note"], "snippet": line.strip()[:200]})
    return out


def iter_files(paths):
    for p in paths:
        if p == "-":
            yield "-"
        elif os.path.isdir(p):
            for root, dirs, files in os.walk(p):
                dirs[:] = [d for d in dirs if d not in (".git", "node_modules", "__pycache__", ".venv", "bin", "obj")]
                for f in sorted(files):
                    if os.path.splitext(f)[1].lower() in EXT_LANG:
                        yield os.path.join(root, f)
        else:
            yield p


def fmt_pages(pgs):
    return ("OCRG p." + ",".join(str(x) for x in pgs)) if pgs else "no OCRG page"


def main():
    ap = argparse.ArgumentParser(description="Simple snippet linter based on the patterns of the OCRG v2.0")
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--format", choices=("text", "json", "md"), default="text")
    ap.add_argument("--include-info", action="store_true")
    ap.add_argument("--include-extrapolation", action="store_true")
    ap.add_argument("--include-comments", action="store_true")
    ap.add_argument("--lang")
    ap.add_argument("--fail-on", choices=("red_flag", "verify", "verificar"), help="exit 1 on findings of this class (verificar = legacy alias of verify)")
    ap.add_argument("--rules", action="store_true")
    ap.add_argument("--explain", metavar="RULE")
    a = ap.parse_args()
    if a.fail_on == "verificar":
        a.fail_on = "verify"

    if a.rules:
        for r in RULES:
            print("%-28s %-9s %-14s %s" % (r["id"], r["class"], r["origin"], fmt_pages(r["pages"])))
        print("\nTotal: %d rules (%d from source/inference, %d extrapolation)" % (
            len(RULES), sum(1 for r in RULES if r["origin"] != "[extrapolation]"), sum(1 for r in RULES if r["origin"] == "[extrapolation]")))
        return
    if a.explain:
        r = RULE_BY_ID.get(a.explain.upper())
        if not r:
            sys.exit("unknown rule: %s" % a.explain)
        print("%s | class %s | origin %s | %s | related ASVS [inference]: %s" % (
            r["id"], r["class"], r["origin"], fmt_pages(r["pages"]), ", ".join("V" + x for x in r["asvs"]) or "-"))
        print("regex: " + r["rx"].pattern)
        print(r["msg"])
        if r["note"]:
            print("note: " + r["note"])
        return
    if not a.paths:
        ap.print_help()
        return
    findings = []
    for p in iter_files(a.paths):
        try:
            if p == "-":
                text = sys.stdin.read()
            else:
                if os.path.getsize(p) > MAX_BYTES:
                    print("skipped (too large): %s" % p, file=sys.stderr)
                    continue
                with open(p, "rb") as f:
                    raw = f.read()
                if b"\x00" in raw[:4096]:
                    continue
                text = raw.decode("utf-8", errors="replace")
        except OSError as e:
            print("error reading %s: %s" % (p, e), file=sys.stderr)
            continue
        findings += lint_text(text, p, lang_of(p, a.lang), a.include_info, a.include_extrapolation, a.include_comments)
    if a.format == "json":
        print(json.dumps({"findings": findings, "total": len(findings),
                          "warning": "per-line heuristics; false positives/negatives expected; requires human verification (OCRG p.11)"}, ensure_ascii=False, indent=1))
    else:
        for f in findings:
            if a.format == "md":
                print("- **%s** `%s:%d` [%s | %s | %s] %s\n  - snippet: `%s`" % (f["rule"], f["file"], f["line"], f["class"], f["origin"], fmt_pages(f["ocrg_pages"]), f["message"], f["snippet"]))
            else:
                print("%s:%d: %s [%s | %s | %s] %s" % (f["file"], f["line"], f["rule"], f["class"], f["origin"], fmt_pages(f["ocrg_pages"]), f["message"]))
                print("    > " + f["snippet"])
        n_red = sum(1 for f in findings if f["class"] == "red_flag")
        print("\n%d finding(s) (%d red_flag). Per-line heuristic: requires human verification; absence of findings does NOT prove security." % (len(findings), n_red))
    if a.fail_on:
        bad = [f for f in findings if f["class"] == "red_flag" or (a.fail_on == "verify" and f["class"] == "verify")]
        if bad:
            sys.exit(1)


if __name__ == "__main__":
    main()
