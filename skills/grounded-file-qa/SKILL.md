---
name: grounded-file-qa
description: Read one or more local files, especially PDFs, and answer follow-up questions grounded in those sources. Use when the user wants Codex to ingest files first, keep track of evidence across later questions, compare multiple documents, extract key points or terminology, cite file or page anchors, or build a compact working note from a document set.
---

# Grounded File QA

## Overview
Use this skill for source-grounded reading workflows. The job is not just "summarize this once", but "read these files now and keep answering later questions from them."

## Workflow
1. Identify the source bundle.
   - Collect the exact local file paths the user provided.
   - Start reading immediately unless the goal changes the reading strategy in a material way.
   - Treat the provided files as the primary source of truth unless the user explicitly asks for outside knowledge.

2. Build a scratch bundle when the task is larger than one quick answer.
   - Prefer a scratch folder such as `/tmp/grounded-file-qa/<topic>/`.
   - Run `scripts/ingest_documents.sh <scratch-dir> <file1> ...` to extract PDF text and normalize text-like files.
   - Read `manifest.tsv` first to see which files were extracted cleanly and which need fallback handling.
   - Read `source_map.md` for a fast human-readable overview and `page_manifest.tsv` when page-level anchors matter.
   - If the user only gave one short text file, skip the scratch folder and read it directly.

3. Read in passes.
   - First pass: map each file's purpose, structure, and likely relevant sections.
   - Second pass: extract the evidence needed for the current question.
   - For PDFs, prefer the page shards under `pages/<id>/pNNN.txt` so answers can cite `filename p.N`.
   - For multiple files, record agreements, conflicts, and gaps instead of merging everything blindly.

4. Maintain a compact evidence sheet for later turns.
   - Prefer a markdown note in the scratch dir such as `evidence.md`.
   - Use [references/evidence-sheet-template.md](references/evidence-sheet-template.md) when the task has multiple files or many follow-up questions.
   - Keep only high-signal items: per-file summary, glossary, timeline, formulas, unresolved ambiguities, and page anchors.
   - Update the sheet instead of re-reading everything from zero when the conversation continues.
   - If the user wants study or interview prep, also maintain `question_bank.md` with likely follow-up questions.

5. Answer with grounded claims.
   - Cite the source file for non-obvious claims.
   - Add page anchors for PDFs and section headings or line spans for text files when practical.
   - Separate direct evidence from your inference.
   - If a question cannot be answered from the files, say that before adding outside knowledge.

## PDF Handling
- Prefer `pdftotext -layout` through the ingest script for readable extraction.
- Prefer `pdfinfo` page counts plus the generated `pages/` directory when page-level lookup will matter later.
- If extraction is noisy but usable, answer cautiously and cite short anchors.
- If the PDF is image-only or badly scanned, say OCR is needed and do not pretend the text is reliable.
- Ignore headers, footers, page numbers, watermarks, and repeated slide chrome unless they matter.

## Multi-file Patterns
- For comparison requests, build a table with columns such as source, claim, evidence, and confidence.
- For study or report files, keep a glossary of terms, symbols, acronyms, and formulas.
- For policy or requirement sets, track conflicts and the latest controlling source if dates or versions are present.
- For code plus PDF/context mixes, treat executable behavior and source files as first-party evidence and use the PDF as explanatory context.

## Extra Capabilities
Use the same source bundle to optionally provide:
- a 5-10 line executive summary
- a glossary or concept map
- a question bank for revision or interview prep
- a comparison matrix across files
- a list of contradictions or open questions
- a reusable brief file for later turns
- a per-page lookup path for later precise quoting or citation

## Reliability Rules
- Do not claim to have read a file you have not opened or extracted.
- Do not turn weak OCR or garbled extraction into confident prose.
- Prefer "the file suggests" over certainty when evidence is partial.
- Keep quotes short and only when they materially help.
- If later answers depend on a cached note, refresh the original source before making a high-stakes claim.

## Fast Prompt Patterns
- `Use $grounded-file-qa to read these PDFs first, then answer my later questions from them.`
- `Use $grounded-file-qa to compare these two papers and keep a running evidence note.`
- `Use $grounded-file-qa to ingest this folder of PDFs and build a glossary plus summary for follow-up Q&A.`
- `Use $grounded-file-qa to read the provided files and answer only from those sources unless I ask otherwise.`
