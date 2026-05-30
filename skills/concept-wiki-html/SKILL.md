---
name: concept-wiki-html
description: Build a static, local-source-grounded HTML knowledge page from course notes and slides, organized as one big topic with clickable concept nodes and deeper sub-concepts. Use when the user asks to turn local Markdown notes, PDFs, PPT/PPTX, or slide folders into a wiki-like HTML page, concept map, knowledge network, or layered clickable study webpage; especially when they want content drawn only from local notes/courseware and placed in an exact output folder.
---

# Concept Wiki HTML

## Overview

Create a single-topic knowledge webpage whose content is grounded in local source files. The page should behave like a concept network: clicking a concept such as `进程` reveals its definition, composition, related concepts, and clickable child concepts such as `PCB`, which can then be opened for deeper details.

## Workflow

1. Identify the exact source and output paths from the user request.
   - Source examples: `Note/operationSystem/CPU虚拟化`, `slides/operationSystem`.
   - Output example: `Note/operationSystem/CPU虚拟化/noteHtml`.
   - Preserve the user’s requested destination exactly; create a new output folder when requested.

2. Read local sources before designing the page.
   - List Markdown notes and relevant slide/PDF files.
   - Extract slide text with `pdftotext -layout` for PDFs when available.
   - Sample nearby notes to match terminology density and course style.
   - Do not add internet material unless the user explicitly allows it; if the user says local-only, use only local sources.

3. Model the content as one concept graph, not as separate chapters.
   - Root node should be the big topic, for example `CPU 虚拟化`.
   - Each important term becomes a node: `进程`, `PCB`, `进程状态`, `fork()`, `exec()`, `系统调用`, `Trap Table`, `时钟中断`, `上下文切换`, `调度器`, `MLFQ`, `CFS`, `多处理器调度`.
   - Nodes should have `definition`, `why`, `details`, `children`, and `relations`.
   - Use hierarchy where the course naturally has composition: `进程` -> `进程的主要构成` -> `PCB` -> `程序计数器/寄存器/栈指针/调度信息`.

4. Build the static webpage.
   - Use `index.html`, `assets/styles.css`, and `assets/app.js` unless there is a clear reason to split further.
   - Make the first screen the actual knowledge interface, not a landing page.
   - Provide a concept index, current concept panel, child concept cards, related concept cards, detail blocks, breadcrumbs, home/back controls, and search.
   - Opening the HTML directly from disk should work; avoid requiring a dev server.

5. Keep page text knowledge-focused.
   - Do not put meta text such as “内容仅来自你的笔记”, “点击任意知识节点”, “不是按 7 个文件拆开”, or “本页依据”.
   - Navigation labels can be short and functional, such as `下层概念`, `相关概念`, `概念检索`.
   - Intro text should explain the topic itself, not the webpage design or source policy.

6. Validate before finishing.
   - Run `node --check <output>/assets/app.js`.
   - Search for non-knowledge meta text if the user requested a clean study page.
   - Confirm all output files exist under the requested output folder.

## Content Rules

- Prefer completeness over a short overview. The output should feel closer to a course wiki than a summary card page.
- Preserve the course’s terminology and language style. For Chinese OS notes, keep Chinese explanations with English technical terms where the notes use them.
- Keep claims grounded in the inspected notes/slides. If a concept is not in the local source, do not add it unless the user asks for external expansion.
- Avoid organizing the final experience by source file count. A folder with 7 notes can still produce one unified topic tree.
- Include formulas and command examples when they appear in the source, for example `T_turnaround`, `T_response`, `vruntime`, `nice`, `pstree`, `strace`, `taskset`.

## HTML Interaction Pattern

Use this mental model for `assets/app.js`:

```js
const knowledge = {
  root: {
    title: "大主题",
    subtitle: "一句知识性副标题",
    definition: "概念定义",
    why: ["为什么需要它", "它解决什么问题"],
    details: [{ title: "细节组", items: ["要点 1", "要点 2"] }],
    children: ["child-node"],
    relations: ["related-node"]
  }
};
```

The UI should render one `currentNode` at a time and make every child/relation card clickable. Maintain a breadcrumb or back stack so the user can move upward through the concept hierarchy.
