import fs from "node:fs";
import path from "node:path";
import { execSync } from "node:child_process";

// usage: node scan.mjs <map-config.json> <out.json>
// Scans the repo described by the config and emits structural data:
// modules (with per-file LOC trees), dependency edges, git activity, totals.

const [configPath, outPath] = process.argv.slice(2);
if (!configPath || !outPath) {
  console.error("usage: node scan.mjs <map-config.json> <out.json>");
  process.exit(2);
}
const cfg = JSON.parse(fs.readFileSync(configPath, "utf8"));
const ROOT = path.resolve(cfg.repo);
if (!fs.existsSync(ROOT)) {
  console.error(`repo not found: ${ROOT}`);
  process.exit(2);
}

const DEFAULT_EXT = [
  ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".vue", ".svelte",
  ".py", ".go", ".rs", ".java", ".rb", ".php", ".c", ".cc", ".cpp", ".h", ".hpp",
  ".cs", ".swift", ".kt", ".scala", ".ex", ".exs", ".heex", ".eex", ".erb", ".sh",
  ".css", ".scss", ".sass", ".less", ".sql", ".json", ".yaml", ".yml", ".toml",
  ".md", ".mdx", ".rst", ".graphql", ".proto", ".tf", ".html",
];
const CODE_EXT = new Set(cfg.extensions ?? DEFAULT_EXT);
const EXCLUDE_DIRS = new Set([
  "node_modules", "dist", "build", "out", "target", "vendor", "coverage",
  ".git", ".next", ".turbo", ".venv", "venv", "__pycache__", ".pytest_cache",
  ".vercel", ".dbos", "playwright-report", "test-results", ".idea", ".vscode",
  ...(cfg.excludeDirs ?? []),
]);
const EXCLUDE_REL = (cfg.excludeRel ?? []).map((r) => new RegExp(r));

function countLines(file) {
  try {
    const buf = fs.readFileSync(file);
    let n = 0;
    for (let i = 0; i < buf.length; i++) if (buf[i] === 10) n++;
    if (buf.length > 0 && buf[buf.length - 1] !== 10) n++;
    return n;
  } catch {
    return 0;
  }
}

// dir node: { n, c: [children], v: totalLoc, f: fileCount } · file node: { n, v, e }
function walk(dir) {
  const node = { n: path.basename(dir), c: [], v: 0, f: 0 };
  let entries;
  try {
    entries = fs.readdirSync(dir, { withFileTypes: true });
  } catch {
    return node;
  }
  for (const e of entries) {
    if (e.name.startsWith(".") && e.name !== ".github") continue;
    const full = path.join(dir, e.name);
    const rel = path.relative(ROOT, full);
    if (EXCLUDE_REL.some((r) => r.test(rel))) continue;
    if (e.isDirectory()) {
      if (EXCLUDE_DIRS.has(e.name)) continue;
      const child = walk(full);
      if (child.f > 0) {
        node.c.push(child);
        node.v += child.v;
        node.f += child.f;
      }
    } else if (e.isFile()) {
      if (!CODE_EXT.has(path.extname(e.name))) continue;
      const loc = countLines(full);
      node.c.push({ n: e.name, v: loc, e: path.extname(e.name).slice(1) });
      node.v += loc;
      node.f += 1;
    }
  }
  node.c.sort((a, b) => b.v - a.v);
  return node;
}

/* ---------- module discovery ---------- */
// Priority: cfg.modules > JS workspaces > Cargo workspace > Elixir umbrella > top-level dirs.
function expandGlob(g) {
  // supports "dir/*" and exact paths — the patterns real workspace files use
  if (g.startsWith("!")) return [];
  if (g.endsWith("/*")) {
    const base = path.join(ROOT, g.slice(0, -2));
    if (!fs.existsSync(base)) return [];
    return fs
      .readdirSync(base, { withFileTypes: true })
      .filter((e) => e.isDirectory())
      .map((e) => path.join(g.slice(0, -2), e.name));
  }
  return fs.existsSync(path.join(ROOT, g)) ? [g] : [];
}

