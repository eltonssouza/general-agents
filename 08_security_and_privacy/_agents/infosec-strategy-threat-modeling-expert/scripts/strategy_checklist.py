# -*- coding: utf-8 -*-
"""
strategy_checklist.py - information security strategy checklist with items drawn from the DZ
(Infosec Strategies and Best Practices, MacMillan, Packt 2021) and PDF pages (printed = PDF - 17).

Usage (Python 3, stdlib, no network, read-only; run with `python -I`):
  python -I scripts/strategy_checklist.py areas
  python -I scripts/strategy_checklist.py list [--area GOV]
  python -I scripts/strategy_checklist.py markdown [--area GOV] [--title TEXT]
  python -I scripts/strategy_checklist.py evaluate FILE.json     # {"G01":"sim","G02":"nao","R03":"parcial","S05":"na"}
Answers: sim/nao/parcial/na (Portuguese, kept) or yes/no/partial/na (English).

Origin: the PRACTICE behind each item comes from the DZ on the cited page(s) [from source]; the question FORM is [inference].
Dated items are marked [DATED]. The checklist is a review aid; it is not a standard and does not replace ISO 27001 or
applicable law. Exit code: 0 ok; 2 invalid input.
"""
import argparse
import json
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

AREAS = [
    ("GOV", "Governance and risk (Ch.1)"),
    ("ISMS", "ISMS and policies (Ch.2)"),
    ("ATV", "Assets, data, retention and disposal (Ch.2)"),
    ("TERC", "Third parties and vendors (Ch.1, 8)"),
    ("DES", "Secure design and controls (Ch.3)"),
    ("NET", "Network and Zero Trust (Ch.4)"),
    ("IAM", "Access and identity (Ch.5)"),
    ("TST", "Testing and assessments (Ch.6)"),
    ("OPS", "Operations: configuration, change, DR/BC (Ch.7)"),
    ("IR", "Incidents and monitoring (Ch.2, 7)"),
    ("SW", "Software, SDLC and DevSecOps (Ch.8)"),
]

