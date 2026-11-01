# -*- coding: utf-8 -*-
"""
ripd_templates.py - privacy document templates with the elements that the TEXT of the LGPD (Lei Geral de Proteção de
Dados, Brazil's General Data Protection Law) lists, plus labeled additions.

Templates (the subcommand names are kept from the Portuguese original; English aliases in parentheses):
  ripd       RIPD (Relatório de Impacto à Proteção de Dados Pessoais, data protection impact report): minimum content of
             Art. 38, sole paragraph (p.14) + definition in Art. 5º, XVII (p.3) + [inference] additions anchored in other
             articles + a risk analysis section using the NIST IR 8062 logic (problematic data actions, likelihood,
             impact; p.29-31) as [inference/NIST].
  incidente  (incident) Security incident notification to the ANPD (national data protection authority) and the data
             subject: six minimum elements of Art. 48, §1º, I-VI (p.16). Deadline: "reasonable, as defined by the ANPD" in
             the text; a number of hours/days is an [extrapolation] (see the current regulation).
  registro   (record) Record of processing operations (Art. 37, p.14). The law does NOT list the fields: all [inference].
  titular    (data-subject) Response to a data subject request (Art. 18 and 19, p.9-10).
  all        generates all of them.

Usage (Python 3, stdlib, no network; run with `python -I`):
  python -I scripts/ripd_templates.py ripd [--org "ACME"] [--process "Customer registration"] [--format md|json] [--out FILE]
  python -I scripts/ripd_templates.py incidente [--org ...] [--incident INC-1]
  python -I scripts/ripd_templates.py registro [--org ...]
  python -I scripts/ripd_templates.py titular [--org ...]
  python -I scripts/ripd_templates.py all --outdir FOLDER
  (--processo is accepted as an alias of --process; the aliases incident, record, data-subject also work.)

Labels: [from source] = content of the law on the cited page; [inference] = structure/fields proposed by the agent;
[NIST] = NIST IR 8062 concept (not a legal requirement); [extrapolation] = outside the two sources.
This material is NOT legal advice: the RIPD should only be finalized with a lawyer/the encarregado (DPO) and according
to the current ANPD regulation [extrapolation].
"""
import argparse
import io
import json
import os
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

NOTICE = ("NOTICE: support template, not legal advice. Complete and validate it with a lawyer and with the encarregado (DPO); "
          "check the current version of the LGPD and the ANPD regulation on RIPD, incidents and data subject rights [extrapolation].")


def head(title, org, extra=""):
    return ["# %s" % title, "", "Organization: %s%s" % (org or "[fill in]", extra), "", "> " + NOTICE, ""]


