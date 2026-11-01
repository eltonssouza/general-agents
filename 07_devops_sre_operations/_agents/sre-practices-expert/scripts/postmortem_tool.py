# -*- coding: utf-8 -*-
"""
postmortem_tool.py - postmortem template, checklist and validator based on the Google SRE Book (2016).
Pages = PDF (printed = N-12).

Origin of each element:
  * 13 fields of the Appendix D "Example Postmortem" template (SRE p.334-336)           [from source]
  * triggers for writing a postmortem (5)                                                 [from source] (SRE p.126)
  * formal review criteria (5)                                                            [from source] (SRE p.127)
  * fields of the Appendix C Incident State Document (SRE p.332-333)                      [from source]
  * warnings about blame language and about actions without owner/deadline               [inference]/[extrapolation]
    (the Action Items table of App. D is cut off at the PDF margin: only the Action Item column is legible)
Ch. 15 does NOT list the template fields; the fields come from the Appendix D example.

Subcommands:
  template [--lang en|pt]   print the template in Markdown (default: en; pt = Portuguese-language template)
  checklist                 print triggers and review criteria
  triggers [--flags]        assess whether any trigger from the book was hit
  validate FILE.md          check the presence of the 13 fields and warn about blame (Portuguese or English postmortems)
  incident-doc              print the Incident State Document template (App. C)
Offline; read-only (except stdout).
"""
import argparse
import re
import sys

# (English name, Portuguese name, English hint, Portuguese hint). The pt column is the Portuguese-language template.
FIELDS = [
    ("Date", "Data", "Date of the incident", "Data do incidente"),
    ("Authors", "Autores", "Who wrote it", "Quem escreveu"),
    ("Status", "Status", "E.g. complete, actions in progress", "Ex.: completo, acoes em andamento"),
    ("Summary", "Resumo", "Short summary of the incident and its duration", "Resumo curto do incidente e da duracao"),
    ("Impact", "Impacto", "Effect on users, revenue etc. (the example estimates lost queries)", "Efeito em usuarios, receita etc. (o exemplo estima queries perdidas)"),
    ("Root Causes", "Causas-raiz", "Circumstances that led to the incident; the book suggests a technique such as 5 Whys (App. D note)", "Circunstancias que levaram ao incidente; o livro sugere tecnica como 5 Whys (nota do Ap. D)"),
    ("Trigger", "Gatilho", "The event that set off the latent failure", "O evento que disparou a falha latente"),
    ("Resolution", "Resolucao", "What was done to mitigate and resolve", "O que foi feito para mitigar e resolver"),
    ("Detection", "Deteccao", "How it was detected (the example cites monitoring paging the on-call)", "Como foi detectado (o exemplo cita o monitoramento paginando o on-call)"),
    ("Action Items", "Itens de acao", "Prevention/mitigation actions", "Acoes de prevencao/mitigacao"),
    ("Lessons Learned", "Licoes aprendidas", "Subsections: What went well / What went wrong / Where we got lucky", "Subsecoes: What went well / What went wrong / Where we got lucky"),
    ("Timeline", "Linha do tempo", "Chronology; in the example it distinguishes OUTAGE and INCIDENT", "Cronologia; no exemplo distingue OUTAGE e INCIDENT"),
    ("Supporting information", "Informacoes de apoio", "Links, logs, graphs, dashboards", "Links, logs, graficos, dashboards"),
]
# Portuguese synonyms accepted by validate (user input; limitation: only recognizes these and the template names).
SYNONYMS = {
    "Root Causes": ["causa raiz", "causa-raiz", "causas raiz", "causa(s) raiz", "causa raiz do incidente"],
    "Impact": ["impacto"],
    "Trigger": ["gatilho", "disparador"],
    "Detection": ["deteccao", "como foi detectado"],
    "Action Items": ["itens de acao", "acoes", "plano de acao", "item de acao"],
    "Lessons Learned": ["licoes aprendidas", "licoes", "aprendizados"],
    "Timeline": ["linha do tempo", "cronologia"],
    "Supporting information": ["informacoes de apoio", "informacao de apoio", "informacoes de suporte", "informacoes adicionais"],
    "Resolution": ["resolucao", "mitigacao e resolucao"],
    "Summary": ["resumo", "sumario"],
    "Authors": ["autores", "autor"],
    "Date": ["data"],
    "Status": ["status", "situacao"],
}
LESSON_SUBS = [("What went well", "O que deu certo"), ("What went wrong", "O que deu errado"),
               ("Where we got lucky", "Onde tivemos sorte (near misses)")]