const normRel = (rel, sub) => path.normalize(path.join(rel, sub)).split(path.sep).join("/");
const kindOf = (rel, fallback) => (rel.includes("/") ? rel.split("/")[0].replace(/s$/, "") : fallback);

function discoverCargoWorkspace() {
  const rootToml = path.join(ROOT, "Cargo.toml");
  if (!fs.existsSync(rootToml)) return null;
  const src = fs.readFileSync(rootToml, "utf8");
  const members = src.match(/\[workspace[^\]]*\][\s\S]*?members\s*=\s*\[([\s\S]*?)\]/);
  if (!members) return null;
  const globs = [...members[1].matchAll(/["']([^"']+)["']/g)].map((m) => m[1]);
  // [workspace.dependencies] entries with a path — resolved by `dep = { workspace = true }` in members
  const wsDeps = new Map();
  const wsDepSection = src.match(/\[workspace\.dependencies\]([\s\S]*?)(?=\n\[|$)/);
  if (wsDepSection) {
    for (const m of wsDepSection[1].matchAll(/^\s*([\w-]+)\s*=\s*\{[^}]*path\s*=\s*["']([^"']+)["']/gm)) {
      wsDeps.set(m[1], m[2].split(path.sep).join("/"));
    }
  }
  const mods = [];
  for (const g of globs) {
    for (const rel of expandGlob(g)) {
      const toml = path.join(ROOT, rel, "Cargo.toml");
      if (!fs.existsSync(toml)) continue;
      const csrc = fs.readFileSync(toml, "utf8");
      const deps = [...csrc.matchAll(/^\s*[\w-]+\s*=\s*\{[^}]*path\s*=\s*["']([^"']+)["']/gm)]
        .map((m) => normRel(rel, m[1]));
      for (const m of csrc.matchAll(/^\s*([\w-]+)(?:\s*=\s*\{[^}]*workspace\s*=\s*true|\.workspace\s*=\s*true)/gm)) {
        if (wsDeps.has(m[1])) deps.push(wsDeps.get(m[1]));
      }
      mods.push({
        id: rel,
        dir: path.basename(rel),
        relPath: rel,
        kind: kindOf(rel, "crate"),
        name: csrc.match(/^\s*name\s*=\s*["']([^"']+)["']/m)?.[1] ?? rel,
        declaredDeps: [...new Set(deps)],
      });
    }
  }
  return mods.length ? mods : null;
}

function discoverMixUmbrella() {
  const appsDir = path.join(ROOT, "apps");
  if (!fs.existsSync(path.join(ROOT, "mix.exs")) || !fs.existsSync(appsDir)) return null;
  const mods = [];
  for (const e of fs.readdirSync(appsDir, { withFileTypes: true })) {
    if (!e.isDirectory()) continue;
    const mixPath = path.join(appsDir, e.name, "mix.exs");
    if (!fs.existsSync(mixPath)) continue;
    const src = fs.readFileSync(mixPath, "utf8");
    const deps = [...src.matchAll(/\{:(\w+)\s*,[^}]*in_umbrella:\s*true/g)].map((m) => "apps/" + m[1]);
    mods.push({
      id: "apps/" + e.name,
      dir: e.name,
      relPath: "apps/" + e.name,
      kind: "app",
      name: src.match(/app:\s*:(\w+)/)?.[1] ?? e.name,
      declaredDeps: [...new Set(deps)],
    });
  }
  return mods.length ? mods : null;
}

