# 03. Security protocols (Ch. 4)

Convention: "SE3 p.N" = PDF page; printed = PDF − 47. Reading: ch. 4 in full.

## 1. Evaluating a protocol
- `[from source]` Protocol = steps that principals use to establish trust relationships; it is where cryptography and access control meet (SE3 p.166). Two questions: is the threat model realistic? Does the protocol deal with it? (SE3 p.167).
- `[from source]` Protocols fail because of assumptions that change over time (see §5) and often more through protocol bugs than through cryptanalysis (SE3 p.170, 190).
- `[from source]` "Don't design your own protocols; ask an expert and publish for peer review; even experts get the first version wrong" (SE3 p.190).

## 2. Remote control and tokens (SE3 p.167-171)
- Serial number as password, replay ("grabber"), 16-bit codes (average 2^15 attempts; < 1 h at 10/s), 32 bits does not solve replay; PT2262 garage chip (3^12 codes) (SE3 p.167-168).
- Notation: T→G: T,{T,N}KT; nonce N guarantees freshness (random, counter, challenge, timestamp, with trade-offs in cost and replay resistance); key diversification KT = {T}KM (SE3 p.169). A 128-bit key derived from a 16-bit device number has only 2^16 keys (SE3 p.170).
- South African prepayment meter that only checked whether the nonce differed from the last one: alternating two tokens A and B recharges indefinitely (ABAB...) (SE3 p.170). A 16-bit counter with a resynchronization window can be broken with 6 well-chosen codes (SE3 p.170-171). Random vs counter: memory to remember codes vs resynchronization (SE3 p.170-171).
- Security does not always protect the owner: access control of accessories (printers) serves business models (SE3 p.171).

## 3. Challenge-response and immobilizers (SE3 p.171-180)
- Immobilizer: E→T: N; T→E: T,{T,N}K (SE3 p.172). Between 2005 and 2015 all the major systems were broken through a combination of protocol errors, poor key management, weak ciphers and short export-driven keys: TI DST (40 bits), DST80 (2020: Hyundai 24 bits of entropy; Toyota derived from the serial number), Keeloq (diversification by XOR), Hitag2 (48 bits), Megamos (96 nominal, 49 effective; global master keys in 23 models) (SE3 p.172-173). Practical test: try buying a spare key (SE3 p.173). Universal masters give a BORA attack (break-once-run-anywhere) (SE3 p.173 note).
- **PKES (keyless):** relay attack; thefts +56% in the UK in 2017; crypto alone does not solve it; fix = UWB with distance measurement (802.15.4z) (SE3 p.173-174) `[DATED]`.
- HTTP digest; 2FA with password generator (S→U: N; U→P: N,PIN; P→U: {N,PIN}K); DoD CAC cut intrusions by 46% (SE3 p.175); real-time phishing against password calculators (SE3 p.176-178).

## 4. Protocol attacks (SE3 p.176-183)
- **Middleperson** (MIG-in-the-middle; relay): the defensive layer in banks combines known machine, password, second factor and transaction risk assessment; authenticating only the last 4 digits of the account for usability (SE3 p.178-179). The MIG story is told by one source and was disputed by another (SE3 p.177).
- **Reflection:** include the name in the challenge ({B,N}K); check that the intruder has not reflected its own challenge (SE3 p.179 and note). Trust reasoning: a response within 20 ms proves only that someone with K is within ≤2000 miles (SE3 p.179-180).
- **Spurious challenge (IFF):** active IFF is audible farther away than the radar echo; Germany plotted bombers at twice the radar range in 1944; modern systems authenticate the challenge (SE3 p.180). "Protocol correctness depends on assumptions about requirements" (SE3 p.180).
- **Message manipulation:** taximeters, tachographs, satellite commands that must not be accepted twice (SE3 p.181).
- **Chosen protocol attack (Mafia-in-the-middle):** malicious protocol that induces the user to reuse the same key/token; reusing keys across different applications is dangerous; letting third parties base their security on yours (SMS 2FA and SIM swap) can be foolish (SE3 p.183-184).

## 5. The environment changes (SE3 p.181-182)
`[from source]` Phantom withdrawals in the Netherlands (1993) and in the UK after chip-and-PIN: the assumptions of the 1980s (non-secret stripe; only the PIN encrypted; equipment in a trusted environment) stopped holding when cards moved to untrusted terminals; the change was gradual and the industry "did not see the problem coming" (SE3 p.181-182).

## 6. Key management and trusted-third-party protocols (SE3 p.184-188)
- **TOFU / resurrecting duckling:** digital tachograph and Homeplug trust the first key; a reset button "kills and resurrects" the device (SE3 p.184).
- **Sam as TTP:** A→S: A,B; S→A: {A,B,KAB,T}KAS, {A,B,KAB,T}KBS; certificates without expiry make revocation worse (SE3 p.185).
- **Needham-Schroeder (1978):** Bob does not know whether KAB is fresh; revocation is hard; the flaw is one of "displaced assumptions" (the enemy is among the users) (SE3 p.185-186).
- **Kerberos:** authentication server + ticket granting; timestamps fix revocation but create a dependency on synchronized clocks; it is a TTP (police with a warrant can obtain keys) (SE3 p.186-187). OAuth: delegation, short tokens; not designed to authenticate users; OpenID Connect is the profile for authentication (SE3 p.187-188).
- **Practical management:** how many keys, generation, lifetime, destruction, headroom for future functionality and failure recovery are common afterthoughts; HSMs (SE3 p.188).

## 7. Design assurance (SE3 p.188-189)
`[from source]` Formal methods force assumptions to be made explicit, but "we find bugs in verified protocols; they're just not in the part that was verified" (TLS verified in 1998, ~1 bug/year since). Robust protocols are *explicit*: interpretation depends only on the content (explicit names), formats are unambiguous, and the protocol must not allow attacking the software that processes it; randomness in protocols helps against attacks at other layers (SE3 p.189).

## Triggers
- "Can I use a counter or a random value?" → §2 + `references/04-criptografia.md` (nonce).
- "Review a protocol designed in-house" → remember: recommend an expert and public review `[from source]` (SE3 p.190); generate a checklist with `se3_checklist.py` area "protocolos".
- Dated items: car chips and keys, UWB, TLS (see `datado-desde-2020.md`).
