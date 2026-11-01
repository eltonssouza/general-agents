# -*- coding: utf-8 -*-
"""
incident_templates.py - templates for an incident response plan, postmortem, recovery checklist and meeting agendas,
assembled from what the BSRS (chs. 16-18) actually contains. Each section cites PDF pages (BSRS p.N).

IMPORTANT (fidelity): the book does NOT include a literal template for an IR plan or a postmortem. It provides content
lists (ch.16: p.407-409), security postmortem questions and action items (ch.18: p.472-473), the recovery
checklist template (Figure 18-1, p.465) and meeting agendas (ch.17: p.441, 444-445). These templates organize
those items; the structure is [inference]; the items come from the cited pages. General blameless postmortem is SRE: see sre-practices-expert.

Usage (Python 3, stdlib, no network; run with `python -I`):
  python -I scripts/incident_templates.py list
  python -I scripts/incident_templates.py plan [--org NAME]
  python -I scripts/incident_templates.py postmortem [--incident ID]
  python -I scripts/incident_templates.py recovery-checklist
  python -I scripts/incident_templates.py agenda kickoff|sync|handover
  python -I scripts/incident_templates.py declaration
  python -I scripts/incident_templates.py opsec
  python -I scripts/incident_templates.py ic-loop
  python -I scripts/incident_templates.py all [--out DIR]
"""
import argparse
import io
import os
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass

NOTA = ("> Source: *Building Secure and Reliable Systems* (BSRS), PDF pages (printed = N − 36). Items are `[from source]`; "
        "the organization of the template is `[inference]`. It does not replace legal/regulatory advice; notification deadlines are not in the book.\n")


def plan(org):
    return """# Incident response plan — %(org)s

%(nota)s
## 1. Mission and scope (charter)
- Mission in one sentence: the types of incidents the team handles (BSRS p.405).
- Scope: environment (technologies, users, products, stakeholders); what is handled internally and what is outsourced (BSRS p.405).
- Adequate morale and workload; scope agreement with leadership and a champion (BSRS p.405).
- Definition of success: when the IR work is done; incident exit criteria (BSRS p.401, 405).

## 2. Team and roles (roles, not individuals)
- Incident commander; SREs; public relations; customer support; legal; privacy engineers; forensic specialists; security engineers (BSRS p.403-404).
- Staffing model: dedicated, dual-role or outsourced; the forensic part can be outsourced (with a risk of unavailability) (BSRS p.403).
- Delegates with authority to approve emergency fixes, changes and messages, across multiple time zones (BSRS p.404).
- Senior champion who commits resources (BSRS p.404-405). Shifts to reduce fatigue (BSRS p.404).
- Crisis roles (IMAG/ICS): IC, operations lead, communications lead, remediation lead, management liaison, legal lead (BSRS p.429-430, 438).

## 3. Severity and priority models
- Severity (0-4; 0 = most severe): impact on the organization; example from the book: unauthorized individuals on the network = 0; temporary unavailability of security logs = 2 (BSRS p.405-406).
- Priority (0-4; 0 = immediate response before any other work; 4 = routine work); severity tends to stay fixed and priority changes over the course of the incident (BSRS p.406).
- A model common to all teams to avoid different response times (BSRS p.406).

## 4. Operational parameters
- Expected initial response time (e.g., 5 min, 30 min, 1 h, next business day) (BSRS p.406).
- Time for initial triage and a response plan with an operational agenda (BSRS p.406).
- SLOs that indicate when IR interrupts day-to-day work; on-call rotations (principles: sre-practices-expert) (BSRS p.406-407).

## 5. Response plan content
- Incident reporting; triage (who responds to the initial report); SLOs; roles and responsibilities; outreach to engineering teams (BSRS p.407).
- Communications: informing leadership (channel and content); intra-organization communication (chat, video conference, email, secure IRC, bug tracker); external parties (regulators, police) with legal and a contact index; customer support; communicating without alerting the adversary if the channel is unavailable or compromised (BSRS p.407-408).
- Backup channels are mandatory: the adversary may get onto the distribution list of a compromised email (BSRS p.408).
- Criteria for notifying senior leadership and engaging local engineering (BSRS p.409).

## 6. Playbooks (per team, procedural, reviewed frequently)
- Temporary emergency access; log extraction and analysis; failover and when to apply graceful degradation (BSRS p.409).
- Store the documentation where it stays accessible in a disaster and up to date; incident tracking system (need-to-know for security and privacy) (BSRS p.409).

## 7. Prestaging
- IR access levels and emergency escalation defined in advance; read access to logs and tools (BSRS p.410).
- Fault tolerance and failovers; forensic agents with logs enabled and long retention (~200 days to detect intrusions; consult legal about legal limits); hardware/software to restore backups and restore drills; alternative access paths and trusted air-gapped systems (BSRS p.410-411).
- OpSec plan defined before the incident (BSRS p.430-432).

## 8. Training
- IR team: severity/priority models, operating model, response times, location of plans and playbooks (BSRS p.411).
- Other engineers: IMAG roles; recognize, report and escalate; finite window before escalating (e.g., 15 min); decision criteria defined beforehand; competing priorities (uptime vs forensic preservation); take notes on activities to separate them from the attacker's (BSRS p.411).

## 9. Processes
- Fast hardware/software acquisition; pre-approved outsourcing contracts; preserve evidence and logs (BSRS p.412).

## 10. Testing and evaluation (at least annually)
- Audit automation (backups, logs, patches, alerts, communication) (BSRS p.412-413).
- Tabletops (believability, details, decision points ~10-20 per 60 min, interactive participants, outcomes with owners) (BSRS p.414-415).
- Production tests: fault injection, loss of key people, multi-component failures, full failover; Red Team (BSRS p.415-417).
- Evaluate: measure times, blameless postmortem, feedback loops, keep logs, evaluate "failed" tests, Purple Team (BSRS p.418).

## 11. During the incident (operational summary)
- Triage; do not panic; declare the incident and the IC; OpSec; investigate before fixing; parallelize; shifts of at most 12 h; formal handover; close with an outbrief (BSRS p.424-433, 437-441, 450).
- Recovery and post-incident: use `recovery-checklist` and `postmortem` (BSRS p.459-473).
""" % {"org": org, "nota": NOTA}