# (id, area, question, pages, extra_label)
ITEMS = [
    ("G01", "GOV", "Is there an asset register with the crown jewels and an owner per asset?", "24, 56", ""),
    ("G02", "GOV", "Were the impact and likelihood scales defined with the stakeholders (the DZ example uses 1-5 and % of revenue)?", "28-29", ""),
    ("G03", "GOV", "Is the risk appetite (acceptance level) defined and do the scales reflect it?", "33", ""),
    ("G04", "GOV", "Does the risk register carry the treatment (avoid, reduce, transfer, accept) and the residual risk?", "33-34", ""),
    ("G05", "GOV", "Are earlier versions of the risk register kept to show progress?", "44", ""),
    ("G06", "GOV", "Is risk reported to senior management in terms of impact, cost and deadline, without technical jargon?", "44-45, 48-49", ""),
    ("G07", "GOV", "Are threats and actors documented per asset (capability, interest, tactics), with placeholders for actors that are irrelevant today?", "25-26", ""),
    ("G08", "GOV", "Were environmental threats (weather, power) considered for availability?", "26", ""),
    ("G09", "GOV", "Are legal, regulatory and contractual requirements cataloged and reviewed regularly?", "35-37", ""),
    ("G10", "GOV", "Do internal audits check whether the organization does what it says and says what it does?", "36, 89", ""),
    ("G11", "GOV", "Do gaps found (simulations, tests) become small projects, with risk reassessment after the fix?", "39-40", ""),
    ("G12", "GOV", "Is there awareness training with an annual agreement and simulations, without blaming the phishing victim?", "41", ""),
    ("I01", "ISMS", "Is there explicit executive sponsorship and a consequence for not following the policies?", "48, 64", ""),
    ("I02", "ISMS", "Are the ISMS context and scope documented (including what is out of scope and how third parties align with the appetite)?", "51-52", ""),
    ("I03", "ISMS", "Is there a Statement of Applicability with a justification per control (applicable-implemented, applicable-not implemented, not applicable)?", "52-53", "[DATED] ISO 27001:2013 numbering"),
    ("I04", "ISMS", "Does the security policy have measurable CIA objectives, and is it approved, published and communicated?", "54", ""),
    ("I05", "ISMS", "Are roles and responsibilities, legal requirements, internal audit and corrective action documented?", "54-55", ""),
    ("I06", "ISMS", "Are records (BIA, training, monitoring, audits, management review, corrective actions, logs) kept?", "55", ""),
    ("I07", "ISMS", "Do the risk assessment and treatment methodologies define when (e.g., annually or on significant change), who and how?", "59", ""),
    ("I08", "ISMS", "Is there a two-level risk report (overview for management; detailed per asset and per control)?", "60", ""),
    ("I09", "ISMS", "Is the ISMS effectiveness reviewed regularly and do nonconformities go to corrective action?", "64", ""),
    ("I10", "ISMS", "Do the IT documents (access, password, backup, change, disposal etc.) reflect reality?", "63", ""),
    ("A01", "ATV", "Is the inventory kept up to date and does each asset have an owner with responsibility and authority?", "56", ""),
    ("A02", "ATV", "Is there a classification policy (usually ~4 levels) and a labeling policy?", "57", ""),
    ("A03", "ATV", "Is there an acceptable use policy that is accessible and part of the training?", "57-58", ""),
    ("A04", "ATV", "Is data discovery and classification automated (DLP/Information Protection) where manual work does not scale?", "68", ""),
    ("A05", "ATV", "Is retention defined (what to keep, for how long, how to search, owner) and enforced by technology where possible?", "69-70", ""),
    ("A06", "ATV", "Are data in transit and at rest encrypted as required (e.g., PCI-DSS, ISO 27001)?", "73", ""),
    ("A07", "ATV", "Does media disposal follow a formal procedure, with a record and removal of data remnants?", "76", "[DATED] 7-pass overwrite rule"),
    ("A08", "ATV", "Does archiving respect legal retention periods?", "77", ""),
    ("A09", "ATV", "Are the controls reassessed when the asset value changes?", "72", ""),
    ("T01", "TERC", "Are there binding SLAs with availability and penalties, seen as a compensating control?", "42, 72", ""),
    ("T02", "TERC", "Do vendors answer a VSAQ or CAIQ in the purchasing phase, with risk as the backbone of the analysis?", "43", ""),
    ("T03", "TERC", "Are due diligence and due care documented to prove an informed decision?", "43-44, 225", ""),
    ("T04", "TERC", "Are the assets managed by third parties cataloged and is the shared responsibility clear?", "61, 97", ""),
    ("T05", "TERC", "Does the contract provide for vendor liability, remediation SLAs and a channel to report vulnerabilities?", "225-226, 245", ""),
    ("T06", "TERC", "Is the vendor asked how it follows the SDLC, and is evidence requested?", "246", ""),
    ("T07", "TERC", "Is a pentest report requested, or is there a vendor bug bounty, as a signal?", "247", ""),
    ("T08", "TERC", "Does third-party on-prem software run with least privilege and fall within the scope of the scans?", "247", ""),
    ("T09", "TERC", "Does open source go through the same steps (dependencies, SAST, DAST, scans) as in-house software?", "248", ""),
    ("D01", "DES", "Are new systems designed with security from the start (secure by design)?", "80, 104", ""),
    ("D02", "DES", "Is least privilege applied, with Just-In-Time where possible?", "103", ""),
    ("D03", "DES", "Does the design follow Zero Trust (always verify, assume breach, segment)?", "104", ""),
    ("D04", "DES", "Does the design avoid security through obscurity as the main defense?", "105, 123", ""),
    ("D05", "DES", "Is there defense in depth for each attacker step (gain access, escalate privileges, maintain access, exfiltrate, evade detection)?", "85, 105", ""),
    ("D06", "DES", "Are controls chosen by risk level and knowledge of the application, without complexity that brings no benefit?", "102", ""),
    ("D07", "DES", "Are new controls tested (first internally, then by a third party if the asset justifies it)?", "98", ""),
    ("D08", "DES", "Where applicable, were TCB, TPM and the reference monitor (NEAT) considered?", "99", ""),
    ("D09", "DES", "Do mobile devices, IoT and SCADA have specific mitigations (segregated network, air gap, baseline)?", "107-109", ""),
    ("D10", "DES", "Was the system designed to receive updates and patches, even if isolated?", "110", ""),
    ("D11", "DES", "Do the controls cover deter, prevent, detect, delay, correct and recover?", "71-72", ""),
    ("D12", "DES", "Do backups and redundancy cover availability and integrity (including ransomware)?", "106", ""),
    ("N01", "NET", "Is there a network security policy with change control, reviewed whenever something relevant changes?", "136-137", ""),
    ("N02", "NET", "Is the network segmented (avoiding a flat network)?", "126", ""),
    ("N03", "NET", "Was deny-all with an allowlist evaluated against a real inventory of communications, to avoid outages?", "126", ""),
    ("N04", "NET", "Do encrypted protocols replace legacy ones (HTTPS, SFTP, SSH), with a VPN when unavoidable?", "133", ""),
    ("N05", "NET", "Is there a plan against DoS/DDoS, including cloud cost (Denial-of-Wallet)?", "134-136", ""),
    ("N06", "NET", "Is the cloud under change control, with testing before production and deprovisioning?", "141-142", ""),
    ("N07", "NET", "Are there microsegmentation, the two-person principle and segregation of duties?", "139-140", ""),
    ("N08", "NET", "Is there an asset lifecycle and vulnerability management (identify, classify, remediate, mitigate)?", "140", ""),
    ("N09", "NET", "Does the SOC/SIEM receive signals from IDS/IPS, firewalls, CDN, antivirus and vulnerability management?", "142-143", ""),
    ("M01", "IAM", "Are authentication and authorization distinct, and does MFA use factors from different categories?", "153-154", ""),
    ("M02", "IAM", "Are passwords stored with hash and salt, with an attempt limit?", "154", ""),
    ("M03", "IAM", "Is SSO used where it reduces password reuse and eases revocation?", "156", ""),
    ("M04", "IAM", "Was legacy NTLM removed or mitigated (SMB signing, blocking NTLMv1, LDAP signing/channel binding, EPA)?", "157-158", ""),
    ("M05", "IAM", "Are PKI and certificates used for passwordless authentication, preferably with a second factor?", "160-161", ""),
    ("M06", "IAM", "Is the access model (RBAC, ABAC, MAC, DAC or a combination) chosen and does it apply least privilege?", "151-152, 161", ""),
    ("M07", "IAM", "Is identity centralized, with provisioning and deprovisioning automated from HR?", "162-163", ""),
    ("M08", "IAM", "Is access reviewed periodically to prevent accumulation with every role change?", "163", ""),
    ("M09", "IAM", "Do exceptions to the access rules have escalation, approval and administration?", "163", ""),
    ("M10", "IAM", "Is physical access controlled and logged, and are its risks in the risk register?", "164-166", ""),
    ("S01", "TST", "Does senior management support the tests and react formally to the findings (remediate or accept)?", "172", ""),
    ("S02", "TST", "Are the testing requirements of applicable standards mapped (e.g., PCI-DSS Req.11)?", "173-174", ""),
    ("S03", "TST", "Does each assessment have its reason, scope, time, deadline and budget defined?", "175", ""),
    ("S04", "TST", "Do the terms include an NDA and care not to take production down?", "176", ""),
    ("S05", "TST", "Is there a clone environment with fictitious data for scans and some pentests (aware of the acceptance trade-off)?", "179, 188", ""),
    ("S06", "TST", "Do web application and network scanners run regularly?", "177-181", ""),
    ("S07", "TST", "Are SAST, DAST and dependency scanning in the SDLC/CI?", "181-183", ""),
    ("S08", "TST", "Are there internal assessments (tests and phishing simulations, compliance audits)?", "183-184", ""),
    ("S09", "TST", "Is a third-party pentest, red team or black team used according to risk?", "184-185", ""),
    ("S10", "TST", "Are findings presented to stakeholders, the fix validated internally, a retest done and a new cycle scheduled?", "189", ""),
    ("O01", "OPS", "Are there approved baseline configurations (e.g., CIS) pointed to by a living document, rather than embedded in the policy?", "194-196", ""),
    ("O02", "OPS", "Do changes record user, time, what and which systems, with segregation of duties and aligned environments?", "195-196", ""),
    ("O03", "OPS", "Is IaC versioned and scanned, with no way to disable pipeline checks?", "197-200", ""),
    ("O04", "OPS", "Are secrets managed (create, revoke, rotate, audit) and kept out of code?", "199, 240", ""),
    ("O05", "OPS", "Are DR and BC truly rehearsed (not only tabletop), with hot/warm/cold sites evaluated by risk?", "201-203", ""),
    ("O06", "OPS", "Does change control include justification, impact, rollback, approvals, communication and evaluation?", "205", ""),
    ("O07", "OPS", "Is there a security improvement program for large gaps, with a plan for time, cost, risks and gains?", "206", ""),
    ("O08", "OPS", "Does the IT team receive regular education about the risks (the why behind the changes)?", "204-205", ""),
    ("R01", "IR", "Are event, incident and nonconformity defined for the organization?", "207", ""),
    ("R02", "IR", "Does the response plan define roles, duties, prioritization by risk, documentation and notification method?", "208-209", ""),
    ("R03", "IR", "Are playbooks simple (scenario by scenario) and tested in tabletops with curveballs?", "62", ""),
    ("R04", "IR", "Are minor and major incidents defined, along with the legal notification obligations?", "210", ""),
    ("R05", "IR", "Are there external contacts (insurer, police, regulators, customers) and roles for C-suite, CISO, legal, HR, communications?", "211", ""),
    ("R06", "IR", "Are incident documents accessible even if the systems go down (copy outside the affected environment)?", "61", ""),
    ("R07", "IR", "Is there external response support (IR consultancy with hours contracted in advance) or reference guides (NCSC, ENISA, NIST SP 800-61, CREST)?", "209-212", "[DATED] confirm the guides' current revision"),
    ("R08", "IR", "Was the SIEM planned with requirements, pilot, scale, retention, rules and a list of what not to collect (PII, card data, passwords, keys)?", "216-218", ""),
    ("R09", "IR", "Was the 'normal' baseline built while avoiding the incorporation of threats already present?", "214-215", ""),
    ("R10", "IR", "Do the SIEM configuration and response policies have a recurring scheduled review?", "219", ""),
    ("W01", "SW", "Does the SDLC cover requirements, design, test plan, development and testing?", "227", ""),
    ("W02", "SW", "Do the requirements include security and privacy, with abuse cases (and misuse stories with care)?", "228, 235", ""),
    ("W03", "SW", "Are security tests planned before development?", "229", ""),
    ("W04", "SW", "Are secure development practices (input/output, errors, isolation, cryptography, access) trained and verified?", "232", ""),
    ("W05", "SW", "Is there code review (two-person principle) as part of defense in depth?", "233", ""),
    ("W06", "SW", "Is the minimum of the OWASP Proactive Controls verified (see the ASVS agent for depth)?", "233-242", "[DATED] controls version"),
    ("W07", "SW", "Do repositories have protected branches, sign-off and signed commits?", "249-250", ""),
    ("W08", "SW", "Does the CI/CD pipeline apply automatic scans and reduce production access to least privilege?", "250-251", ""),
    ("W09", "SW", "Are third-party libraries in the asset catalog, from maintained sources, and kept updated?", "235-236", ""),
]
IDS = [i[0] for i in ITEMS]
AREA_NAMES = dict(AREAS)

