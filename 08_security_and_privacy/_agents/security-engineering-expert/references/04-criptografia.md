# 04. Cryptography for engineers (Ch. 5, with supplements from ch. 20)

Convention: "SE3 p.N" = PDF page; printed = PDF − 47. Reading: ch. 5 in full from 5.2.2 (p.195); 5.1-5.2.1 only the beginning (p.192-195). 2020 book: key lengths, hash breaks and the state of standards are `[DATED]` — check current sources (NIST etc.) before deciding.

## 1. Principles
- `[from source]` Crypto is "where security engineering meets mathematics"; many constructions are confusing and many tools have insecure defaults (CAPI encourages ECB) (SE3 p.192-193).
- `[from source]` In real systems **almost no attack is cryptanalytic**; most exploit implementation (bad RNG, timing, handling errors), and short keys due to export control/ignorance (SE3 p.249).
- `[from source]` **"Don't roll your own"**: do not design your own ciphers or protocols or write the crypto code if you can avoid it; use accredited, current toolkits; seek experts and peer review (SE3 p.239, 250-251).
- `[from source]` Randomness/randomization in protocols and ciphers increases robustness against attacks at other layers (SE3 p.189, 234).

## 2. Security models (SE3 p.195-203)
- **Perfect secrecy** (one-time pad): all possible plaintexts equiprobable given the ciphertext; Shannon: requires at least as many keys as texts and equiprobability; does not protect integrity (malleable) (SE3 p.195-196).
- **Concrete security:** the adversary's actual work; at the time of the book, bitcoin miners solved a 68-bit puzzle in ~10 min; an 80-bit key would take 2^12 times longer (~one month); 128 bits would be 2^48 times longer; in 1000 years the probability of hitting it by chance would be 2^-35 (SE3 p.202) `[DATED]`. A system is (t,ε)-secure if an adversary running for time t breaks it with probability ≤ ε (SE3 p.202).
- **Indistinguishability/standard model; semantic security; random oracle** (SE3 p.202-203).

## 3. Hashes and the birthday theorem (SE3 p.203-206)
- Properties: one-wayness (~2^(n-1) attempts), output that does not reveal part of the input, and collision resistance (SE3 p.204-205).
- **Birthday theorem:** with N possible values a collision appears after ~√N samples; for n bits of output, ~2^(n/2) hashes; 50% chance already with 23 people; book formula (note): β = N(N−1)…(N−m+1)/N^m, with approximation N ≃ m²/(2·log(1/β)) (SE3 p.205). Use `se3_calc.py birthday`.
- Engineering consequences: MD5 (128 bits) → up to 2^64; SHA-1 (160) → 2^80; for collision resistance use output ≥ 256 bits (SHA-2 or SHA-3); for second preimage less may suffice (SE3 p.206). In challenge-response, a collision is not a problem if the attacker must answer the freshly issued challenge (SE3 p.206).
- Hash in a digital signature: if there is a collision, the attacker precomputes M1/M2 and fools the signer (book example: book order vs mortgage) (SE3 p.206).
- History: MD4 (1998), MD5 (2004), SHA-1 (collision published in 2017; chosen-prefix attack in 2020, forgeable certificates for tens of thousands of dollars), SHA-2 (2002), SHA-3/Keccak (2015) (SE3 p.229-230) `[DATED]`. A collision does not always break the application (forensics, bank MACs), but it is a "certificational threat": in 2005 a driver was acquitted in Sydney because nobody vouched for the security of MD5 (SE3 p.230).
- HMAC: HMACk(M)=h(k⊕B, h(k⊕A, M)) with 0x36 and 0x5C (SE3 p.230-231). Merkle trees, commitments, key updating (backward security) and autokeying (forward security) (SE3 p.231-232).

