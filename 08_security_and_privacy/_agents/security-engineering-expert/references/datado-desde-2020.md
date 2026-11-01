# [DATED] — what has changed or may have changed since 2020

The book is from 2020 (3rd edition) and the pages read reflect that state. This list marks what should be treated as `[DATED]`; for real decisions consult current sources (NIST, ENISA, legal, vendors). `[extrapolation]` marks what is outside the book. Convention: "SE3 p.N" = PDF page.

## Cryptography and standards
- **Key sizes and hash breaks** (829-bit RSA-250 in 2020; 2048+ bits; SHA-1 with a chosen-prefix attack in 2020; SHA-3 from 2015) (SE3 p.229-232). Check the current recommendations.
- **TLS 1.3 (2019) requiring forward secrecy; HSTS; Certificate Transparency mandatory since 2018** (SE3 p.242-244, 768).
- **Post-quantum cryptography:** NIST in round 3 in 2020 (SE3 p.249); the current state is different — verify.
- **Bitcoin mining power as a brute-force yardstick** (68 bits in ~10 min) (SE3 p.202): hardware changes.
- **DES/3DES, cost of dedicated machines** (SE3 p.221-222).

## Passwords and authentication
- **NIST SP 800-63-3 (2017)** and Google data on SMS/app as a second factor (SE3 p.140, 146-147).
- **CAPTCHA at US$0.50/1000** (2011) (SE3 p.162-163).
- **End of passwords/passkeys:** the book does not cover WebAuthn/FIDO2/passkeys (`se3_lookup.py passkey` → NOT COVERED) `[extrapolation]`.

## Platforms and software
- **iOS, Android 6, Windows 10, SELinux; SGX, TrustZone, CHERI** (SE3 p.261-277).
- **Spectre/Meltdown** and mitigations (SE3 p.281-282); **use-after-free as the dominant cause of remote execution** (SE3 p.280).
- **Vulnerability statistics** (90% buffer overflow in 2000; less than half in 2008) (SE3 p.283-284).
- **Containers/Docker Hub 2019** (SE3 p.272); **Rust** cited as a better language (SE3 p.283-284).
- **Microsoft SDL, DevSecOps, SaaS, SRE** (SE3 p.1017-1026): practices and tools have evolved.

## Incidents cited (all ≤ 2020)
- Equifax (2017), WannaCry/NotPetya (2017), Mirai (2016), DigiNotar (2011), Bangladesh Bank (2016), Tesco Bank (2016), Dieselgate, 737 Max (2019), Vault 7, Wirecard (2020) (SE3 p.89, 74, 92, 241, 469, 496-497, 1075-1080, 1054-1055, 389, 461-462). **Not** in the book: SolarWinds, Log4Shell, Kaseya and other later ones.

## Regulation and standards
- **GDPR (2018), Safe Harbour (struck down 2015), Privacy Shield (struck down Jul/2020), CCPA** (SE3 p.987-992): the transfer regime has changed; verify. **LGPD is not covered.**
- **EU Cybersecurity Act (2019/881), Cyber Essentials, ISO 27001, PCI DSS** (SE3 p.452-453, 482-483, 1065-1067).
- **EU medical device regulation 2017/745 (postponed to May/2021), 2019 European law on maintaining digital components** (SE3 p.56, 1051-1053).
- **Common Criteria: 85 of 1472 products at EAL6+ (2020)** (SE3 p.1057-1060).

## Payments
- **EMV, 3DS, contactless limits, No-PIN (only stopped working in the UK in 2017), pre-play** (SE3 p.484-497): the ecosystem has evolved.
- **SWIFT and 2016 controls** (SE3 p.465-471).

## Privacy and data
- **2020 US census and DP** (SE3 p.435-436); **HES, DeepMind, TPP, NHS** (SE3 p.402-405).
- **Facial recognition:** NIST FRVT 2018 (SE3 p.612-615); performance and regulation have changed a lot.

## Telephony, network, AI
- **SIM swap, SS7, 5G** (SE3 p.771, 794-795): details of 3G/4G/5G were NOT read.
- **State of AI/ML** (SE3 p.907-915): LLMs, generative AI and prompt injection are **not** in the book `[extrapolation]`.
- **Antivirus, IDS, SOAR, BeyondCorp** (SE3 p.749-760): products and effectiveness evolve.

## Others
- **Cybercrime statistics** (≈ half of crime by volume; pay-per-install US$10-15/1000; ransomware) (SE3 p.89-97): prices and volumes change.
- **UK/Ontario smart meters (2018)** (SE3 p.543-546); **STS counter rollover in 2024** (SE3 p.542-543).
- **Right-to-repair and automotive sustainability** (SE3 p.1082-1083).