def ripd(org, processo):
    p = processo or "[name of the processing process/activity]"
    sec = []
    sec.append({"id": "0", "title": "Instructions and origin of the document",
                "items": [
                    ("Use", "Controller's documentation of processing that may generate risks to civil liberties and fundamental rights, with measures, safeguards and mitigation mechanisms.", "[from source] LGPD Art. 5º, XVII, p.3"),
                    ("When it is required", "The ANPD may order it, including for sensitive data, under regulation, observing trade and industrial secrets; it may request it when the basis is legitimate interest (Art. 10 §3º) and may ask public bodies (Art. 32) or in the Art. 4º, III exceptions (§3º).", "[from source] LGPD Art. 38 caput p.14; Art. 10 §3º p.6; Art. 32 p.12; Art. 4º §3º p.2"),
                    ("ANPD regulation", "The ANPD issues regulations on RIPD for high-risk cases; check the current regulation (content, template, deadlines).", "[from source] LGPD Art. 55-J, XIII, p.21; regulation details = [extrapolation]"),
                ]})
    sec.append({"id": "1", "title": "Identification (proposed fields)",
                "items": [
                    ("Organization/controller", "[fill in]", "[inference]"),
                    ("Processor(s) involved", "[fill in] (Art. 39: they process according to the controller's instructions)", "[inference] + LGPD Art. 39 p.14"),
                    ("Encarregado (DPO)", "[name and contact; they must be publicly disclosed, Art. 41 §1º]", "[inference] + LGPD Art. 41 p.14"),
                    ("Process/activity assessed", p, "[inference]"),
                    ("Version, date, people responsible for drafting and approval", "[fill in]", "[inference]"),
                    ("Reason for the RIPD", "[ANPD order | legitimate interest | high risk | internal initiative (Art. 50 §2º, I, d)]", "[inference] + LGPD Art. 50 §2º I d p.17"),
                ]})
    sec.append({"id": "2", "title": "MINIMUM content required by the text (Art. 38, sole paragraph)",
                "items": [
                    ("2.1 Description of the types of data collected", "List the categories of personal data, indicating which are sensitive (Art. 5º, II) and whether data of children/adolescents is involved (Art. 14). Include origin, approximate volume and data subjects.", "[from source] LGPD Art. 38 sole paragraph, p.14"),
                    ("2.2 Methodology used for collection and for guaranteeing the security of the information", "Describe how data is collected (channels, forms, integrations) and how security is ensured (technical and administrative measures of Art. 46; security from the design stage, Art. 46 §2º).", "[from source] LGPD Art. 38 sole paragraph, p.14; Art. 46 p.15"),
                    ("2.3 Controller's analysis of the measures, safeguards and risk mitigation mechanisms adopted", "For each risk identified (section 4), describe the existing measures, the additional ones, the residual risk and the decision.", "[from source] LGPD Art. 38 sole paragraph, p.14; Art. 5º XVII p.3"),
                    ("2.4 Description of the processing processes that may generate risks to civil liberties and fundamental rights", "Describe the operations (life cycle: collection to deletion, Art. 5º X) and highlight those that may affect liberties and rights.", "[from source] LGPD Art. 5º XVII p.3 and X p.3"),
                ]})
    sec.append({"id": "3", "title": "Recommended additions (anchored in articles; the law does not require them in the RIPD)",
                "items": [
                    ("Purpose and legal basis", "Specific purpose and the Art. 7º basis (or Art. 11 if sensitive); for legitimate interest, the concrete situation and strictly necessary data.", "[inference] + LGPD Art. 6º I, Art. 7º, Art. 10, Art. 11"),
                    ("Necessity and minimization", "Why each data item is necessary; alternatives with less data.", "[inference] + LGPD Art. 6º III p.3"),
                    ("Sharing and international transfer", "Who the data is shared with (Art. 9º V; Art. 18 VII); if there is international transfer, the Art. 33 basis.", "[inference] + LGPD Art. 9º, 18, 33"),
                    ("Retention and deletion", "Periods, end-of-processing criteria and retention cases.", "[inference] + LGPD Art. 15-16 p.8"),
                    ("Data subject rights", "How the Art. 18 rights are met (channels, formats, Art. 19 deadlines).", "[inference] + LGPD Art. 18-19 p.9-10"),
                    ("Incidents", "How incidents will be detected and reported (Art. 48).", "[inference] + LGPD Art. 48 p.16"),
                    ("Consultation with stakeholders", "Record consultations (encarregado, security, legal, business area, data subjects or representatives when feasible).", "[inference]; NIST highlights the communication gap between legal and engineering (NIST8062 p.34)"),
                ]})
    sec.append({"id": "4", "title": "Risk analysis (NIST IR 8062 logic as a proposed method)",
                "note": "NIST defines risk as a function of likelihood and impact (p.29), proposes the problematic data action as a factor (p.29), likelihood for a representative individual (p.30), impact with cost proxies (p.30) and context (p.31). The LGPD asks to consider the probability and severity of risks (Art. 50 §1º, p.16) and a systematic assessment of impacts and risks (Art. 50 §2º I d, p.17). The scales and formulas below are [inference]: NIST IR 8062 provides no scale or matrix.",
                "table": ["Data action (collection, retention, logging, analysis, generation, merging, disclosure, transfer, disposal)",
                          "PII involved and context",
                          "Potential problem for the individual (loss of trust | loss of self-determination | discrimination | economic loss; NIST Fig. 3, p.18)",
                          "Likelihood (low/medium/high) and justification",
                          "Impact (low/medium/high) and proxies (compliance, mission, reputation, culture; NIST p.30)",
                          "Objective affected (predictability | manageability | disassociability; NIST p.25-28)",
                          "Existing / additional controls",
                          "Residual risk and decision (mitigate | accept | avoid) [inference]"],
                "items": [("Table rows", "[one row per data action; fill in]", "[inference + NIST8062 p.29-31]")]})
    sec.append({"id": "5", "title": "Approval, publication and review",
                "items": [
                    ("Approval", "[responsible person, date]", "[inference]"),
                    ("Periodic review", "Update based on continuous monitoring and periodic assessments (governance program).", "[from source] LGPD Art. 50 §2º I h p.17"),
                    ("Availability", "Demonstrate to the ANPD when requested; publication as appropriate (public authorities: Art. 32).", "[from source] LGPD Art. 50 §2º II p.17; Art. 32 p.12"),
                    ("Trade and industrial secrets", "The text requires observing them when the RIPD is ordered; mark confidential passages.", "[from source] LGPD Art. 38 caput p.14"),
                ]})
    return sec


