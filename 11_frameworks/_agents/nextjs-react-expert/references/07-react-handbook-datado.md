# React Handbook (freeCodeCamp, Flavio Copes, 2020-11-13) — [DATED]

**Source:** `React-Handbook-freeCodeCamp.pdf`, acronym **RCTHB**, 35 pages. Convention: PDF page (no printed number). Introductory 2020 guide based on **create-react-app**; the text does not state the React version. It is **[DATED]** relative to the Next releases (NX13-NX16), which require React 18.2+ (NX13 p.14) and use React 19 / 19.2 in the App Router (NX15 p.5-6; NX16 p.11). Read in full; the screenshot-only pages (p.7-10) were handled through the surrounding text.

## Contents (by section)
- **What React is (p.2-3):** a library for interfaces, born at Facebook in 2013; four concepts to start with: components, JSX, state and props.
- **JavaScript prerequisites (p.4-5):** variables, arrow functions, rest/spread, destructuring, template literals, callbacks, ES Modules. Reasons to learn it (p.5): popularity, tools like Next.js and Gatsby use React underneath, job interviews.
- **Installation (p.6-11):** `npx create-react-app <name>` (example `todolist`), `npm start` on port 3000.
- **Components (p.11-14):** `App.js` as a function that returns JSX; imports of React, SVG and CSS; a component can have state and receive props.
- **JSX (p.14-24):** looks like HTML but is not; `className` instead of `class` (reserved word, p.20); JSX does not forgive unclosed tags (p.21); composition (`WelcomeMessage`, p.17-19); expressions in braces, one per block, including ternaries (p.23-24).
- **State (p.24-26):** `useState` returns `[value, setter]`; do not change the variable directly; multiple calls allowed. The final example uses `ReactDOM.render(<Counter />, ...)` (p.26).
- **Props (p.27-29):** attributes become the function argument; destructuring; functions as props; special prop `children`.
- **Data flow (p.29-30):** parent → child through props; the child changes the parent's state by receiving the setter; Context API and Redux only mentioned.
- **Events (p.30-31):** `onClick` and others (`onKeyUp`, `onFocus`, `onChange`, `onMouseDown`, `onSubmit`).
- **`useEffect` (p.31-33):** runs after every render; second parameter with a dependency array; `[]` to run only on mount; useful for logs and third-party APIs.
- **Next steps (p.33-34):** Virtual DOM, immutability, composition, CSS, Context/Redux, forms, React Router, testing, and "a framework on top of React, such as Gatsby or Next.js".

## Important limits
- **Does not cover** Server Components, `'use client'`/`'use server'`, Suspense, Server Actions or hooks beyond `useState` and `useEffect` (see `09-sem-cobertura.md`).
- The Next releases **do not mention** `create-react-app` or `ReactDOM.render`; whether they work on React 18/19 is `[extrapolation]`, outside the collection.
- Specific links to the releases: NX15 p.6-7 (React Compiler reduces `useMemo`/`useCallback`), NX15 p.15 (hooks plugin 5.0.0), NX16 p.11 (`useEffectEvent`, Activity) — only cited in the releases, without a tutorial.
- For **React Native** questions: out of scope (agent mobile-frameworks-expert).
