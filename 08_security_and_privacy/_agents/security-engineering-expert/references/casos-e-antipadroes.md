# Real cases from the book and antipatterns

Convention: "SE3 p.N" = PDF page (printed = PDF − chapter offset; see `INDEX.md`). Each case is a summary, in our own words, of what the book reports on the cited page `[from source]`; "Lesson" and "Antipattern" are our organization `[inference]`. Incidents and numbers are from 2020 or earlier: `[DATED]`. Only cases that are on pages that were read are included (see coverage in `INDEX.md`).

## 1. Opponents and crime
| Case | What the book reports | Lesson / antipattern | Pages |
|---|---|---|---|
| EternalBlue / NotPetya / WannaCry | A tool of spies leaked in 2017 was reused by criminals and state actors | State tools end up with criminals; model this | SE3 p.67, 74, 84-85, 88 |
| Equifax 2017 | Struts patch not applied; 76 days of access; ≥145.5 million people | Antipattern: failed patching and inventory; avoidable | SE3 p.89 |
| Mirai and default passwords | Devices with factory passwords make up botnets | Antipattern: default password not reset | SE3 p.92, 147 |
| BEC / CEO fraud | Fraud through failing payment procedures at large badly managed or mid-size companies | Procedural controls would have prevented most | SE3 p.96-97 |
| VW and the lawsuit against academics | Manufacturer sued researchers and lost | Antipattern: reacting to disclosure with litigation | SE3 p.100-101, 1028-1031 |
| Intimate partner abuse | "All the usual advice is upside down" | Design for abusability | SE3 p.106-107 |

## 2. Psychology and passwords
| Case | Report | Lesson | Pages |
|---|---|---|---|
| 2007 IRS audit | 62 of 102 employees changed their password at the auditor's request | Social engineering works; training is not enough | SE3 p.132-133 |
| Greening 1996 | 138 of 336 students returned a valid password | Phishing exploits social trust | SE3 p.133-134 |
| Security questions (Palin 2008; Google) | Guessable or public answers | The system is as strong as its fallback | SE3 p.139-141 |
| Forced password change | >40% guessable from the previous one; NIST backed off in 2017 | Antipattern: periodic change policy | SE3 p.146-147 |
| Banks training customers to click | Links in email and calls asking for data | "Blame and train" does not work | SE3 p.148-150 |
| TENEX timing | Byte-by-byte comparison reduces attempts from A^N/2 to A·N/2 | Side channel in password verification | SE3 p.154 |
| NCA and DDoS-for-hire ads | Ads deterred demand for booters | Intervening at the human *choke point* | SE3 p.123 |

## 3. Protocols and cryptography
| Case | Report | Lesson | Pages |
|---|---|---|---|
| South African prepayment meter | Only remembered the last nonce; alternating tokens A and B recharged endlessly | Badly designed freshness | SE3 p.170, 541-542 |
| Immobilizers (TI DST, Keeloq, Hitag2, Megamos) | Broken 2005-2015 through protocol, key management, weak cipher and short keys | Test: try buying a spare key | SE3 p.172-173 |
| Relay on keyless cars | Thefts +56% in the UK in 2017 | Crypto does not solve distance; UWB | SE3 p.173-174 |
| Phantom withdrawals (Netherlands 1993; UK post chip-and-PIN) | 1980s assumptions stopped holding | The environment changes; revisit assumptions | SE3 p.181-182 |
| MIG-in-the-middle / IFF | Aircraft interrogation reflected | Include names in the challenge; authenticate the challenge | SE3 p.177-180 |
| Needham-Schroeder | Bob does not know whether the key is fresh | Displaced assumptions | SE3 p.185-186 |
| MD5/SHA-1 | Collisions published; in 2005 a driver was acquitted in Sydney for lack of attestation of MD5's security | Certificational threat also matters | SE3 p.229-230 |
| DigiNotar 2011 | Fraudulent wildcard certificates (Gmail; ~300,000 Iranian users) | Centralization amplifies damage; CT | SE3 p.241, 290-291, 765 |
| Padding oracle and Bleichenbacher RSA | Error oracles break implementations | Implementation errors > cryptanalysis | SE3 p.224-225, 235 |
| Dual_EC_DRBG / export | Weakened standard left vulnerabilities | Supply chain and standards | SE3 p.70-71 |
| Insecure FDE (2019) | Three third-party products (60% of the market) insecure | Trust neither brand nor certificate | SE3 p.704-705 |