## 4. Block ciphers, AES, DES and modes (SE3 p.208-228)
- Block = pseudorandom permutation; attack types: known/chosen plaintext, chosen ciphertext, related-key (SE3 p.208-209). "Certificational attacks" (differential DES 2^47, linear 2^43) have no practical effect, but shake confidence (SE3 p.209).
- **A 64-bit block is a limit:** repetitions after ~2^32 blocks in CBC/OFB; 3DES suffers from this (SE3 p.226). A 16-bit block would allow a dictionary (SE3 p.213).
- **AES:** 128-bit blocks; keys of 128/192/256; 10/12/14 rounds; biclique attack 2^126 vs 2^127 (AES-128): no practical effect; practical attacks are implementation ones (cache timing, power) (SE3 p.216-217). The author advises against "pluggable cryptography" (risk in the negotiation protocol > risk of attack on AES) (SE3 p.217-218) and recommends AES over GOST/Camellia/Serpent (SE3 p.218).
- **DES:** brute force 2^55 on average; Deep Crack (1998, <US$250,000, 3 days); 2006: 120 FPGAs/US$10,000/7 days; 3DES(k0,k1,k2;M) = DES(k2; DES⁻¹(k1; DES(k0;M))) (SE3 p.221-222) `[DATED]`.
- **Modes:** ECB only for single blocks (PINs, challenges) — reveals patterns, allows cut-and-splice (SE3 p.223-224); CBC requires a separate MAC and suffers from *padding oracle* (Vaudenay 2002; variants up to 2016) (SE3 p.224-225); CTR parallelizable, cycle 2^n (SE3 p.225); additive modes have two systemic weaknesses: **keystream reuse** ("two-time tape", Venona) and lack of integrity (changing $500 to $500,000) (SE3 p.207, 225); MAC: CBC-MAC (fixed length), CMAC (variable) (SE3 p.226); **GCM** (NIST 2007) is "the sensible default for authentication+encryption of bulk content", secure as long as keys/IVs are never repeated; CCM ~2x more expensive (SE3 p.227); XTS-AES for disk preserves size, but tampering still needs to be detected by other layers (SE3 p.227-228).

## 5. Asymmetric (SE3 p.232-243)
- Factoring and discrete logarithm; RSA-250 record (829 bits, 2020); 1024 bits probably factorable by the NSA; use ≥ 2048 bits (SE3 p.232) `[DATED]`. To match 128 symmetric bits, 256-bit EC; traditional RSA/DL need 3072 bits for Top Secret; NSA Suite B uses 384-bit EC (SE3 p.247) `[DATED]`.
- **"Raw" RSA is not secure:** it is multiplicatively homomorphic and deterministic; a small exponent with the same message to several recipients is dangerous; use randomized padding (OAEP, PKCS#1) and sign the hash (SE3 p.233-235). Real failures: Bleichenbacher (error oracle), timing, computation errors that reveal factors (SE3 p.235).
- **Diffie-Hellman:** transient keys give forward security (term from ch. 5; "forward secrecy" appears in TLS, p.244); without authentication it suffers from middleperson; common 1024-bit primes are a risk (SE3 p.237-238). DSA with 2048-bit p and 256-bit q and SHA-256 (SE3 p.240). Bluetooth KNOB (1-byte key) (SE3 p.238) `[DATED]`.
- **CAs:** hundreds of trusted CAs; several states can coerce at least one; revocation is "flaky"; DigiNotar 2011 and the Kazakhstan certificate 2019 (SE3 p.241-242 and note 10).
- **TLS:** handshake, downgrade by 40-bit export, ≥12 serious attacks despite the 1998 formal verification; TLS 1.1/1.2; HSTS and Certificate Transparency; TLS 1.3 (Jan/2019) requires forward secrecy and eliminates old ciphers (SE3 p.242-244) `[DATED]`.
- **Code signing** is harder when the user is the enemy (SE3 p.244-245). PGP: only 4 of 12 subjects sent encrypted email correctly (SE3 p.245-246).
- **Special primitives:** threshold crypto, blind signatures (SE3 p.246-247).
- **Quantum:** the author is skeptical about the practical threat and about quantum cryptography (SE3 p.248); NIST post-quantum in round 3 in 2020 (SE3 p.249) `[DATED]` — the assessment has changed since; confirm.
- **RNG:** RSA with common factors; 1 in 172 IoT certificates trivial (2020) (SE3 p.249).

## 6. How ch. 20 complements this
FDE (key derived from a password allows offline attack; cold boot; Android reset; encrypting S3 may be mere compliance) (SE3 p.703-705); Signal (X3DH, double ratchet; forward and backward secrecy; hard part = initial authentication) (SE3 p.706-707); HSMs (complex APIs: "does a chain of 17 transactions leak a key?", p.712; featuritis, p.716-717). See `references/12-canais-laterais-e-cripto-avancada.md`.

## Related scripts
`se3_calc.py birthday | bits | brute-force | entropy | hash-collision | dod-password`. All formulas checked against the cited pages; see `tests/relatorio-de-fidelidade.md`.
