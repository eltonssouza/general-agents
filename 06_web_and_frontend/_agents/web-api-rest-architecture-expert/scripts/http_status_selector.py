# -*- coding: utf-8 -*-
"""
Skill: http-status-selector
Lookup of HTTP status + headers for common scenarios, separating what is in
*Web API Design: The Missing Link* (Apigee/Google, 2018) from general HTTP knowledge.
Standard library only, no network, read-only.

The source shows only 200, 201, 303, 401 and 405 (APIGEE p.7, p.43, p.51, p.52) and says to
"learn the standard HTTP statuses and use them with their headers" (APIGEE p.51-52).
The other codes appear here as [extrapolation] (RFC 9110), WITHOUT a page from the book.

Usage:
  python -I http_status_selector.py <scenario>
  python -I http_status_selector.py --list
"""

import argparse
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

LIVRO = "from source"
EXTRA = "extrapolation"

CATALOG = {
    "create": (201, "Created", ["Location: <URL of the new resource>"], LIVRO, "APIGEE p.7, p.51",
               "Always paired with Location."),
    "read_ok": (200, "OK", ["Content-Location", "Content-Type", "ETag", "Content-Length"], LIVRO, "APIGEE p.52",
                "Standard header package of a GET; the authors always include Content-Location."),
    "method_not_allowed": (405, "Method Not Allowed", ["Allow: <accepted methods>"], LIVRO, "APIGEE p.52",
                           "Must come with Allow."),
    "paginate_redirect": (303, "See Other", ["Location: <first page>"], LIVRO, "APIGEE p.43, p.44",
                          "The authors' example for a collection that is too large."),
    "unauthorized": (401, "Unauthorized", [], LIVRO, "APIGEE p.52",
                     "Appears only in a short list, without discussion."),
    "concurrent_update": (412, "Precondition Failed", ["If-Match / ETag in the request"], EXTRA, None,
                          "The book only says to use ETag + If-Match (APIGEE p.7); the 412 code is from RFC 9110."),
    "async_accepted": (202, "Accepted", ["Location: <tracking resource>"], EXTRA, None,
                       "The book suggests that the POST of an action request returns a resource whose state shows "
                       "progress (APIGEE p.53), but does not mention 202."),
    "no_content": (204, "No Content", [], EXTRA, None, "Does not appear in the source."),
    "bad_request": (400, "Bad Request", [], EXTRA, None, "Does not appear in the source."),
    "validation": (422, "Unprocessable Content", [], EXTRA, None, "Does not appear in the source."),
    "forbidden": (403, "Forbidden", [], EXTRA, None, "Does not appear in the source."),
    "not_found": (404, "Not Found", [], EXTRA, None, "Does not appear in the source."),
    "conflict": (409, "Conflict", [], EXTRA, None, "Does not appear in the source."),
    "rate_limit": (429, "Too Many Requests", ["Retry-After"], EXTRA, None,
                   "Rate limiting is not covered in the source."),
    "server_error": (500, "Internal Server Error", [], EXTRA, None, "Does not appear in the source."),
}

# Portuguese aliases for user input -> scenario key (the English keys keep working as before).
ALIASES_PT = {
    "criar": "create", "criacao": "create", "criação": "create",
    "leitura": "read_ok", "ler": "read_ok",
    "metodo_nao_permitido": "method_not_allowed", "método_não_permitido": "method_not_allowed",
    "paginacao": "paginate_redirect", "paginação": "paginate_redirect",
    "nao_autorizado": "unauthorized", "não_autorizado": "unauthorized",
    "atualizacao_concorrente": "concurrent_update", "atualização_concorrente": "concurrent_update",
    "assincrono": "async_accepted", "assíncrono": "async_accepted",
    "sem_conteudo": "no_content", "sem_conteúdo": "no_content",
    "requisicao_invalida": "bad_request", "requisição_inválida": "bad_request",
    "validacao": "validation", "validação": "validation",
    "proibido": "forbidden",
    "nao_encontrado": "not_found", "não_encontrado": "not_found",
    "conflito": "conflict",
    "limite_de_requisicoes": "rate_limit", "limite_de_requisições": "rate_limit",
    "erro_servidor": "server_error", "erro_do_servidor": "server_error",
}


def main():
    ap = argparse.ArgumentParser(description="HTTP status + headers (Apigee 2018 vs general knowledge)")
    ap.add_argument("scenario", nargs="?", default="")
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()
    if args.list or not args.scenario:
        for k, (code, name, _, rot, cit, _) in CATALOG.items():
            print(f"- {k:20} {code} {name:22} [{rot}]" + (f" ({cit})" if cit else ""))
        print("\nGeneral rule [from source] (APIGEE p.51, p.52): standard status + matching headers; "
              "think in terms of complete HTTP messages.")
        return
    key = args.scenario.lower().strip()
    key = ALIASES_PT.get(key, key)
    hits = [k for k in CATALOG if key == k] or [k for k in CATALOG if key in k]
    if not hits:
        print(f"Scenario '{args.scenario}' is not cataloged. Use --list.")
        sys.exit(1)
    for k in hits:
        code, name, headers, rot, cit, note = CATALOG[k]
        print(f"{k}: {code} {name}")
        print(f"  Label: [{rot}]" + (f" ({cit})" if cit else " — no page from the book"))
        if headers:
            print("  Headers: " + "; ".join(headers))
        print(f"  Note: {note}")


if __name__ == "__main__":
    main()
