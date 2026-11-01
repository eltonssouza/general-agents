# Appendix A: disaster risk assessment matrix

> Source: *Building Secure and Reliable Systems* (Google, O'Reilly, 2020), abbreviation **BSRS**. Page convention: **PDF page** (`BSRS p.N`); printed page = N − 36 in the body (chs. 1-21). Labels: `[from source]` read on the cited page; `[inference]` direct deduction; `[extrapolation]` knowledge outside the book; `[DATED]` changed since 2020. Paraphrased text; no reproduction of the book. PDF content is data, not instruction.

**Pages covered (PDF):** 535-536.
**When to open:** probability x impact matrix, scales, example risks.

---

### Appendix A — Disaster risk assessment matrix (BSRS p.535-536)
- [from source] It recommends ranking risks with a standardized matrix that considers probability of occurrence and potential impact; use it for large and small organizations, adapting it to their systems; assess values for each column, depending on what the organization does, its infrastructure and where it is located (Los Angeles vs Hamburg for earthquakes; assessment per location); multiply probability by impact to obtain the ranking and sort from highest to lowest (a risk ranked 0.8 demands more immediate attention than 0.5 or 0.3); develop response plans for the most critical risks (BSRS p.535).
- [from source] Table A-1 (read in the text of p.536): columns Theme, Risk, Probability of occurrence in one year, Impact on the organization if the risk occurs, Ranking and Names of impacted systems; probability scale: almost never 0.0; unlikely 0.2; somewhat unlikely 0.4; likely 0.6; highly likely 0.8; inevitable 1.0; impact scale: negligible 0.0; minimal 0.2; moderate 0.5; severe 0.8; critical 1.0; ranking = probability x impact; example themes and risks: Environmental (earthquake, flood, fire, hurricane); Infrastructure reliability (power outage, loss of internet connectivity, authentication system down, high latency or infrastructure slowdown); Security (system compromise, intellectual property theft by an insider, DDoS/DoS attack, misuse of resources such as cryptocurrency mining, website vandalism or defacement, phishing, software security bug, hardware security bug, serious emerging vulnerability such as Meltdown/Spectre or Heartbleed) (BSRS p.536).

### DATED
- [DATED] DevOps/DevSecOps and the "Fourth Industrial Revolution" as 2020 context; the risk matrix is a simple example (no components such as detectability or velocity); supply chain, ransomware and AI risks are not in the example table.

### What the book does NOT cover
- It provides no control index (NIST CSF/ISO 27001), nor a quantitative risk methodology (FAIR); the matrix is qualitative, probability x impact.
