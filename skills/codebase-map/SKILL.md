---
name: codebase-map
description: Generate an interactive, self-contained HTML map of any codebase — a dependency graph of its modules, a zoomable lines-of-code treemap, and stack-specific tabs (API surface, DB schema, routes, background jobs). Use when the user asks for a codebase visualization, codebase map, architecture diagram/atlas, "help me understand this repo visually", "explore the codebase interactively", or wants to onboard someone onto a repo. Also use to refresh a map generated earlier by this skill.
metadata:
  version: 1.0.0
---

# Codebase Map

Produce a single self-contained HTML file (no CDNs, works offline, light+dark, colorblind-validated palette) that lets a visual learner explore a repo from architecture level down to individual files.

The pipeline separates what is generic from what is not:

- `scripts/scan.mjs` — generic scanner: modules, per-file LOC trees, dependency edges, git activity. Works on any repo.
- `scripts/build.mjs` — assembles scan + `meta.json` + `facets.json` into `assets/viewer.html` (single `__EMBED__` placeholder) and writes the final HTML.
- **You** supply the two things a script can't: prose understanding (`meta.json`) and stack-specific facets (`facets.json`, schema in `references/facets.md`).

## Procedure

### 1. Set up a map workspace
Ask where the output should live if not stated (default: a `codebase-map/` dir next to the repo, or the user's notes dir). Create a working dir there holding: `map-config.json`, `meta.json`, `facets.json`, `extract-facets.mjs`, and the output HTML. Keeping these files makes every future refresh a one-command rebuild.

### 2. Write `map-config.json`
```json
{
  "repo": "/abs/path/to/repo",
  "title": "repo-name",
  "subtitle": "COMPANY · WHAT IT IS · MONOREPO ATLAS",
  "out": "repo-name-map.html",
  "branch": "main",
  "topKinds": ["app"],
  "stripKinds": ["tooling"],
  "excludeDeps": ["@org/tsconfig", "@org/tailwind-config"],
  "excludeRel": ["drizzle/meta$", "migrations/meta$"],
  "edges": [["apps/web", "packages/api"]],
  "modules": [{ "id": "backend", "path": "src/backend", "kind": "service", "deps": ["core"] }]
}
```
Module discovery order: explicit `modules` → JS workspaces (pnpm-workspace.yaml / package.json workspaces, edges from package.json deps) → Cargo workspace members (edges from path/workspace deps) → Elixir umbrella `apps/*` (edges from `in_umbrella: true` deps) → top-level dirs (no edges). For anything else (Go multi-module, Django apps, single-app repos), list `modules` yourself with `deps` derived from a quick import grep — even rough edges make the graph useful. All fields except `repo`/`title`/`out` are optional.

- `topKinds`: kinds pinned to the top row (deployables — apps, services). Without it, layering is pure longest-path and low-dependency apps sink into the middle.
- `stripKinds`: kinds excluded from the graph and shown as a footnote chip strip (tooling, infra).
- `excludeDeps`: dep names every module shares (base tsconfig etc.) — they'd make the graph a hairball.
- `excludeRel`: regexes for **generated content that would drown real code** (lockfile-scale JSON, migration meta snapshots). Sanity-check for this in step 3.

### 3. Scan and sanity-check
```bash
node <skill-dir>/scripts/scan.mjs map-config.json codebase-data.json
```
Then inspect the biggest files/modules (quick `node -e` over the JSON). If the top files are generated artifacts, add `excludeRel` patterns and rescan. Do not skip this — one 600k-line generated dir silently ruins every number and treemap.

### 4. Write `meta.json` — the understanding layer
Explore the codebase (fan out a read-only subagent if your harness supports one; medium breadth: package manifests, entry files, key dirs — not whole files) across all modules and produce JSON:

> For each module return: "purpose" (1–2 specific sentences on what it does in the product), "keyAreas" (3–6 items, `"dir — what it does"` format), "runtime" (one line: where/when it runs), plus a top-level "runtimeStory" (4–6 sentences tracing how a request flows through the pieces at runtime). Base every claim on files actually seen.

Shape:
```json
{
  "runtimeStory": "…",
  "flow": [["browser → apps/web", "Next.js UI + BFF"], ["web → packages/api", "…"]],
  "testSegments": ["qa-datasets"],
  "modules": {
    "apps/web": { "purpose": "…", "keyAreas": ["src/app — …"], "runtime": "…", "testOnly": false }
  }
}
```
Write `flow` yourself: 4–6 numbered steps distilled from the runtimeStory. Mark test-harness modules (`e2e`, evals) with `testOnly: true` (dashed border in the graph). `testSegments` adds repo-specific dir names to the treemap's test-hatching heuristic. Modules in `stripKinds` just need `purpose` (used as the chip tooltip).

### 5. Build facets — the stack-specific tabs
Detect the stack, then write one throwaway `extract-facets.mjs` that emits `facets.json`. Read `references/facets.md` for the section schemas (`tiles`, `barlist`, `groups`, `tree`, `loclist`) and per-stack extractor recipes (tRPC, Drizzle, Prisma, Next.js/TanStack Start, Express/FastAPI/Rails/Django routes, Rust axum/actix + diesel/sea-orm/sqlx, Phoenix/Ecto/Oban, Go chi/gin + sqlc, GraphQL, job queues, CLIs) — the recipes are worked examples, not a whitelist; any stack works by grepping its registration idiom. 2–3 high-signal facets beat 5 thin ones; skip facets the stack doesn't have. Verify counts against the source (e.g. a "router" file with zero procedures is a helper — filter it, don't count it).

### 6. Build
```bash
node <skill-dir>/scripts/build.mjs map-config.json
```
Stamps the current commit/date from git and writes `cfg.out`.

### 7. Verify by rendering — mandatory
Open the file in a browser and look at every tab, both themes. If your browser tooling can't open `file://` URLs, serve briefly: `python3 -m http.server <port>` in the output dir (kill it after). Check: console has zero errors; graph layers/ordering look sane (adjust `topKinds`/`excludeDeps` if it's a hairball or apps sank); treemap shows colored file cells, not large empty dir voids; hover tooltips, node click → panel, treemap zoom + breadcrumbs work; facet numbers match the counts you verified in step 5; dark AND light themes both read well.

### 8. Hand off
Write a short README in the map workspace: what the map is, `node <skill-dir>/scripts/build.mjs map-config.json` to refresh, and that `meta.json`/`facets.json` are hand-maintained (counts auto-update on rebuild; prose and domain groupings don't). Offer to update the user's memory/notes with the location.

## Design constraints (do not regress these)

- The output must stay **fully self-contained** — no CDN scripts, no fetches, no web fonts. Everything inline; system font stacks only.
- The palette in `viewer.html` is pre-validated for both themes (colorblind-safe adjacent-hue ordering; low-contrast slots relieved by direct labels). Don't introduce new colors or reorder series colors. If the user wants brand colors, verify colorblind separation and surface contrast before swapping values.
- Treemap recursion is size-gated, not depth-capped — that's what keeps deep single-chain trees (Next.js app dirs) from rendering as voids.
- Tooltips carry full paths; labels appear only on cells that fit (relief rule for low-contrast fills).
- LOC counts and byte-based heuristics are for *visual proportion* only — never present them as anything more precise than that.