def postmortem(inc):
    return """# Security incident postmortem — %(inc)s

%(nota)s
> The book does not include a literal postmortem template: it presents questions and guidance on action items (BSRS p.472-473). General blameless format: SRE book (sre-practices-expert).

## 1. Summary
- What happened, impact, duration, who declared and when; final severity and priority (BSRS p.405-406).

## 2. Timeline (forensic timeline)
- Chronological list of events centered on the incident events, to determine correlation and causality (BSRS p.435).
- Include the entry point, the pivot points investigated and the attacker's actions (BSRS p.435-436); separate the investigators' actions from the attacker's (BSRS p.375-376, 411).

## 3. Detection and response
- Was it detected by an expected technology control (e.g., IDS)? If not, how can detection be improved? (BSRS p.472)
- How quickly was it detected and responded to? Is that within an acceptable range? How can response time be improved? (BSRS p.472)
- OpSec, communication and handover decisions; what worked and what did not (BSRS p.430-441).

## 4. Root cause analysis
- Main contributing factors; variants and similar problems elsewhere in the environment (BSRS p.472).
- What tests or audits should have detected these factors earlier? Is it possible to create them? (BSRS p.472)
- Was the important data protected enough to deter the attacker? What new controls? (BSRS p.472)

## 5. Recovery
- Did the recovery team use the tools well (versioning, deploy, test, backup, restore)? (BSRS p.472)
- What normal procedures (testing, deploy, release) were bypassed during recovery? What remediation to apply now? (BSRS p.473)
- Temporary infrastructure or tooling changes that need refactoring; short-term mitigations accepted as technical debt: when to remove them, who pays, how to flag them, how to prove they can be removed (BSRS p.463, 473).
- Quarantined assets: were they remediated securely and permanently? (BSRS p.466)
- Bugs opened during the incident and the recovery (BSRS p.473).

## 6. Action items (explicit owners; sorted into short and long term)
- Short term ("low-hanging fruit"): e.g., add 2FA, reduce the time to apply patches, create a vulnerability discovery program (BSRS p.473).
- Long term (posture strategy): e.g., dedicated security team, backbone encryption, change OS choices (BSRS p.473).
- Document the deadlines and effort of each item and which roadmap it belongs to (BSRS p.472).
- Industry and peer best practices that would have helped prevent, detect or respond (BSRS p.473).

| # | Action | Owner | Deadline | Horizon (short/long) | Cause reference |
|---|--------|-------|----------|----------------------|-----------------|
| 1 |        |       |          |                      |                 |

## 7. Closure
- Review with legal and leadership; outbrief with the team and communication of the closure to all teams involved (BSRS p.450).
- Review the rewards system that may have led to the emergency (BSRS p.519).
""" % {"inc": inc, "nota": NOTA}


