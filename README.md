# AgentSkills

A collection of Codex skills for local workflows, study pipelines, codebase exploration, and lightweight automation.

## Included Skills

| Skill | What it does |
| --- | --- |
| `ai-paper-digest` | Collects recent AI papers and supports follow-up paper analysis. |
| `battery-status` | Reads local battery and charging information in a compact format. |
| `book-to-skill` | Converts books and documents into reusable knowledge skills. |
| `codebase-map` | Generates an interactive HTML codebase map and dependency graph. |
| `codebase-overview` | Explores a codebase systematically and maps its architecture. |
| `codebase-summary` | Produces structured architecture summaries and API inventories. |
| `concept-wiki-html` | Builds a local-source-grounded concept-network HTML study page. |
| `frontend-design` | Guides intentional frontend visual design. |
| `gh-address-comments` | Inspects and addresses GitHub pull request review feedback. |
| `gh-fix-ci` | Investigates failing GitHub Actions checks. |
| `github` | Routes GitHub repository, pull request, and issue workflows. |
| `grounded-file-qa` | Ingests local files, especially PDFs, for evidence-grounded Q&A. |
| `imagegen` | Generates and edits raster images with bundled helpers. |
| `learn-codebase` | Reads every source file to build full codebase context. |
| `lecture-note-writer` | Writes or rewrites course notes from slides in the user's note style. |
| `ning-python-scientific-plotting` | Creates and reviews Python research figures using nine plotting chapters and supporting references. |
| `openai-docs` | Finds official OpenAI product and API documentation. |
| `plugin-creator` | Scaffolds Codex plugins and maintains local plugin metadata. |
| `ponytail` | Guides minimal implementations and avoids unnecessary complexity. |
| `ponytail-audit` | Audits a whole repository for over-engineering. |
| `ponytail-debt` | Collects deliberate shortcuts from `ponytail:` comments. |
| `ponytail-gain` | Displays the skill's recorded benchmark impact. |
| `ponytail-help` | Provides a reference for the ponytail skill family. |
| `ponytail-review` | Reviews changes specifically for unnecessary complexity. |
| `repo-quick-scan` | Gives a shallow, read-only repository orientation. |
| `review-agent` | Performs delegated, read-only code reviews focused on defects. |
| `skill-creator` | Creates and validates Codex skills. |
| `skill-installer` | Installs skills from curated sources or GitHub repositories. |
| `use-code-wiki` | Navigates repositories through a `.code-wiki/wiki.json` index. |
| `yeet` | Handles intentional GitHub commit, push, and draft PR workflows. |

## Repository Layout

```text
skills/
  <skill-name>/
    SKILL.md
    agents/       # When supplied by the skill
    scripts/      # When supplied by the skill
    references/   # When supplied by the skill
    assets/       # When supplied by the skill
```

Each skill keeps its own `SKILL.md` plus any supporting scripts, references, or agent metadata.

## Local Sync Snapshot

On September 12, 2026, 24 missing skills were copied from local installations and plugin packages. The original 5 skills were preserved unchanged. A follow-up packaged the scientific plotting resources with a new entrypoint, bringing the collection to 30 skills.

| Local source | Added | Details |
| --- | ---: | --- |
| `~/.codex/skills/` | 13 | All top-level skills with a `SKILL.md`. |
| `~/.codex/skills/.system/` | 6 | `imagegen`, `openai-docs`, `plugin-creator`, `review-agent`, `skill-creator`, `skill-installer`. |
| `~/snap/codex/current/skills/` | 1 | `book-to-skill`; duplicate system skills use the `~/.codex` copy. |
| `~/.codex/plugins/cache/openai-curated/github/bd2122cb/skills/` | 4 | `gh-address-comments`, `gh-fix-ci`, `github`, `yeet`; the source plugin manifest declares MIT. |
| `~/.agents/skills/ning-python-scientific-plotting/` | 1 | Nine chapter files, `patterns.md`, and `glossary.md`, with a new repository-side `SKILL.md` and agent metadata. |

Copies retain their supporting resources, executable permissions, and upstream license files. Git metadata, Python bytecode, and OS cache files are excluded. Existing destination skills are not overwritten.

The plotting package preserves all 11 source resource files unchanged. Its new `SKILL.md` routes tasks to the relevant chapters and distinguishes historical journal guidance from current submission requirements. The original local resource directory is unchanged.

Not imported:

- 22 skills in `~/.codex/plugins/cache/openai-curated-remote/`: `deep-research`, `plugin-management`, and 20 `artifact-template-*` skills. Their plugin manifests declare `Proprietary`; they are left out of this shared collection.
- Claude plugin marketplace checkouts and temporary download directories: these are not treated as installed skills.

The source validator accepts 21 of the 24 imported skills. It flags existing extended frontmatter in `codebase-overview` (`context`, `routing`, `user-invocable`), `ponytail` (`argument-hint`), and `use-code-wiki` (`disable-model-invocation`). These fields are preserved rather than changing upstream behavior to satisfy a narrower validator.

## Installation

Copy or symlink any skill directory you want into your local Codex skills directory.

Example:

```bash
mkdir -p ~/.codex/skills
cp -R skills/grounded-file-qa ~/.codex/skills/
```

## Notes

- These skills are designed for a local Codex-style workflow.
- Some skills depend on local CLI tools such as `pdfinfo`, `pdftotext`, `upower`, `node`, or network access.
- Bundled system skills are snapshots; there is no need to install a second copy if your client already supplies them.
- GitHub plugin skills may require the corresponding GitHub app connection or authenticated `gh` CLI. Copying a skill does not install or configure its plugin.
- Read each skill's `SKILL.md` for usage details and constraints.

## License

Repository-authored material is MIT. See [LICENSE](LICENSE). Imported skills retain their upstream license notices and terms; the root license does not relicense third-party material. Check the license files and provenance of each imported skill before redistribution.