function discoverModules() {
  if (cfg.modules?.length) {
    return cfg.modules.map((m) => ({
      id: m.id ?? m.path,
      dir: path.basename(m.path ?? m.id),
      relPath: m.path ?? m.id,
      kind: m.kind ?? "module",
      name: m.name ?? (m.id ?? m.path),
      declaredDeps: m.deps ?? null,
    }));
  }
  // JS monorepo?
  let globs = null;
  const wsYaml = path.join(ROOT, "pnpm-workspace.yaml");
  if (fs.existsSync(wsYaml)) {
    const src = fs.readFileSync(wsYaml, "utf8");
    const m = src.match(/^packages:\s*\n((?:\s+-\s+.*\n?)+)/m);
    if (m) globs = [...m[1].matchAll(/-\s+["']?([^"'\n]+)["']?/g)].map((x) => x[1].trim());
  }
  if (!globs) {
    const rootPkgPath = path.join(ROOT, "package.json");
    if (fs.existsSync(rootPkgPath)) {
      const rootPkg = JSON.parse(fs.readFileSync(rootPkgPath, "utf8"));
      const ws = rootPkg.workspaces;
      globs = Array.isArray(ws) ? ws : ws?.packages ?? null;
    }
  }
  if (globs) {
    const mods = [];
    for (const g of globs) {
      for (const rel of expandGlob(g)) {
        const pkgPath = path.join(ROOT, rel, "package.json");
        if (!fs.existsSync(pkgPath)) continue;
        const pkg = JSON.parse(fs.readFileSync(pkgPath, "utf8"));
        mods.push({
          id: rel,
          dir: path.basename(rel),
          relPath: rel,
          kind: kindOf(rel, "package"),
          name: pkg.name ?? rel,
          pkgDeps: { ...pkg.dependencies, ...pkg.devDependencies, ...pkg.peerDependencies },
        });
      }
    }
    if (mods.length) return mods;
  }
  const cargo = discoverCargoWorkspace();
  if (cargo) return cargo;
  const mix = discoverMixUmbrella();
  if (mix) return mix;
  // fallback: top-level dirs with source files
  const mods = [];
  for (const e of fs.readdirSync(ROOT, { withFileTypes: true })) {
    if (!e.isDirectory() || e.name.startsWith(".") || EXCLUDE_DIRS.has(e.name)) continue;
    mods.push({ id: e.name, dir: e.name, relPath: e.name, kind: "dir", name: e.name });
  }
  return mods;
}

function gitCommits(rel, since) {
  try {
    return (
      parseInt(
        execSync(`git -C "${ROOT}" rev-list --count --since="${since}" HEAD -- "${rel}"`, {
          encoding: "utf8",
          stdio: ["ignore", "pipe", "ignore"],
        }).trim(),
        10,
      ) || 0
    );
  } catch {
    return 0;
  }
}

const since = cfg.since ?? "180 days ago";
const modules = discoverModules();
const nameToId = new Map(modules.map((m) => [m.name, m.id]));
const ids = new Set(modules.map((m) => m.id));
const excludeDeps = new Set(cfg.excludeDeps ?? []);

const out = { repoName: cfg.title ?? path.basename(ROOT), since, modules: [] };
for (const m of modules) {
  const tree = walk(path.join(ROOT, m.relPath));
  tree.n = m.id;
  if (tree.f === 0) continue;
  let deps = [];
  if (m.declaredDeps) deps = m.declaredDeps.filter((d) => ids.has(d));
  else if (m.pkgDeps)
    deps = Object.keys(m.pkgDeps)
      .filter((d) => !excludeDeps.has(d))
      .map((d) => nameToId.get(d))
      .filter((id) => id && ids.has(id));
  out.modules.push({
    id: m.id,
    dir: m.dir,
    kind: m.kind,
    name: m.name,
    loc: tree.v,
    files: tree.f,
    commits: gitCommits(m.relPath, since),
    deps: [...new Set(deps)],
    tree,
  });
}
for (const [from, to] of cfg.edges ?? []) {
  const mod = out.modules.find((m) => m.id === from);
  if (mod && ids.has(to) && !mod.deps.includes(to)) mod.deps.push(to);
}
out.totals = {
  loc: out.modules.reduce((s, m) => s + m.loc, 0),
  files: out.modules.reduce((s, m) => s + m.files, 0),
  modules: out.modules.length,
};

fs.writeFileSync(outPath, JSON.stringify(out));
console.log(
  `scan: ${out.totals.modules} modules, ${out.totals.files} files, ${out.totals.loc} loc → ${outPath}`,
);