## 4. Access control and systems
| Case | Report | Lesson | Pages |
|---|---|---|---|
| Morris worm / `finger` | 256-byte buffer | Memory safety | SE3 p.278-279 |
| Docker Hub containers (2019) | 194 of 1,000 images with blank root password | Insecure defaults at scale | SE3 p.272 |
| Migration to containers | Exposures because ACLs were forgotten | Antipattern: ACL external to the thing that changes | SE3 p.258 |
| Windows pre-2006 | Required admin to install; dialogs trained users to click | Usability and privilege | SE3 p.282-283 |
| Spectre/Meltdown | CPU optimization leaked across domains | Isolation has hardware limits | SE3 p.281-282 |
| 737 Max | Two sensors, one read; FAA delegated to Boeing; 346 dead | Redundancy does not cure bad design | SE3 p.299, 1054-1055 |
| 2001 truckers' strike | Dependency outside the mapped chain | Map dependencies | SE3 p.301-302 |
| £10m payment discarded | Duplicate transaction number | Uniqueness of names | SE3 p.313 |
| Bank linked accounts by name | Statement sent to the wife | Name semantics change | SE3 p.312 |

## 5. Economics and organizations
| Case | Report | Lesson | Pages |
|---|---|---|---|
| Lojack | US$100/year to the driver, social benefit US$1,500 | Positive externality underinvested | SE3 p.514 |
| Windows and platforms | "Ship fast, fix it in v3" is rational | Platform incentive | SE3 p.338-340 |
| Bookmakers extorted by DDoS | US$10-50 thousand; Akamai + police solution | DoS and extortion | SE3 p.302-303 |
| Privacy paradox | Assurances led to disclosing less | Salience of risk | SE3 p.349-350 |

## 6. Policies and data
| Case | Report | Lesson | Pages |
|---|---|---|---|
| Vault 7 | Cyberweapons without compartmentation; shared password; JWICS without 2FA | Antipattern: no compartments and no monitoring | SE3 p.389 |
| NPfIT | ~£10bn; RBAC + relationship gave the receptionist the psychiatric notes | A single record with a single context was a bad idea | SE3 p.400-401 |
| HES and DeepMind/Royal Free | Data sold to >1,000 organizations; secondary use | Consent and transparency | SE3 p.402-405 |
| Sweeney, AOL, Netflix | Reidentification from a few attributes | Anonymization is fragile | SE3 p.428-430 |
| 2020 census (US) | Reconstruction of microdata through equations | DP and privacy budget | SE3 p.435-436 |
| Wildbook (leopards) | Abstracted data can be more sensitive | Sensitivity comes from context | SE3 p.389-392 |
| Safe Harbour / Privacy Shield | Struck down in 2015 and 2020 | The regime changes; confirm | SE3 p.991-992 |

## 7. Banks and payments
| Case | Report | Lesson | Pages |
|---|---|---|---|
| Lloyds / "Fizzy" | Insider charged the victim's authenticator code (£113m) | Insider and 2FA | SE3 p.456-457 |
| Barings, Maxwell, Wells Fargo, Wirecard | Executive fraud; €2.1bn not found | Verify the balance with the bank (audit 101) | SE3 p.457-458, 461-462 |
| Post Office / Horizon | 587 sub-postmasters won £58m in 2019 | Legal presumption that the accounting system is correct | SE3 p.459-460 |
| Bangladesh Bank 2016 | US$81m diverted; US$851m blocked | Attack on the gateway, not on SWIFT | SE3 p.469 |
| Rifkin 1979; Johannesburg 1986 | Codes by phone defeat dual control | Business processes | SE3 p.470-471 |
| Postbank (South Africa) | PIN key copied from a laptop; R56m | Real key ceremony | SE3 p.473-474 |
| Munden and Badger | Bank claimed an infallible system | Non-repudiation and burden of proof (Regulation E vs UK) | SE3 p.478-479 |
| EMV No-PIN and pre-play | Unverified flag; "unpredictable number" was a counter | Protocol implemented without checking | SE3 p.492-494 |
| Tesco Bank 2016 | £2.2m from 8,261 accounts; £16.4m fine | Fraud engine and weekend processes | SE3 p.496-497 |
| CAP (PIN calculator) | Possible cause of homicides: negligent design | Security that harms customers | SE3 p.500-501 |