TRIGGERS = [
    ("user_visible_downtime", "user-visible downtime or degradation above a threshold"),
    ("data_loss", "data loss of any kind"),
    ("oncall_intervention", "on-call intervention (release rollback, traffic rerouting etc.)"),
    ("slow_resolution", "resolution time above a threshold"),
    ("monitoring_failure", "monitoring failure (the incident was usually discovered manually)"),
]
REVIEW = [
    "Was the key incident data collected for posterity?",
    "Are the impact assessments complete?",
    "Is the root cause deep enough?",
    "Is the action plan appropriate and are the bugs given appropriate priority?",
    "Was the outcome shared with the relevant stakeholders?",
]
INCIDENT_DOC = [
    "Title with date + link to the incident management cheat sheet",
    "Summary", "Status (e.g. active, incident #N)", "Command Post(s)",
    "Command Hierarchy: Incident Commander, Operations lead, Planning lead, Communications lead, next IC (update at least every 4 hours and at the Comms handoff)",
    "Detailed Status (with time and author of the last update)",
    "Exit Criteria (e.g. availability and latency SLOs met for 30+ minutes)",
    "TODO list and bugs filed", "Incident timeline (most recent first, UTC)",
]
BLAME_PATTERNS = [
    r"\bculpa d[eoa]s?\b", r"\bfault of\b", r"\bnegligen", r"\bcareless", r"\bincompeten",
    r"\bblame\b", r"\bdescuid", r"\bshould have known\b", r"\bfoi culpa\b",
    # PT-BR (normalized text: lowercase, no accents); "sem culpa" / "sem atribuir culpa" (blameless postmortem) does not count
    r"(?<!sem )(?<!sem atribuir )(?<!nao ha )\bculpa(do|dos|da|das)?\b", r"\bnegligenc", r"\bimperici", r"\birresponsab",
    r"\bfalha humana\b", r"\berro humano\b", r"\bdesatenc", r"\bdistrai",
    r"\b(fez|executou|rodou|digitou|aplicou|escolheu|configurou|esqueceu)\b[^.\n]{0,50}\berrad[oa]s?\b", r"\bfoi errad[oa]\b",
    r"\balguem errou\b", r"\b\w+ errou\b", r"\bquem errou\b", r"\bo erro (foi|e) d[eoa]\b",
    r"\badvertid[oa]s?\b", r"\badvertenc", r"\bpunid[oa]s?\b", r"\bpunic", r"\bdemitid", r"\bdemiss",
    r"\bmais cuidados[oa]s?\b", r"\bter mais cuidado\b",
    r"\bdeveria ter (sabido|testado|percebido|verificado|cuidado|checado|revisado)\b",
    r"\bnao testou\b", r"\bnao verificou\b", r"\bnao prestou atencao\b",
    r"\bresponsavel pel[oa] (erro|incidente|falha|problema|outage|queda)\b",
]


def cmd_template(a):
    pt = a.lang == "pt"
    print("# Postmortem: <titulo do incidente> (incidente #<n>)" if pt else "# Postmortem: <incident title> (incident #<n>)")
    if pt:
        print("<!-- Campos do exemplo do Apendice D (SRE p.334-336). Foco: processo e tecnologia, sem culpa (SRE p.126-127). -->\n")
    else:
        print("<!-- Fields from the Appendix D example (SRE p.334-336). Focus: process and technology, blameless (SRE p.126-127). -->\n")
    for en, ptn, hint_en, hint_pt in FIELDS:
        name = ptn if pt else en
        print("## %s" % name)
        if en == "Lessons Learned":
            for e, p in LESSON_SUBS:
                print("### %s" % (p if pt else e))
                print("- ")
        elif en == "Action Items":
            if pt:
                print("| Acao | Tipo (prevenir/mitigar) | Dono | Prazo |  <!-- dono/prazo: boa pratica [extrapolacao]; a tabela do Ap. D esta cortada no PDF -->")
            else:
                print("| Action | Type (prevent/mitigate) | Owner | Due date |  <!-- owner/due date: good practice [extrapolation]; the App. D table is cut off in the PDF -->")
            print("|---|---|---|---|")
            print("|  |  |  |  |")
        else:
            print("<!-- %s -->" % (hint_pt if pt else hint_en))
        print()
    return 0


