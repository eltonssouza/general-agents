# 12. Side channels and advanced cryptographic engineering (Chs. 19 and 20)

Convention: "SE3 p.N" = PDF page; printed = PDF − 36 (ch. 19) and − 35 (ch. 20). PARTIAL reading. Ch. 19: read p.675-677, 685-686, 699-701; NOT read p.677-699 (timing, power, glitch, Rowhammer, Spectre, acoustic). Ch. 20: read p.702-709 (FDE, Signal), 712 and 716-717 (HSMs), 730-733 (crypto dreams, summary); NOT read Tor, the detail of API attacks on HSMs (xor-to-null-key etc.), enclaves and blockchains (p.709-711, 713-715, 718-729). Everything is from 2020: `[DATED]`.

## 1. Side channels (Ch. 19)
- `[from source]` *Side channel* = accidental leakage through a means not designed for communication; *covert channel* = deliberate leakage. Five families: (1) electromagnetic signals (Tempest; "after the Cold War it was realized that normally nobody was listening"), (2) leakage between tasks on a device (power/timing/contention; DPA delayed bank smartcards by 2-3 years), (3) Spectre/Meltdown (will force a redesign of superscalar CPUs in 2020-25), (4) shared local physical resources (phone listening to keyboard, laser on microphone), (5) shared social resources (SE3 p.675-676).
- **Prioritization:** "we underestimate the importance of some and spend irrational sums defending against others"; understanding the basics avoids missing scalable threats and avoids "chasing shadows" (SE3 p.676).
- Emsec/Tempest: embassies in hostile countries; the cleaning staff loosen the gaskets; Lockheed/Coast Guard 2007; attacks on smartphones (Goller & Sigl 2015) (SE3 p.685-686).
- **Social channels:** pizza deliveries at the Pentagon; a visit to a GUM clinic leaked because the insurer did not call for a routine check-up; "de-identification does not turn sensitive data into raw material"; privacy as **contextual integrity** (Nissenbaum): most harms come from information from one context ending up in another (SE3 p.699).
- **Summary and research:** which channels are a real threat depends on the application; "hardware verification did not see side channels"; timing in a CC EAL4+ certified TPM (2019) shows that you cannot trust brands or certificates (SE3 p.699-701).

## 2. FDE (SE3 p.703-705)
`[from source]` A key derived from a password allows offline attack; TPM limits attempts; cold boot (2008); poorly done factory reset on Androids (2015); in 2019 three third-party FDE products (60% of the market) were insecure and BitLocker turned itself off in their presence; encrypting S3 buckets may be just "tick-box" compliance because the typical failure is access negligence; abusability: FDE is a component of ransomware and users treat FDE as a "magic safe" and do not report a lost laptop (SE3 p.704-705).

## 3. Signal (SE3 p.705-708)
`[from source]` Forward secrecy and backward secrecy (post-compromise security); X3DH and double ratchet; the hard part is **initial authentication** (if the server swaps the identity key, "all bets are off"); the attacker needs to compromise the phone or steal the number (SIM swap, SS7); metadata and the anonymity set matter; *private contact discovery* via SGX (the original version swept 505m US numbers with 100 accounts in 25 days); governance of critical infrastructure of public interest (SE3 p.706-708).

## 4. HSMs (SE3 p.712, 716-717)
- `[from source]` When a trusted computer talks to a less trusted one, "expect the less trusted one to lie, cheat and probe the limits with unexpected combinations of commands" (SE3 p.712). HSM APIs with hundreds of transactions: "how can you be sure there is no chain of 17 transactions that leaks a key in the clear?" (SE3 p.712); EMV attack on an HSM secure-messaging transaction (SE3 p.716). Gemalto/PKCS#11 2019 by fuzzing the SDK emulator (SE3 p.716).
- `[from source]` **HSM risk management:** "someone has found an attack on at least one version of every security module on the market; root cause: *featuritis*"; rigorous configuration management, patches ready; banks have little HSM expertise; API vulnerabilities are independent of whether it is on-premises, cloud or enclave (SE3 p.716-717).

## 5. Failed dreams and summary (SE3 p.730-732)
- `[from source]` Blockchain voting (Moscow 2018; West Virginia 2018): "you don't fix elections with this technology because it doesn't attack the way they are stolen" (SE3 p.731).
- `[from source]` Lessons of ch. 20: (technical) crypto is not magic, has bugs and needs patching; (economic) HSMs cost more than servers, SGX has limits, mining has a CO2 cost; (political) advanced mechanisms get entangled with liability and regulation — "TANSTAAFL" (SE3 p.731-732).

## Triggers
- "Do I need an HSM/enclave?" → §4 and `references/14-biometria-e-tamper-resistance.md` (§ "what is worth protecting").
- Side-channel failure in a crypto implementation: NOT COVERED in detail by this agent (p.677-699 not read); recommend reading/an expert.
