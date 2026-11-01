# 4.5 Authorization testing (WSTG-ATHZ-01 to ATHZ-04)

Pages = PDF (WSTG p.N; printed = N − 2). Paraphrased; the directory traversal strings and encodings of the guide are **not** reproduced here (use the original text, p.171-174, in an authorized engagement). See also `validacao-de-entrada-inpv-parte1.md` and `validacao-de-entrada-inpv-parte2.md` for injections.

## WSTG-ATHZ-01 Directory traversal and file inclusion (p.170-174)
- **Objectives** [from source]: identify injection points related to path traversal and assess bypass techniques and the extent of the problem (p.170).
- Context: the application confines files to a "web root", but poorly validated inputs (form parameters, cookies) allow reading/writing files outside it or including external files (p.170). Two stages: **enumeration of input vectors** and **testing techniques** (p.170).
- Enumeration: file operation parameters, unusual extensions, interesting variable names, cookies that assemble pages/templates (p.171).
- Techniques: the tester needs to know the target system (there is no point requesting a Unix file from an IIS) (p.171); there is also inclusion of external files and use of protocols as an argument to probe the local file system or local services (p.171); revealing the source of a CGI without traversal characters (p.172). The guide teaches that developers often handle only the basic encodings; if one does not work, try another scheme (p.172). There are considerations of URL/double URL encoding, UTF-8 and Windows peculiarities (separators, UNC paths, device namespace) (p.172-173). `[extrapolation]`: for strategies beyond the guide, see ASVS (forward to `owasp-asvs-code-review-expert`).
- Gray-box: review code for include and file functions (PHP, JSP, ASP) with `grep`; values coming from the database can also be used in an include; functions that "fix" invalid input are prone to failures (p.173-174).
- Tools: DotDotPwn, WFuzz lists, ZAP, Burp, DirBuster (p.174).

## WSTG-ATHZ-02 Bypassing the authorization schema (p.175-179)
- **Objective**: assess whether **horizontal** or **vertical** access is possible (p.175).
- Questions per function and role: access without authentication? after logout? to functions of another role? administrative functions by a regular user? (p.175).
- **Horizontal** (same role, another identity): create two users with identical privileges, keep two sessions, swap parameters and the session identifier from token 1 to token 2 and compare responses; it is vulnerable if the response has the same private data or indicates success on someone else's data (p.175-176).
- **Vertical** (higher role): register users, keep sessions of distinct roles, swap the identifier and check whether the weaker role obtains data or runs functions of the stronger role; the guide illustrates with a table of banking roles (Administrator, Manager, Staff, Customer) (p.176-177). Note: validation only in the interface (GUI) and not in the function is a common flaw (p.177).
- Sub-tests: access to administrative functions (p.178), resources assigned to another role (e.g., resumes in a bucket) (p.178), **handling of special headers** such as `X-Original-URL` and `X-Rewrite-URL` (first detect whether there is support by comparing the response to a nonexistent resource) and forwarding/IP headers (`X-Forwarded-For` etc.) with localhost or private-network values (p.178-179).
- **Remediation**: principle of least privilege in users, roles and resources (p.179). Tools: ZAP (Access Control Testing add-on), Burp, AuthMatrix and Autorize extensions (p.179). Cross-reference: ASVS 4.0.1 (p.179).

## WSTG-ATHZ-03 Privilege escalation (p.180-182)
- **Objectives**: identify injection points related to privilege manipulation and try to bypass security measures (p.180).
- Definition of the guide: vertical = accessing resources of more privileged accounts; horizontal = resources of equivalent accounts (p.180).
- Procedure: record every functionality in which the user creates, receives or deletes data and try to access it with another identity (p.180). Variations: manipulation of user group (group and request parameters), of profile (hidden field with profile), of **condition value** (server response with implicit trust), of IP address (forwarding header used as the client IP), URL traversal (p.180-181). White-box: authorization check by partial URL match (startswith, contains etc.) and weak session ID derived from a predictable hash (p.182).
- Tool: ZAP (p.182).

## WSTG-ATHZ-04 Insecure direct object references (IDOR) (p.183-184)
- **Objectives**: identify object reference points and assess the access control (p.183).
- Map all places where user input directly references objects (database row, file, page); the best practice is to have **at least two users** (and, if relevant, different privileges) to try to access others' objects (p.183).
- Four scenarios of the guide: value used to obtain a database record (e.g., invoice number); to execute an operation on the system (e.g., changing another user's password, usually in a wizard); to obtain a file (often combined with path traversal); to access functionality (menu item) (p.183-184). Note: the reference may be split across more than one parameter (p.184).
