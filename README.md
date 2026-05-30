# AgentSkills

A small open-source collection of Codex skills for local workflows, study pipelines, and lightweight automation.

## Included Skills

| Skill | What it does |
| --- | --- |
| `ai-paper-digest` | Collects recent AI papers and supports follow-up paper analysis. |
| `battery-status` | Reads local battery and charging information in a compact format. |
| `concept-wiki-html` | Builds a local-source-grounded concept-network HTML study page. |
| `grounded-file-qa` | Ingests local files, especially PDFs, for evidence-grounded Q&A. |
| `lecture-note-writer` | Writes or rewrites course notes from slides in the user's note style. |

## Repository Layout

```text
skills/
  ai-paper-digest/
  battery-status/
  concept-wiki-html/
  grounded-file-qa/
  lecture-note-writer/
```

Each skill keeps its own `SKILL.md` plus any supporting scripts, references, or agent metadata.

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
- Read each skill's `SKILL.md` for usage details and constraints.

## License

MIT. See [LICENSE](LICENSE).