def render_ripd_md(org, processo):
    out = head("Data protection impact report (RIPD - Relatório de Impacto à Proteção de Dados Pessoais) - template", org, " | Process: %s" % (processo or "[fill in]"))
    for s in ripd(org, processo):
        out.append("## %s. %s" % (s["id"], s["title"]))
        if s.get("note"):
            out += ["", s["note"], ""]
        if s.get("table"):
            out.append("| " + " | ".join(s["table"]) + " |")
            out.append("|" + "---|" * len(s["table"]))
            out.append("| " + " | ".join(["" for _ in s["table"]]) + " |")
            out.append("")
        for k, v, src in s["items"]:
            out.append("- **%s**: %s _(%s)_" % (k, v, src))
        out.append("")
    return "\n".join(out)


def incidente(org, inc):
    out = head("Security incident notification (ANPD and data subjects) - template", org, " | Incident: %s" % (inc or "[ID]"))
    out += [
        "Basis: the controller must notify the ANPD and the data subject of an incident that may cause relevant risk or harm (Art. 48, caput, p.16) `[from source]`.",
        "Deadline: the text says 'reasonable period, as defined by the ANPD' (Art. 48 §1º, p.16) `[from source]`; the number of hours or days is an `[extrapolation]` (check the current ANPD regulation). The text does not set 72 hours.",
        "",
        "## A. Triage (proposed fields) `[inference]`",
        "- Date/time of awareness and of occurrence; how it was detected; systems involved.",
        "- May the incident cause relevant risk or harm to data subjects? Justification (nature of the data, volume, sensitivity, ease of identification, measures that make the data unintelligible, Art. 48 §3º p.16).",
        "- Decision to notify (yes/no), responsible person and date.",
        "",
        "## B. Minimum content of the notification (Art. 48, §1º, I to VI, p.16) `[from source]`",
        "1. Description of the nature of the personal data affected: [fill in]",
        "2. Information on the data subjects involved: [fill in]",
        "3. Indication of the technical and security measures used to protect the data, observing trade and industrial secrets: [fill in]",
        "4. Risks related to the incident: [fill in]",
        "5. Reasons for the delay, if the notification was not immediate: [fill in or 'immediate notification']",
        "6. Measures that were or will be adopted to reverse or mitigate the effects of the harm: [fill in]",
        "",
        "## C. After the notification",
        "- The ANPD verifies the severity and may order measures, such as wide disclosure and measures to reverse or mitigate (Art. 48 §2º, p.16) `[from source]`.",
        "- Keep evidence of the measures adopted: relevant to the severity assessment (Art. 48 §3º) and to the sanction parameters (Art. 52 §1º, VIII and X, p.18) `[from source]`.",
        "- Encarregado channel for data subjects and the ANPD (Art. 41 §2º, p.14) `[from source]`.",
        "- Notification to the data subject: clear language, what to do, contact channel `[inference]`.",
        "",
    ]
    return "\n".join(out)


def registro(org):
    cols = ["Operation/activity", "Purpose", "Legal basis (Art. 7º/11)", "Categories of data and data subjects", "Sensitive data/children?", "Sharing (with whom)", "International transfer (Art. 33)", "Retention period and deletion criterion", "Security measures", "Processor(s)"]
    out = head("Record of processing operations (Art. 37) - template", org)
    out += [
        "Basis: the controller and the processor must keep a record of processing operations, especially when based on legitimate interest (Art. 37, p.14) `[from source]`.",
        "The law does NOT list the fields of the record; all columns below are `[inference]` anchored in other articles (purpose Art. 6º I; bases Art. 7º/11; sharing Art. 9º V; transfer Art. 33; retention Art. 15-16; security Art. 46). The ANPD may regulate the retention time of the records (Art. 40, p.14) `[from source]`.",
        "",
        "| " + " | ".join(cols) + " |",
        "|" + "---|" * len(cols),
        "| " + " | ".join(["" for _ in cols]) + " |",
        "",
    ]
    return "\n".join(out)