def recovery():
    return """# Recovery checklist (Figure 18-1 template)

%(nota)s
> The figure (p.465) is an image; its content was read visually on the page and is not verifiable by text.

## Instructions (color code, BSRS p.465)
- Highlight in **GREEN** when DONE.
- Highlight in **ORANGE** the TO-DO items.
- Highlight in **RED** if the task cannot be completed; it must be replaced by an equivalent action.
- Highlight in **BLUE** if the task will not be completed because it is operationally risky; adjustments are needed.

## Incident commander (BSRS p.465)
- Give a "hands off keyboards" briefing (everyone's full attention; BSRS p.464, note).
- Present an overview of the tasks and constraints.
- Tell everyone involved the exact time at which remediation will start.

## In order of operation, the remediation lead starts execution (BSRS p.465)
1. [Team name #1]: task description
   - a. Detailed commands or steps
2. [Team name #2]: task description
   - a. Detailed commands or steps
3. [Team name #3]: task description
   - a. Detailed commands or steps
4. [Team name #4]: task description
   - a. Detailed commands or steps

## Also include (BSRS p.464)
- Specific tools and commands; cleanup and rollback procedures in case the plan fails; tasks claimed by skill; parallelizable items marked.

## Planning questions before executing (BSRS p.459-464)
1. How will the attacker respond to the recovery? Avoid ejecting without understanding the attack, unless it is already doing something dangerous (BSRS p.459-460).
2. Are the recovery infrastructure and tools compromised? Recover in a clean, isolated environment (BSRS p.460-461).
3. What variants of the attack exist (same vector on other systems; related classes)? (BSRS p.461)
4. Will the recovery reintroduce vectors (golden images, contaminated configs and backups)? Determine the timeline (BSRS p.462).
5. What mitigations, and what technical debt does each one create? (BSRS p.462-464)

## Checklist examples from the book (read from the figures)
- Compromised cloud instances (Figure 18-2, p.474): vulnerability scan; fix software; deploy new instances in parallel; disable the compromised ones and archive or delete.
- Large-scale phishing (Figure 18-3, p.476): 2FA for email; lock email accounts until reset and 2FA; 2FA adoption and password resets with the helpdesk; 2FA for VPN and cloud.
""" % {"nota": NOTA}


AGENDAS = {
    "kickoff": """# Incident kickoff meeting agenda (BSRS p.444-445)

%(nota)s
1. [IC] Designate a note taker.
2. [IC] Introductions, starting with the IC: name, team, role.
3. [IC] Rules of engagement: confidentiality; OpSec concerns; who decides and who should or should not take part in decisions; tell the lead when switching tasks or finishing something.
4. [IC] Describe the status: what problem are we solving?
5. [All] Discuss the problem.
6. [IC] Summarize actions and owners.
7. [IC] Ask the group: do we need more resources? Other groups? What blockers?
8. [IC] Set the time of the next sync and the expected attendance (required and optional).
""",
    "sync": """# Ongoing sync meeting agenda (BSRS p.445)

%(nota)s
1. [IC] Designate a note taker.
2. [IC or OL] Summarize the current status.
3. [IC] Receive updates from each participant or workstream.
4. [IC] Discuss next steps.
5. [OL] Assign tasks and ask each person to repeat what they will do.
6. [IC] Set the times of the next meetings (every two or four hours, BSRS p.444).
7. [OL] Update the action tracker.
""",
    "handover": """# Incident handover agenda (BSRS p.441)

%(nota)s
Before: prepare tracking documentation, evidence notes and records; agree on logistics, time and method; shifts of at most 12 hours (BSRS p.439, 441).
1. [Outgoing IC] Designate a note taker, preferably from the incoming team.
2. [Outgoing IC] Summarize the current status.
3. [Outgoing IC] Describe the tasks they would do in the next 12 hours if they were not handing over the incident.
4. [All] Discuss.
5. [Incoming IC] Describe the tasks they expect to handle in the next 12 hours.
6. [Incoming IC] Set the time(s) of the next meetings.
A formal handover is also done from each lead (ops, comms, etc.) to their replacement (BSRS p.441).
""",
}


def declaration():
    return """# Incident declaration and initial briefing

%(nota)s
- Formula from the book: "Our team is declaring an incident involving X, and I am the incident commander (IC)." Declaring explicitly aligns expectations (BSRS p.429).
- If the IC is chosen, the designation is explicit and the designee explicitly acknowledges acceptance (BSRS p.429).
- Tell executives that teams may ignore or bypass normal processes until containment (BSRS p.429).
- The IC notifies: an incident occurred; will take the IC role; needs support to investigate (BSRS p.447).
- Before communicating by email/chat, apply OpSec (BSRS p.430-433, 447).
""" % {"nota": NOTA}


