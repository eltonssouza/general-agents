# Topics NOT COVERED in the collection

The collection is an **overview**: four release posts (Next 13 to 16), a 2019 Next.js handbook and a 2020 React handbook. For the items below, answer "NOT COVERED"; use outside content only as a labeled `[extrapolation]` and only if the user asks. Automatic check: `python -I scripts/nx_lookup.py --gaps`.

- Hooks beyond useState/useEffect (useRef, useReducer, useContext in detail, useMemo/useCallback in detail)
- Server Components details, the 'use client' boundary and server/client composition
- App Router file conventions beyond page/layout/loading/default/route
- next/navigation, the App Router useRouter, redirect/notFound in detail
- Full 'use cache' syntax, cacheLife and profiles (only the names max/hours/days and { expire })
- proxy.ts: matcher and full API
- Authentication, databases, testing, i18n, advanced SEO in Next
- Redux, React Router, Context API (only mentioned as next steps in RCTHB p.34)
- Intermediate minor versions (13.x, 14.x, 15.x) and Next 12 or earlier (except stray mentions: 12.2 in NX13 p.11; 14.1/14.2.0 in NX14/NX15; 15.3+ in NX16 p.6)
- Next.js 17 or later; current state of the Pages Router after 16
- React Native (out of scope; belongs to mobile-frameworks-expert)
- Vue, Svelte, Angular, Express, Node (other agents)
- Vercel: plans, pricing, current deploy (NXHB p.77 gives 2019 Now plan limits, [DATED])

Note: the NX16 text describes itself as a release that is "now available" (p.1) and later mentions a migration guide "before the stable release" (p.14); do not use that phrase to state the stability status of specific features.