# Answer vocabulary: Portuguese (kept) + English aliases.
ANSWER_ALIASES = {"sim": "sim", "yes": "sim", "nao": "nao", "não": "nao", "no": "nao",
                  "parcial": "parcial", "partial": "parcial", "na": "na", "n/a": "na"}


def sel(area):
    if area:
        if area not in AREA_NAMES:
            print("ERROR: invalid area. Use: " + ", ".join(AREA_NAMES))
            sys.exit(2)
        return [i for i in ITEMS if i[1] == area]
    return ITEMS


def line(it):
    extra = (" " + it[4]) if it[4] else ""
    return "%s %s [from source] (DZ p.%s)%s" % (it[0], it[2], it[3], extra)


def cmd_areas():
    for k, v in AREAS:
        print("%-5s %s (%d items)" % (k, v, len([i for i in ITEMS if i[1] == k])))
    print("Total: %d items." % len(ITEMS))


def cmd_list(area):
    for it in sel(area):
        print("- " + line(it))


def cmd_markdown(area, title):
    print("# %s" % (title or "Information security strategy checklist (basis: DZ)"))
    print("")
    print("> The practice behind each item comes from the DZ (MacMillan, Packt, 2021) on the cited PDF page [from source]; the question form is [inference]. Mark yes/no/partial/NA. It does not replace a standard or legislation.")
    cur = None
    for it in sel(area):
        if it[1] != cur:
            cur = it[1]
            print("\n## %s" % AREA_NAMES[cur])
        print("- [ ] " + line(it))


