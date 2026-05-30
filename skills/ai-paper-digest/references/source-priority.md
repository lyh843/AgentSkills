# Source Priority

Use this file to decide where to collect papers from and how to rank or label them.

## 1. Priority Venues

### Core machine learning
- ICML
- NeurIPS
- ICLR

### Machine learning theory
- COLT
- AISTATS

### Computer vision
- CVPR
- ICCV
- ECCV

### Broad AI
- AAAI
- IJCAI

### Data mining
- KDD
- ICDM

### Journals
- IEEE TPAMI
- IEEE TKDE
- Journal of Machine Learning Research
- Machine Learning
- Artificial Intelligence
- Transactions on Machine Learning Research

## 2. Source Order By Task

### Daily or recent digest
1. arXiv
2. Hugging Face Papers
3. OpenAlex recent journal search
4. Official venue pages when a venue is currently active or the user requests it
5. Aminer, Paper Copilot, Bohrium, Hugging Face Blog as supplemental discovery

### Venue-specific lookup
1. Official proceedings or official conference site
2. OpenReview when the venue uses it
3. arXiv version if available
4. Aminer or Paper Copilot for convenient navigation

### Single-paper follow-up
1. User-provided local PDF or note
2. Official proceedings page or publisher page
3. arXiv abstract or PDF
4. Community mirrors only as fallback

## 3. Suggested Venue Hints

Use title, URL, source labels, or page text to infer venue tags:
- `neurips`, `nips`
- `icml`
- `iclr`
- `cvpr`
- `iccv`
- `eccv`
- `aaai`
- `ijcai`
- `kdd`
- `icdm`
- `aistats`
- `colt`
- `tpami`
- `tkde`
- `jmlr`
- `tmlr`

Treat venue inference as provisional unless confirmed by the paper page.

## 4. Recommended Output Fields
- `title`
- `paper_url`
- `source_name`
- `venue`
- `published_or_seen_date`
- `authors`
- `short_intro_zh`
- `method_keywords`
- `reason_to_watch`

## 5. Notes
- arXiv is best for freshness, but many papers have no final venue yet.
- Conference proceedings are best for canonical venue attribution, but they are not daily streams year-round.
- Journal platforms often expose publisher metadata but not a clear "hot" ranking, so use recency plus citations or visibility as heuristics.
- Discovery sites are useful for breadth and navigation, but should not be treated as the final authority when a primary paper page exists.
