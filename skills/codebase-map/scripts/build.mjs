import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { execSync } from "node:child_process";

// usage: node build.mjs [map-config.json]
// Runs scan.mjs, merges meta.json + facets.json (from the config's directory),
// stamps git commit/date, injects everything into the viewer template, and
// writes the final self-contained HTML to cfg.out.

const scriptsDir = path.dirname(fileURLToPath(import.meta.url));
const configPath = path.resolve(process.argv[2] ?? "map-config.json");
const workDir = path.dirname(configPath);
const cfg = JSON.parse(fs.readFileSync(configPath, "utf8"));
const REPO = path.resolve(cfg.repo);

const dataPath = path.join(workDir, "codebase-data.json");
execSync(`node "${path.join(scriptsDir, "scan.mjs")}" "${configPath}" "${dataPath}"`, {
  stdio: "inherit",
});
const scan = JSON.parse(fs.readFileSync(dataPath, "utf8"));

const readIf = (p) => (fs.existsSync(p) ? JSON.parse(fs.readFileSync(p, "utf8")) : {});
const meta = readIf(path.join(workDir, "meta.json"));
const facets = readIf(path.join(workDir, "facets.json"));

let commit = "", commitDate = "";
try {
  commit = execSync(`git -C "${REPO}" log -1 --format=%h`, {
    encoding: "utf8",
    stdio: ["ignore", "pipe", "ignore"],
  }).trim();
  commitDate = execSync(`git -C "${REPO}" log -1 --format=%ad --date=format:%Y-%m-%d`, {
    encoding: "utf8",
    stdio: ["ignore", "pipe", "ignore"],
  }).trim();
} catch {
  console.warn("build: not a git repo — no commit stamp");
}

const embed = {
  title: cfg.title ?? scan.repoName,
  subtitle: cfg.subtitle ?? "",
  generated: new Date().toISOString().slice(0, 10),
  commit,
  commitDate,
  branch: cfg.branch ?? "",
  topKinds: cfg.topKinds ?? [],
  stripKinds: cfg.stripKinds ?? [],
  scan,
  meta,
  facets: facets.facets ?? [],
};

const template = fs.readFileSync(path.join(scriptsDir, "..", "assets", "viewer.html"), "utf8");
const safe = (s) => s.replace(/<\/script/gi, "<\\/script");
const html = template.replace("__EMBED__", () => safe(JSON.stringify(embed)));
if (html.includes("__EMBED__")) throw new Error("placeholder not replaced");
const outPath = path.resolve(workDir, cfg.out ?? "codebase-map.html");
fs.writeFileSync(outPath, html);
console.log(`build: ${outPath} (${Math.round(html.length / 1024)}KB${commit ? `, ${commit} @ ${commitDate}` : ""})`);