## 8. Physical, metering, biometrics, tamper
| Case | Report | Lesson | Pages |
|---|---|---|---|
| Hackensack / Tulsa | Alarm cable cuts (US$2.1m in watches; 50,000 homes) | Alarm DoS; anonymous and redundant communications | SE3 p.532-533 |
| TSA | ~20% of threats get through if tested several times per shift; 60-75% if once | False alarms tire guards | SE3 p.533-534 |
| STS: lightning, brown-out | Maximum credit on failure | Prolonged field testing | SE3 p.541-542 |
| UK/Ontario smart meters | £20bn projected; 12.5 million installed and 39 million still to install at the end of 2018 | Divergent incentives | SE3 p.543-546 |
| Trujillo experiment | 71 experts no better than chance | Tamper detection is hard | SE3 p.603 |
| Petrov 1983 | False alert of nuclear attack | Beware of cyberattacks on ISR | SE3 p.580-581 |
| Matsumoto 2002 (gelatin) | 11 readers fooled | Liveness | SE3 p.620 |
| Newham and Tampa (face) | "Security theatre" | Old face recognition ineffective | SE3 p.612-615 |
| PDF "signed by Amazon" | Bypass in 21 of 22 viewers | Untrusted interface | SE3 p.667-668 |

## 9. Network and telephony
| Case | Report | Lesson | Pages |
|---|---|---|---|
| Network with SSH and trust | SSH keys create trust among thousands of machines | Do not trust the local network | SE3 p.748-749 |
| IDS and base rate | 10 attacks/million, 0.1% → ratio 100 | Calculate first | SE3 p.759-760 |
| SIM swap and SMS 2FA | Operators swap SIMs with little control | Dependence on third parties | SE3 p.794-795, 183-184 |
| FordPass | Control of the car months after return | Revocation | SE3 p.808-809 |

## 10. Development, assurance and AI
| Case | Report | Lesson | Pages |
|---|---|---|---|
| Challenger | Failure of risk analysis/organization | FMEA and reporting culture | SE3 p.1005 |
| London Ambulance; Y2K | Misunderstood requirements; Y2K counterexample | Design failures are requirements failures | SE3 p.1033-1034 |
| Dieselgate | Manufacturer enters the threat model | Model the supplier | SE3 p.1075-1080 |
| ISO 27001 | Almost every large breach occurs at a certified firm | Checklist ≠ security | SE3 p.463, 1034-1036, 1066 |
| Recall of 465,000 pacemakers | Update as part of product security | Safety and security entangled | SE3 p.1075-1080 |
| Tay (Microsoft, 2016) | Shut down in 16 hours after poisoning | Training data can be manipulated | SE3 p.909 |
| Stickers and signs | Car reads 30 mph as 60 | Adversarial samples | SE3 p.909-910 |

## Cross-cutting antipatterns (summary `[inference]`)
1. Protecting the wrong thing (9/11: knives allowed; policy, not mechanism) — SE3 p.52.
2. *Security theatre* — SE3 p.53.
3. Trusting the weakest fallback (account recovery, stripe after chip) — SE3 p.141, 302-303.
4. Protecting the wrong resource against the wrong opponent — SE3 p.533-534.
5. Declaring the system infallible — SE3 p.463-464, 478-479.
6. Blaming and training users instead of designing — SE3 p.150, 752.
7. Dual control defeated by a business process — SE3 p.470-471.
8. Checklist/certification as assurance — SE3 p.1034-1036, 1063-1065.
9. Keys and identifiers with an effective space smaller than the nominal one — SE3 p.170, 172-173.
10. Environmental assumptions that change silently — SE3 p.181-182, 284-285.
11. Anonymization as a magic solution — SE3 p.418, 443.
12. DoS that pushes to an insecure fallback — SE3 p.302-303.
