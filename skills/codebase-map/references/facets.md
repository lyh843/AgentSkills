# Facets — stack-specific tabs

The viewer's first two tabs (Architecture, File explorer) are computed from the scan and work for any repo. Everything stack-specific — API surface, DB schema, routes, background jobs, CLI commands, GraphQL types — is a **facet**: a declarative JSON block you generate by writing a small throwaway extractor script for the repo's stack. The viewer renders facets with generic section renderers; you never edit the HTML.

Write `facets.json` in the map workspace:

```json
{ "facets": [ <facet>, ... ] }
```

## Facet shape

```json
{
  "id": "api",                          // unique, becomes the tab anchor (#facet-api)
  "nav": "API surface",                 // tab label (defaults to title)
  "title": "tRPC API surface",          // h2 on the page
  "headline": "28 routers · 307 procedures",   // appended to the h2, lighter weight (optional)
  "sub": "one row per router in packages/api/src/router",  // right-aligned caption (optional)
  "hero": { "v": "307", "l": "tRPC procedures", "s": "28 routers" },  // adds a header stat tile (optional, first 3 facet heroes fit)
  "columns": 2,                         // 2 = render sections side by side (optional)
  "sections": [ <section>, ... ]
}
```

## Section kinds

### `tiles` — stat tile row (no card wrapper)
```json
{ "kind": "tiles", "tiles": [
  { "v": "75", "l": "tables", "s": "60 app · 15 auth" }
]}
```

### `barlist` — ranked horizontal stacked bars
For "N things sized by counts" (API routers by procedures, controllers by actions, GraphQL types by fields). Gets a by-value/a–z sort toggle and a legend automatically. Series colors come from the validated palette in fixed order — never reorder series between rows.
```json
{ "kind": "barlist", "title": "…optional card title…",
  "note": "hover a row for detail",
  "series": [ { "k": "q", "label": "queries" }, { "k": "m", "label": "mutations" } ],
  "rows": [
    { "label": "admin", "values": { "q": 18, "m": 25 }, "meta": "18q 25m", "tip": "router/admin.ts · 2.0k loc" }
  ]}
```

### `groups` — cards of chips, grouped by domain
For DB tables by domain, env vars by service, events by producer. `accent: true` gives a card a colored left border (use for one special group, e.g. generated/auth tables).
```json
{ "kind": "groups", "groups": [
  { "title": "Projects", "chips": ["project", "project_member"] },
  { "title": "Auth (generated)", "accent": true, "chips": ["user", "session"] }
]}
```

### `tree` — collapsible hierarchy with badges
For route trees, CLI command trees, module namespaces. Top level renders expanded, deeper levels collapsed. Badge colors are assigned per distinct badge string in order of first appearance (blue, orange, aqua, violet, yellow) — put the most important badge first in the data.
```json
{ "kind": "tree", "title": "Web routes — 39 pages · 38 handlers", "sub": "apps/web/src/app",
  "items": [
    { "label": "admin", "badge": "page", "children": [ { "label": "users", "badge": "page" } ] },
    { "label": "api/health", "badge": "api" }
  ]}
```

### `loclist` — labeled rows with a thin proportional bar
For background jobs, workflows, migrations, scripts — anything "name + size/steps". `bar` is a raw number, normalized against the section max. `muted: true` grays a row (helpers/support files). A row of `{ "section": "…" }` inserts a subheading.
```json
{ "kind": "loclist", "title": "Background workflows", "sub": "packages/jobs/src/workflows",
  "rows": [
    { "label": "github-sync", "meta": "18 steps · 934 loc", "bar": 934 },
    { "section": "support modules" },
    { "label": "workflow-execution-helpers", "meta": "519 loc", "bar": 519, "muted": true }
  ]}
```

## Extractor recipes

Write one Node script (`extract-facets.mjs` in the map workspace) that greps/parses the repo and writes `facets.json`. Keep it dumb and regex-based — counts and names, not ASTs. Worked patterns:

**tRPC** (routers dir): per file, count `\.query\(`, `\.mutation\(`, `\.subscription\(` → barlist rows. Filter files with 0 procedures (helpers living in the router dir). Cross-check router count against the `: \w+Router` entries in the root router file.

**Drizzle**: `export const (\w+)\s*=\s*pgTable\(\s*["'](\w+)["']` over schema files → table names; `pgEnum\(` count; migration count = `*.sql` files in the drizzle/migrations dir. Group tables into domains by hand (you just read the schema — you know the domains); leftovers go in an "Other" group so nothing is silently dropped.

