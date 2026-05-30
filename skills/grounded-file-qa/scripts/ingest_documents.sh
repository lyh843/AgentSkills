#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: ingest_documents.sh <out-dir> <file1> [file2 ...]

Extract PDF text and normalize text-like files into a scratch folder.
Outputs:
  manifest.tsv   tab-separated source status table
  page_manifest.tsv  per-page extraction table for PDFs
  text/          extracted or copied text files
  pages/         per-page PDF text shards when available
  source_map.md  readable summary of the bundle
  evidence.md    starter note for follow-up grounded Q&A
  question_bank.md  starter prompts for later exploration
EOF
}

is_text_extension() {
  case "$1" in
    txt|md|markdown|rst|csv|tsv|json|yaml|yml|xml|html|htm|css|js|jsx|ts|tsx|py|java|c|cc|cpp|h|hpp|go|rs|sh|sql|log)
      return 0
      ;;
    *)
      return 1
      ;;
  esac
}

if [ "$#" -lt 2 ]; then
  usage >&2
  exit 1
fi

out_dir=$1
shift

mkdir -p "$out_dir/text" "$out_dir/pages"
manifest="$out_dir/manifest.tsv"
page_manifest="$out_dir/page_manifest.tsv"
source_map="$out_dir/source_map.md"
evidence="$out_dir/evidence.md"
question_bank="$out_dir/question_bank.md"

printf 'id\tkind\tstatus\tpage_count\toriginal_path\textracted_path\tnote\n' > "$manifest"
printf 'id\tpage\tstatus\textracted_path\tchar_count\tnote\n' > "$page_manifest"
printf '# Source Map\n\n| ID | Type | Status | Pages | Source | Notes |\n| --- | --- | --- | --- | --- | --- |\n' > "$source_map"

extract_pdf_pages() {
  local src=$1
  local page_dir=$2
  local doc_id=$3
  local page_count=$4
  local extracted_any=0
  local page

  mkdir -p "$page_dir"

  for page in $(seq 1 "$page_count"); do
    local page_dest page_status char_count note
    page_dest="$page_dir/p$(printf '%03d' "$page").txt"
    page_status="error"
    char_count=0
    note=""

    if pdftotext -layout -f "$page" -l "$page" "$src" "$page_dest" 2>/dev/null; then
      char_count=$(wc -m < "$page_dest" | tr -d '[:space:]')
      if [ "$char_count" -gt 0 ]; then
        page_status="ok"
        note="page extracted"
        extracted_any=1
      else
        page_status="empty"
        note="no text on page"
      fi
    else
      : > "$page_dest"
      note="pdftotext failed on page"
    fi

    printf '%s\t%s\t%s\t%s\t%s\t%s\n' "$doc_id" "$page" "$page_status" "$page_dest" "$char_count" "$note" >> "$page_manifest"
  done

  if [ "$extracted_any" -eq 1 ]; then
    return 0
  fi

  return 1
}

index=1
for src in "$@"; do
  kind="unknown"
  status="unknown"
  note=""
  page_count="-"
  dest="$out_dir/text/$(printf '%03d' "$index").txt"

  if [ ! -f "$src" ]; then
    printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$index" "$kind" "missing" "$page_count" "$src" "-" "file not found" >> "$manifest"
    printf '| %s | %s | %s | %s | `%s` | %s |\n' "$index" "$kind" "missing" "$page_count" "$src" "file not found" >> "$source_map"
    index=$((index + 1))
    continue
  fi

  base=$(basename "$src")
  ext="${base##*.}"
  lower_ext=$(printf '%s' "$ext" | tr '[:upper:]' '[:lower:]')
  mime=$(file -b --mime-type "$src" 2>/dev/null || printf 'application/octet-stream')

  if [ "$lower_ext" = "pdf" ]; then
    kind="pdf"
    if pdfinfo_output=$(pdfinfo "$src" 2>/dev/null); then
      page_count=$(printf '%s\n' "$pdfinfo_output" | awk '/^Pages:/ {print $2; exit}')
      [ -n "$page_count" ] || page_count="-"
    fi

    if pdftotext -layout "$src" "$dest" 2>/dev/null; then
      if [ -s "$dest" ]; then
        status="ok"
        note="pdf extracted with pdftotext -layout"
      else
        status="empty"
        note="pdf extraction produced empty text; OCR likely needed"
      fi
    else
      : > "$dest"
      status="error"
      note="pdftotext failed; OCR or alternate extraction may be needed"
    fi

    if [ "$page_count" != "-" ]; then
      page_dir="$out_dir/pages/$(printf '%03d' "$index")"
      if extract_pdf_pages "$src" "$page_dir" "$index" "$page_count"; then
        :
      elif [ "$status" = "ok" ]; then
        note="$note; per-page extraction was empty"
      else
        note="$note; per-page extraction unavailable"
      fi
    fi
  elif is_text_extension "$lower_ext" || [[ "$mime" == text/* ]]; then
    kind="text"
    cp "$src" "$dest"
    status="ok"
    note="text-like file copied"
  else
    kind="$mime"
    : > "$dest"
    status="unsupported"
    note="unsupported non-text format"
  fi

  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$index" "$kind" "$status" "$page_count" "$src" "$dest" "$note" >> "$manifest"
  printf '| %s | %s | %s | %s | `%s` | %s |\n' "$index" "$kind" "$status" "$page_count" "$src" "$note" >> "$source_map"
  index=$((index + 1))
done

cat > "$evidence" <<'EOF'
# Evidence Sheet

## Source Map

## Per-file Notes

## Key Facts

## Glossary

## Timeline

## Conflicts And Ambiguities

## Open Questions
EOF

cat > "$question_bank" <<'EOF'
# Question Bank

## Fast Questions
- What are the 5 most important claims in these files?
- Which claims appear in more than one source?
- Which pages or sections are likely to matter most later?

## Comparison Questions
- Where do the sources agree?
- Where do they conflict?
- What is missing or left underspecified?

## Deepening Questions
- Which terms need a glossary entry?
- Which formulas, dates, or named entities should be verified carefully?
- What follow-up reading plan would make later answers faster?
EOF

printf 'Wrote %s\n' "$manifest" >&2
printf 'Wrote %s\n' "$page_manifest" >&2
printf 'Wrote %s\n' "$source_map" >&2
printf 'Wrote %s\n' "$evidence" >&2
printf 'Wrote %s\n' "$question_bank" >&2