def opsec():
    return """# OpSec briefing for response members (ch.17)

%(nota)s
**Rules to document and to be acknowledged in writing by each member (BSRS p.431):**
- What is confidential and which channels to use; if email is in scope, do not use email about the incident (BSRS p.430-431).

**Common mistakes to avoid (BSRS p.431-432):**
- Communicating or documenting the incident in a medium the attacker can monitor.
- Logging into compromised servers (exposes credentials).
- Connecting to the attacker's command-and-control servers, downloading their malware from the investigation workstation, port scanning or domain lookups.
- Locking accounts or changing passwords of affected users before the investigation is complete.
- Taking systems offline before understanding the scope.
- Accessing the analysis workstations with credentials the attacker may have stolen.

**Good practices (BSRS p.432):**
- In-person meetings when possible; if using chat or email, use new machines and infrastructure.
- Remote agents or key-based access to collect evidence without revealing login secrets.
- Be specific about confidentiality when asking for help.
- For each step, consider the conclusions a savvy attacker would draw.
- Write domains and indicators as example[dot]com so tools do not expand them (BSRS p.432-433).

**Exception (BSRS p.433):** an imminent, clearly identifiable risk (critical system, trivial and known vulnerability) may justify shutting the system down, knowing that this gives away the response.
""" % {"nota": NOTA}


def icloop():
    return """# Incident commander loop (ch.17, BSRS p.438)

%(nota)s
While the incident is ongoing:
1. Check with each lead: status; new information others need; blockers; need for staff or resources; overload; upcoming problems; fatigue of each lead and each team.
2. Update status documents, dashboards or other sources of information.
3. Are the relevant stakeholders (executives, legal, PR, etc.) informed?
4. Do you need help or additional resources?
5. Are there parallelizable tasks waiting?
6. Is there enough information for remediation and cleanup decisions?
7. How much time does the team need until the next round of updates?
8. Is the incident over? If not, go back to the start.
Addendum: OODA (observe, orient, decide, act) for decisions (BSRS p.438). The IC does not operate: if you are looking at logs, step back (BSRS p.437).
""" % {"nota": NOTA}


def build(kind, args):
    if kind == "plan":
        return plan(args.org)
    if kind == "postmortem":
        return postmortem(args.incident)
    if kind == "recovery-checklist":
        return recovery()
    if kind == "declaration":
        return declaration()
    if kind == "opsec":
        return opsec()
    if kind == "ic-loop":
        return icloop()
    if kind.startswith("agenda-"):
        return AGENDAS[kind.split("-", 1)[1]] % {"nota": NOTA}
    raise SystemExit("unknown template: " + kind)


KINDS = ["plan", "postmortem", "recovery-checklist", "agenda-kickoff", "agenda-sync", "agenda-handover", "declaration", "opsec", "ic-loop"]


def main():
    ap = argparse.ArgumentParser(description="IR plan, postmortem and checklist templates (BSRS chs. 16-18)")
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("list")
    p = sub.add_parser("plan")
    p.add_argument("--org", default="[ORGANIZATION]")
    p = sub.add_parser("postmortem")
    p.add_argument("--incident", default="[INCIDENT ID]")
    sub.add_parser("recovery-checklist")
    p = sub.add_parser("agenda")
    p.add_argument("kind", choices=["kickoff", "sync", "handover"])
    sub.add_parser("declaration")
    sub.add_parser("opsec")
    sub.add_parser("ic-loop")
    p = sub.add_parser("all")
    p.add_argument("--out", help="output directory; without it, prints everything")
    p.add_argument("--org", default="[ORGANIZATION]")
    p.add_argument("--incident", default="[INCIDENT ID]")
    a = ap.parse_args()
    if a.cmd in (None, "list"):
        print("Templates: " + ", ".join(KINDS))
        return
    if a.cmd == "all":
        ns = argparse.Namespace(org=a.org, incident=a.incident)
        if a.out:
            os.makedirs(a.out, exist_ok=True)
            for k in KINDS:
                path = os.path.join(a.out, k + ".md")
                with io.open(path, "w", encoding="utf-8", newline="\n") as f:
                    f.write(build(k, ns))
            print("wrote %d templates to %s" % (len(KINDS), a.out))
        else:
            for k in KINDS:
                print(build(k, ns))
                print("\n---\n")
        return
    kind = a.cmd if a.cmd != "agenda" else "agenda-" + a.kind
    sys.stdout.write(build(kind, a))


if __name__ == "__main__":
    main()