def titular(org):
    out = head("Response to a data subject request (Art. 18-19) - template", org)
    out += [
        "Basis: rights in Art. 18, I to IX, exercised by express request of the data subject or representative to a processing agent (Art. 18 §3º, p.9), answered free of charge (§5º) `[from source]`.",
        "",
        "## Request data `[inference]`",
        "- Protocol, date, channel; identification of the requester (and of the representative, if any); proportionate identity verification; right exercised (Art. 18 inciso).",
        "",
        "## Deadlines and format `[from source]` (Art. 19, p.10)",
        "- Confirmation of existence or access: simplified format, immediately; or a clear and complete declaration within 15 days of the request (inciso II), indicating the origin of the data, absence of records, criteria used and purpose, observing trade and industrial secrets.",
        "- Secure and suitable electronic means or print, at the data subject's choice (§2º). If the origin is consent or a contract, a full electronic copy in a reusable format (§3º). The ANPD may regulate the deadlines differently by sector (§4º).",
        "- For the other incisos the deadline is the one in the regulation (Art. 18 §5º, p.9) `[from source]`; the length of the deadline = `[extrapolation]` (check).",
        "",
        "## If an immediate response is not possible (Art. 18 §4º, p.9) `[from source]`",
        "- State that you are not a processing agent and indicate, if possible, who is; or indicate the factual or legal reasons that prevent immediate action.",
        "",
        "## After the response",
        "- Correction, deletion, anonymization or blocking: immediately inform the agents with whom the data was shared, unless proven impossible or a disproportionate effort (Art. 18 §6º, p.9) `[from source]`.",
        "- Right to petition the ANPD (Art. 18 §1º) and consumer protection bodies (§8º) `[from source]`.",
        "- Record the decision and the evidence of compliance `[inference]`.",
        "",
    ]
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd")
    for name, aliases in (("ripd", []), ("incidente", ["incident"]), ("registro", ["record"]), ("titular", ["data-subject"]), ("all", [])):
        p = sp.add_parser(name, aliases=aliases)
        p.add_argument("--org")
        p.add_argument("--process", "--processo", dest="processo")
        p.add_argument("--incident")
        p.add_argument("--format", choices=["md", "json"], default="md")
        p.add_argument("--out")
        p.add_argument("--outdir")
    a = ap.parse_args()
    if not a.cmd:
        ap.print_help()
        return 0
    a.cmd = {"incident": "incidente", "record": "registro", "data-subject": "titular"}.get(a.cmd, a.cmd)

    def emit(text, out):
        if out:
            with io.open(out, "w", encoding="utf-8", newline="\n") as f:
                f.write(text)
            print("written: %s" % out)
        else:
            sys.stdout.write(text if text.endswith("\n") else text + "\n")

    if a.cmd == "ripd":
        if a.format == "json":
            emit(json.dumps({"notice": NOTICE, "organization": a.org, "process": a.processo, "sections": ripd(a.org, a.processo)}, ensure_ascii=False, indent=1), a.out)
        else:
            emit(render_ripd_md(a.org, a.processo), a.out)
    elif a.cmd == "incidente":
        emit(incidente(a.org, a.incident), a.out)
    elif a.cmd == "registro":
        emit(registro(a.org), a.out)
    elif a.cmd == "titular":
        emit(titular(a.org), a.out)
    elif a.cmd == "all":
        d = a.outdir
        if not d:
            raise SystemExit("--outdir is required with `all`")
        os.makedirs(d, exist_ok=True)
        emit(render_ripd_md(a.org, a.processo), os.path.join(d, "ripd.md"))
        emit(incidente(a.org, a.incident), os.path.join(d, "incidente.md"))
        emit(registro(a.org), os.path.join(d, "registro-operacoes.md"))
        emit(titular(a.org), os.path.join(d, "resposta-titular.md"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
