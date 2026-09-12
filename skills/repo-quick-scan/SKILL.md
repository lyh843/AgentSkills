---
name: repo-quick-scan
description: Quickly understand a repository through a shallow, read-only scan without reading every file. Use when the user asks for a quick repository overview or initial orientation, especially "快速理解仓库" or "不要逐文件阅读". Not for exhaustive architecture documentation, full-source reading, or code review.
---

# Repo Quick Scan

Build a concise working understanding of the requested repository, not a complete inventory. Use the user's language for the report.

## Scan Strategy

- Identify the repository root from the supplied path or current workspace. If multiple repositories are plausible and no target is clear, ask which one to scan.
- Respect repository instructions. Inspect the top-level directory layout, README, dependency manifests, and build or launch configuration first.
- Prefer `rg --files` for discovery and targeted `rg` searches for entry points, imports, routing, and module wiring. Exclude dependency directories, generated output, caches, and large data files from exploration.
- Read only relevant portions of a small selection of entry files and core modules to establish the main execution or data flow. Do not read source files one by one, dump the entire repository, or delegate exhaustive reading.
- Stop once the seven report sections have enough evidence. Leave unresolved details explicitly unconfirmed rather than expanding into a deep investigation.
- Keep the scan read-only. Do not install dependencies, run the application or tests, modify files, or generate documentation artifacts unless separately requested.

## Required Output

Return these seven numbered sections, in order. Keep each section brief and cite relevant repository paths for key claims.

1. **项目用途**: What the project does and its main use case.
2. **技术栈**: Languages, frameworks, storage, and build tools supported by the manifests or code. Mention versions only when declared.
3. **一级目录作用**: A compact list or table describing the top-level directories. Group generated or vendor directories when appropriate; do not recurse into a file inventory.
4. **入口文件**: Main application, CLI, or service entry paths and how launch configuration reaches them. If there is no single entry point, say so.
5. **核心模块关系**: Explain the main dependency, call, or data flow using a short chain or a few bullets. Distinguish confirmed relationships from inferences.
6. **如何运行**: Give prerequisites and commands found in repository documentation or configuration, including the working directory and required configuration names. Do not expose secret values. State that commands were not executed, and flag missing or conflicting instructions.
7. **修改代码时需要注意的位置**: Identify concrete paths that need coordinated changes, such as shared interfaces, configuration, schema or migrations, generated code, and relevant tests. Include only concerns supported by the scan, not a generic review checklist.

When evidence is absent, say "未确认" or its equivalent in the user's language. Do not invent entry points, commands, or module relationships to fill a section.