def cmd_evaluate(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print("ERROR: could not read the JSON: %s" % e)
        return 2
    if not isinstance(data, dict):
        print("ERROR: the JSON must be an object {ID: answer}.")
        return 2
    bad = [k for k in data if k not in IDS]
    if bad:
        print("ERROR: unknown IDs: %s" % ", ".join(bad))
        return 2
    inv = [k for k, v in data.items() if str(v).lower() not in ANSWER_ALIASES]
    if inv:
        print("ERROR: answers must be sim/nao/parcial/na (or yes/no/partial/na): %s" % ", ".join(inv))
        return 2
    sc = {"sim": 1.0, "parcial": 0.5, "nao": 0.0}
    print("# Result by area (yes=1, partial=0.5, no=0; NA and unanswered are left out of the calculation)")
    gaps = []
    for k, name in AREAS:
        its = [i for i in ITEMS if i[1] == k]
        n = 0
        tot = 0.0
        for it in its:
            raw = str(data.get(it[0], "")).lower()
            v = ANSWER_ALIASES.get(raw, "")
            if not v or v == "na":
                continue
            n += 1
            tot += sc[v]
            if v != "sim":
                gaps.append((it, v))
        if n:
            print("- %-5s %3.0f%% (%d/%d answered) %s" % (k, 100 * tot / n, n, len(its), name))
        else:
            print("- %-5s  n/a  (0/%d answered) %s" % (k, len(its), name))
    print("\n## Gaps (%d)" % len(gaps))
    for it, v in gaps:
        print("- [%s] %s" % (v, line(it)))
    print("\nPrioritize the gaps by risk (DZ p.23, 33): the percentage is only a summary.")
    return 0


def main():
    ap = argparse.ArgumentParser(description="Security strategy checklist (DZ)")
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("areas")
    l = sub.add_parser("list")
    l.add_argument("--area")
    m = sub.add_parser("markdown")
    m.add_argument("--area")
    m.add_argument("--title", default="")
    e = sub.add_parser("evaluate")
    e.add_argument("file")
    a = ap.parse_args()
    if a.cmd == "areas":
        cmd_areas()
    elif a.cmd == "list":
        cmd_list(a.area)
    elif a.cmd == "markdown":
        cmd_markdown(a.area, a.title)
    elif a.cmd == "evaluate":
        return cmd_evaluate(a.file)
    else:
        ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
