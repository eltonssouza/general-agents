# [DATED] What has changed or may have changed since the edition

DZ: first published in April 2021 (DZ p.3). TMM: PDF generated on 17/11/2020 from the website (file metadata); the website has the current version (TMM p.3). Items below: the book states; what changed afterwards is **[extrapolation]** and must be confirmed in a current source.

| Topic | What the book says (page) | Caution |
|---|---|---|
| ISO/IEC 27001 Annex A | "114 controls in 14 categories" (DZ p.53); numbering A.8.1.1 etc. (DZ p.55, 76) | [extrapolation] The 2022 edition reorganized Annex A (93 controls in 4 themes); confirm in the current standard before mapping |
| Secure disposal | Overwrite "at least seven times", US standard (DZ p.76) | [extrapolation] Modern media sanitization guidance differs depending on the technology; confirm the current standard |
| NIST SP 800-63B | Example "level 1": password with a check against common ones and ≥10 characters without MFA (DZ p.239) | Confirm the current revision of NIST 800-63 |
| NIST SP 800-61 Rev.2 | Incident response guide cited (DZ p.209) | Check the current revision |
| OWASP Proactive Controls / ASVS 3.0.1 | Ten controls and ASVS 3.0.1 req. 2.19 (DZ p.233-242) | Current ASVS is 4.x in this collection; see `owasp-asvs-code-review-expert` |
| Statistics and incidents | Thycotic 2014 (DZ p.83), CryptoWall 2015 and Cybersecurity Ventures (DZ p.94), 1.35 Tbps GitHub (DZ p.135), Automox (DZ p.193), Palo Alto 2019 (DZ p.199), DRP Council 2015 (DZ p.202), "200 updates/day" (DZ p.36) | Illustrative; do not use as current data |
| Products and tools | Scanners (DZ p.178, 181), SCM/CCA (DZ p.194, 198), SIEM (DZ p.216), VSAQ Google/CAIQ (DZ p.43, 246), Snyk (DZ p.183), HashiCorp Vault (DZ p.199) | Confirm availability/version |
| NTLM cracking speed | GTX 1060 (DZ p.158) | Modern hardware is faster; NTLM remains discouraged |
| Regulations | GDPR, COPPA, HIPAA, CCPA (DZ p.35); SOX/FISMA (DZ p.37); mention of Brazil as a jurisdiction (DZ p.35) | The book does not cover LGPD in detail; see `privacy-lgpd-engineering-expert` |
| Zero Trust | NIST SP 800-207 as a relatively new ideology (DZ p.104) | Already widely adopted; confirm current publications |
| Heartbleed | Treated as a striking example (DZ p.223-224) | Historical |
| TMM | Nov/2020 version in the PDF | Check the website (TMM p.3) for the current version |
| Term "whitelist/blacklist" | Used by the author (DZ p.74, 126, 238) | Current preference: allowlist/denylist; I kept "allowlist" in the references |