**Prisma**: `^model (\w+)` in `schema.prisma`; group by name prefixes/relations.

**Next.js app router**: walk `app/`, a dir with `page.*` → badge `page`, with `route.*` → badge `api`; strip `(group)` segments from paths; build nested tree items. Don't drop the root `/` route (the empty path is easy to lose when splitting on `/`).

**Express/Fastify/Hono**: grep `\.(get|post|put|patch|delete)\(\s*["']([^"']+)` → tree or barlist by method.

**FastAPI/Flask**: `@(app|router)\.(get|post|put|delete)\(["']([^"']+)` / `@app.route\(["']([^"']+)`.

**Rails**: parse `config/routes.rb` (`resources :x`, `get "y"`), or `bin/rails routes` output if runnable. Models: `class (\w+) < ApplicationRecord` → groups.

**TanStack Start / Router**: file-based routes under `src/routes/` (or `app/routes/`) — each route file is a route; map filename to path (`index` → `/`, `$param` → `:param`, dot-nesting `posts.$id.tsx` → `/posts/:id`, strip `(group)` and pathless `_layout` segments; `__root` is the shell). Badge `route`; server functions (`createServerFn(`) and API routes (`createServerFileRoute(`) get badge `server`. If the app is loader-heavy, count loaders/actions per route file for a barlist.

**Django**: `path\(["']([^"']+)` / `re_path\(` in `urls.py` files (group by app) → tree; `class (\w+)\(.*models\.Model\)` per app → groups.

**GraphQL**: `type (\w+)`, `input (\w+)` in SDL files → groups; fields-per-type → barlist.

**Rust**: routes — axum `\.route\(\s*"([^"]+)"\s*,\s*(get|post|put|delete|patch)`, actix/Rocket attribute macros `#\[(get|post|put|delete|patch)\("([^"]+)"` → tree with method badges. DB — diesel `table!\s*\{\s*(\w+)`, sea-orm `#\[sea_orm\(table_name\s*=\s*"(\w+)"\)\]`, sqlx `migrations/*.sql` count plus `query(_as)?!\(` call count → groups + tiles. CLI — clap `#[derive(Parser)]` structs and `Subcommand` enum variants → tree. (Cargo workspace members and their path/workspace deps are auto-discovered by the scanner — no facet needed for the graph.)

**Elixir / Phoenix**: router — `(get|post|put|patch|delete|live|forward)\s+"([^"]+)"` and `resources\s+"([^"]+)"` in `router.ex`, prefixed with the enclosing `scope "..."` blocks → tree with `live`/`api` badges. Ecto — `schema\s+"(\w+)"` across `lib/` → groups by context dir. Background — `use Oban.Worker` modules → loclist. (Umbrella `apps/*` with `in_umbrella: true` deps are auto-discovered by the scanner.)

**Go**: routes — chi `r\.(Get|Post|Put|Delete)\("([^"]+)"`, gin/echo `\.(GET|POST|PUT|DELETE)\("([^"]+)"`, net/http `HandleFunc\("([^"]+)"` → tree. DB — sqlc `-- name: (\w+)` in queries dir, GORM structs with `gorm:"` tags → groups. CLI — cobra `Use:\s*"(\w+)` → tree.

**DBOS / queues / cron**: workflow/job files → loclist with step counts (`DBOS.runStep\(` or the stack's step marker: Sidekiq `perform`, Celery `@task`, Oban `perform/1`, BullMQ processors).

**CLI tools**: subcommand registrations (`command\(["'](\w+)`, clap derives, cobra `Use:`) → tree.

These recipes are worked examples, **not a whitelist** — the section renderers are stack-agnostic. For any stack not listed, apply the same move: find the registration idiom (route macro, schema declaration, job annotation, command definition), grep for it, and emit whichever of the five section kinds fits the shape of the data. If an idiom is too dynamic to grep reliably (runtime route registration, metaprogrammed schemas), prefer running the framework's own introspection command (`rails routes`, `mix phx.routes`, `manage.py show_urls`) and parsing its output — but only if the project already builds, and never install dependencies just for the map.

Only build facets that carry real signal for this repo — 2 or 3 good facets beat 5 thin ones. A facet with fewer than ~5 data points is better folded into another facet's `tiles` section.