def cmd_checklist(a):
    print("TRIGGERS for writing a postmortem [from source] (SRE p.126) - define BEFORE the incident; any stakeholder can request one:")
    for _, t in TRIGGERS:
        print("  - " + t)
    print("\nREVIEW CRITERIA [from source] (SRE p.127):")
    for r in REVIEW:
        print("  [ ] " + r)
    print("\nPrinciples [from source]: blameless (SRE p.126-127); no postmortem goes without review (SRE p.128); no data that identifies end users (SRE p.127).")
    print("The book does NOT set a deadline for publishing nor numeric thresholds for the triggers.")
    return 0


def cmd_triggers(a):
    hit = [t for k, t in TRIGGERS if getattr(a, k)]
    if hit:
        print("Postmortem recommended by the book (SRE p.126). Triggers hit:")
        for h in hit:
            print("  - " + h)
    else:
        print("No trigger from the book was hit. Even so, any stakeholder can request a postmortem (SRE p.126); the book also says there is a cost and that you should choose when to write one.")
    return 0


def norm(s):
    import unicodedata
    s = unicodedata.normalize("NFKD", s.lower())
    return "".join(c for c in s if not unicodedata.combining(c))


def cmd_validate(a):
    try:
        with open(a.file, encoding="utf-8") as f:
            text = f.read()
    except OSError as e:
        print("Error reading file: %s" % e)
        return 2
    low = norm(text)
    head_re = r"^\s*(?:#+|\*\*|[-*]\s*\*\*)\s*([^\n*]+)"
    heads = [norm(m.group(1)) for m in re.finditer(head_re, text, re.M)]
    heads_blob = " | ".join(heads)
    missing = []
    for en, ptn, _, _ in FIELDS:
        names = [norm(en), norm(ptn)] + SYNONYMS.get(en, [])
        if not any(n in heads_blob for n in names):
            missing.append(en)
    print("Template fields (Appendix D, SRE p.334-336): %d/%d present" % (len(FIELDS) - len(missing), len(FIELDS)))
    for m in missing:
        print("  MISSING: %s" % m)
    for e, p in LESSON_SUBS:
        if norm(e) not in heads_blob and norm(p.split(" (")[0]) not in heads_blob:
            print("  WARNING: Lessons Learned subsection missing: %s [from source] (SRE p.334-335)" % e)
    low_nc = re.sub(r"<!--.*?-->", " ", low, flags=re.S)  # HTML comments from the template ("sem culpa") do not count
    blame = [p for p in BLAME_PATTERNS if re.search(p, low_nc)]
    if blame:
        print("  WARNING [inference]: possible blame language (the book asks for a blameless postmortem, SRE p.126-127): %s" % ", ".join(blame))
    if re.search(r"action items", low) or "itens de acao" in low:
        if not re.search(r"\b(dono|owner|responsavel|prazo|due)\b", low):
            print("  WARNING [extrapolation]: actions without owner/deadline (the App. D table is cut off in the PDF, only the Action Item column is legible; tracking follow-up is recommended: SRE p.120)")
    return 1 if missing else 0


def cmd_incident_doc(a):
    print("# Incident State Document (Appendix C, SRE p.332-333; keep it live and editable by several people, SRE p.124)")
    for i, f in enumerate(INCIDENT_DOC, 1):
        print("%d. %s" % (i, f))
    print("\nBook tip: most important information at the top; retain it for the postmortem (SRE p.124).")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("template")
    s.add_argument("--lang", choices=["en", "pt"], default="en")
    s.set_defaults(f=cmd_template)
    s = sub.add_parser("checklist")
    s.set_defaults(f=cmd_checklist)
    s = sub.add_parser("triggers")
    for k, t in TRIGGERS:
        s.add_argument("--" + k.replace("_", "-"), dest=k, action="store_true", help=t)
    s.set_defaults(f=cmd_triggers)
    s = sub.add_parser("validate")
    s.add_argument("file")
    s.set_defaults(f=cmd_validate)
    s = sub.add_parser("incident-doc")
    s.set_defaults(f=cmd_incident_doc)
    a = ap.parse_args(argv)
    return a.f(a)


if __name__ == "__main__":
    sys.exit(main())
