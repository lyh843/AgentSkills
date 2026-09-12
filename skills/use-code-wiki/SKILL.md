---
name: use-code-wiki
description: Navigate a documented Git repository through .code-wiki/wiki.json to locate implementation files, plan changes, and answer codebase-structure questions. Use when a Code Wiki index exists and repository exploration should proceed from summaries to headers to full source.
disable-model-invocation: true
---

# Use Code Wiki

Use the Code Wiki as a progressive navigation cache. Treat current source code as authoritative.

## Workflow

1. Resolve the target Git root.
2. Run `python3 scripts/query_index.py --root <absolute-root> --json status` from this skill directory.
3. If the index is absent, invalid, or unsupported, stop using it and recommend `build-code-wiki`.
4. Run `python3 scripts/query_index.py --root <absolute-root> --json show .` for repository orientation.
5. Query only directory nodes relevant to the request.
6. Shortlist files from their summaries.
7. Read the managed headers of shortlisted files.
8. Read complete files only when implementation detail is required or an entry is stale.
9. Read adjacent tests and configuration before editing.
10. Verify claims against current source before answering or modifying code.
11. Recommend `build-code-wiki` after source changes.

## Query operations

- Use `show <relative-path>` for one repository, directory, or file node.
- Use `stale` only when freshness affects the task.
- Never pass absolute paths or paths containing `..`.
- Do not load the complete index when targeted subtree queries are sufficient.

Read [wiki.schema.json](references/wiki.schema.json) only when schema interpretation or validation detail is required.
