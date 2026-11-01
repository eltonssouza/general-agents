# "The web is flat", renaming and aliases

## The web is flat

- Hierarchies (employee → department → unit → company) tempt us to encode them in the URL (APIGEE p.28).
- **In query URLs** this can be good: navigation paths through hierarchies and relationships help locate things (APIGEE p.28).
- **In link URLs** (stored by the server, bookmarked by the client) it is a bad idea: hierarchies are less stable than they seem, and encoding them prevents reorganization or breaks the links when it happens (APIGEE p.28).
- The book **sets no numeric limit on nesting levels**. The criterion is link (stable, flat) vs query (can navigate relationships, including several hops: `/dogs/123456/owner/spouse`) (APIGEE p.28, p.33).

## The renaming dilemma

- A friendly identifier in the URL gives pretty URLs but prevents renaming; a machine identifier allows renaming but yields ugly URLs (APIGEE p.29).
- Solution: one URL in links and another in the query URI templates. E.g. template `https://dogtracker.com/person/{name}` → `/person/JoeMCarraclough` to find; persistent link with the machine ID (`/person/e9cdcf7a-…`) (APIGEE p.29, p.30).
- When Joe becomes JoeSmith44, the links do not change; the query now uses the new name (APIGEE p.30).
- The two URLs identify **different resources**: a specific person vs whoever has that name now; they may coincide for a while and then diverge (analogy with a president's page vs "current president" on DBpedia) (APIGEE p.30, p.31).

## Aliases with redirects

- Alternative: include the name in the URL and, on renaming, create a new alias; the old ones may redirect to the latest, which becomes the canonical URL (APIGEE p.31).
- Costs: the canonical URL changes over time; old names are never released (as on GitHub when renaming repositories); the implementation stores all previous names (APIGEE p.31).

## Common mistakes when citing this topic

- "The book limits nesting to 1 or 2 levels": there is no such number.
- "Every entity must sit at the root": the text is about stable links, it does not forbid query paths (APIGEE p.28, p.33, p.34).
