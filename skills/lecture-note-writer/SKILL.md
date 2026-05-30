---
name: lecture-note-writer
description: Use when the user wants course notes or study notes written from local slide PDFs, PPTs, or existing markdown notes, especially when the notes should match the user's existing style. This skill reads the source material, samples nearby notes to infer structure and tone, then writes or rewrites the target markdown in a consistent format.
---

# Lecture Note Writer

## Overview
This skill is for note-production workflows where source material and house style both matter. Use it when the user wants you to read lecture slides or existing notes, infer the user's note style from nearby files, and then create or rewrite a target markdown file in that same style.

## When To Use
- The user asks to read a local PDF or PPT and turn it into a markdown note.
- The user asks to rewrite a note based on nearby notes in the same subject folder.
- The user wants multiple note files written in the same format and tone.
- The user explicitly asks to "match my style", "follow my existing notes", or similar.

Do not use this skill for:
- Plain summarization of text the user already pasted inline with no file work.
- Creative writing unrelated to study notes.
- Cases where the user wants a brand new format and does not want style matching.

## Workflow
1. Identify inputs.
   Required inputs are:
   - source material such as a local PDF, PPT, or existing note
   - target markdown path to create or rewrite
   Helpful context:
   - neighboring notes in the same topic directory

2. Read the source material first.
   - Prefer direct text extraction from PDF when possible.
   - Capture the chapter flow, definitions, examples, formulas, and any explicit comparisons.
   - Ignore slide boilerplate such as teacher name, school logo, and duplicate headings unless useful.

3. Infer the user's note style from nearby notes.
   Sample 2-5 related notes from the same subject area and extract:
   - heading style such as `#`, `##`, numbered sections, and separators like `---`
   - language mix such as English titles with Chinese terminology notes
   - density of bullets vs prose
   - typical formula formatting
   - how examples and summaries are labeled
   - whether the notes are terse outline style or more explanatory

4. Build the target outline from content, not from the slide page order alone.
   Preferred structure:
   - intro / motivation
   - core idea
   - mechanism or algorithm
   - worked examples
   - pros / cons / trade-offs
   - summary
   - connection to next topic when relevant

5. Write or rewrite the target markdown.
   - Preserve the user's existing style where it is stable.
   - Normalize obvious inconsistencies only when they make the note clearer.
   - Keep terminology accurate even if the user's style is informal.
   - If the target file is empty, create a full note from scratch.
   - If the target file already has useful content, integrate rather than overwrite blindly.

6. Verify coherence before finishing.
   Check:
   - section order is logical
   - formulas and numeric examples are correct
   - terminology is consistent across the note
   - the note connects cleanly with adjacent topics

## Writing Rules
- Match the user's local note style before introducing your own preferences.
- Prefer concise bullets over long paragraphs unless nearby notes are prose-heavy.
- Keep titles and subsection naming consistent with neighboring files.
- Use bilingual terminology naturally when the user's notes do that.
- Keep examples concrete; do not leave placeholder text such as `==ppt中图片==` unless the user uses that intentionally.
- Do not pad the note with generic textbook filler.
- If a slide deck is shallow, produce a short note; if the deck is dense, produce a fuller note.

## Output Pattern
When the local notes follow the style seen in this workspace, a good default shape is:
- `# Topic Name`
- `---`
- `## 01. Intro`
- `## 02. Core Idea`
- `## 03. Example / Translation / Mechanism`
- `## 04. Problems / Trade-offs`
- `## 05. Summary`
- `## 06. Connection to Next Part`

Adjust this shape if nearby notes clearly use a different one.

## Fast Prompt Patterns
Use prompts like:
- `Use $lecture-note-writer to read slides/operationSystem/2_7-虚拟化-快速地址转换.pdf, infer my style from Note/operationSystem, and rewrite Note/operationSystem/内存虚拟化/快速地址转换.md.`
- `Use $lecture-note-writer to read this PDF and rewrite the target note in the same style as nearby markdown files.`
- `Use $lecture-note-writer to complete the missing notes in this folder with the same structure as the existing ones.`
