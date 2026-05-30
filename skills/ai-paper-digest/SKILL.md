---
name: ai-paper-digest
description: Collect and summarize recent AI papers with emphasis on major ML/AI venues, journals, arXiv, and paper-discovery sites. Use when Codex needs to build a daily or topical AI paper digest, rank papers from venues such as ICML/NeurIPS/ICLR/CVPR/AAAI/KDD, give short Chinese introductions, or continue with follow-up analysis of a specific paper's methods, contributions, experiments, and limitations.
---

# AI Paper Digest

Use this skill to produce a compact, source-aware AI paper briefing first, then continue into deeper paper analysis on demand.

## Quick Start
- For a daily digest, run `scripts/fetch_ai_digest.py` to collect recent papers from arXiv, OpenAlex journals, and selected paper-discovery feeds.
- Use [references/source-priority.md](references/source-priority.md) to decide which venues and sites to prioritize for the user's request.
- Return a short Chinese introduction for each paper:
  1. what the paper studies
  2. the core idea or method at a high level
  3. why it may matter
- When the user points to one paper for deeper analysis, switch from digest mode to paper-analysis mode and work from the paper abstract, official page, PDF, or local file.

## Workflow

### 1. Decide the task mode
- Use `daily-digest` when the user wants today's or recent papers across sources.
- Use `venue-focused` when the user cares about conferences or journals such as ICML, NeurIPS, ICLR, CVPR, COLT, TPAMI, or TMLR.
- Use `single-paper-analysis` when the user asks about one named paper, one link, one PDF, or a follow-up such as "这篇论文的方法是什么".

### 2. Build the source set
- Default priority order:
  1. arXiv daily preprints for freshness
  2. Hugging Face Papers for community-visible daily papers
  3. OpenAlex journal results for recent journal articles
  4. Official proceedings or venue pages for venue-specific retrieval
  5. Secondary discovery sites such as Aminer, Paper Copilot, Bohrium for navigation and triangulation
- Treat the user's preferred venues as a ranking hint, not a reason to ignore fresher relevant papers from other sources.
- Prefer official or primary sources when available. Use discovery sites to locate papers faster, then link back to the paper page, proceedings page, arXiv page, DOI page, or PDF.

### 3. Produce the digest
- Group or tag papers by venue family where possible: core ML, theory, vision, broad AI, data mining, journals, or community picks.
- Keep each paper entry compact unless the user asks for depth.
- Include:
  - title
  - source and venue guess
  - date or recency basis
  - paper link
  - 2-4 sentence Chinese introduction
- If "today" is ambiguous because a source updates weekly or irregularly, say the exact time basis, for example "近 24 小时 arXiv" or "近 7 天期刊文章".

### 4. Continue into single-paper analysis
- For a follow-up on one paper, gather the best available source in this order:
  1. local PDF or local note from the user
  2. official abstract or proceedings page
  3. arXiv abstract or PDF
  4. publisher abstract page
- If a local PDF is provided, use `$grounded-file-qa` for evidence-grounded reading and page-aware follow-ups.
- For method analysis, structure the answer with:
  1. problem setting
  2. proposed method
  3. model or algorithm components
  4. training or optimization strategy
  5. experiments and findings
  6. limitations or assumptions
- Separate direct evidence from inference. If the method cannot be confirmed from the abstract alone, say that and request or fetch the PDF before going deeper.

## Venue Coverage

Use the venue registry in [references/source-priority.md](references/source-priority.md). The main target set includes:
- Core ML: ICML, NeurIPS, ICLR
- Theory: COLT, AISTATS
- Vision: CVPR, ICCV, ECCV
- Broad AI: AAAI, IJCAI
- Data mining: KDD, ICDM
- Journals: IEEE TPAMI, IEEE TKDE, JMLR, Machine Learning, Artificial Intelligence, TMLR
- Additional sources: arXiv, Hugging Face Papers, Aminer, Paper Copilot, Bohrium, Hugging Face Blog

## Scripts

### `scripts/fetch_ai_digest.py`
- Use this script for a reusable, dependency-light first pass over recent AI papers.
- It fetches:
  - recent arXiv AI/ML categories
  - recent OpenAlex journal articles filtered for AI-related topics
  - Hugging Face Papers page headlines
- It ranks results with simple heuristics and prints JSON, so the result can be reformatted into markdown or fed into later analysis steps.

Example:

```bash
python3 skills/ai-paper-digest/scripts/fetch_ai_digest.py --days 3 --limit 20
```

### When to skip the script
- Skip the script if the user already provided a specific paper or PDF.
- Skip the script if the task is only to explain one known paper.
- Skip the script if the environment blocks network and no cached or local sources are available.

## Response Style
- Answer in Chinese unless the user asks otherwise.
- For digest entries, optimize for scanability and avoid long abstracts pasted verbatim.
- For deeper paper analysis, use clear headings and concise technical language.
- Do not overclaim novelty or results if only titles or abstracts are available.

## Failure Handling
- If a source is temporarily unavailable, say which source failed and continue with the remaining sources.
- If a venue page is difficult to scrape, fall back to discovery sites or search, then verify the target paper page before summarizing.
- If the user asks for "today's hottest" papers, explain the ranking basis because there is no single authoritative AI-wide hotness metric.

## Prompt Patterns
- `Use $ai-paper-digest to give me today's AI papers with short Chinese intros.`
- `Use $ai-paper-digest to focus on ICLR, NeurIPS, ICML, and arXiv papers from the last 3 days.`
- `Use $ai-paper-digest to find recent CVPR and ICCV related papers and tell me which ones are worth reading first.`
- `Use $ai-paper-digest to summarize this paper first, then explain its method and experiments.`
