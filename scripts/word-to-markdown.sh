#!/usr/bin/env bash
# Converts Word documents in word/ to Jekyll Markdown with Pandoc.
#
#   word/midlife-musings/My post.docx            -> _posts/<today>-my-post.md
#   word/midlife-musings/2025-07-04 My post.docx -> _posts/2025-07-04-my-post.md
#   word/my-approach/My case.docx                -> _my_approach/<today>-my-case.md
#   word/data-work/My study.docx                 -> _data_work/<today>-my-study.md
#   word/pages/My page.docx                      -> _pages/my-page.md  (URL /my-page/)
#
# A document anywhere else in word/ is not converted, and the script exits
# with an error naming it so the GitHub Action shows it failed.
#
# Images in the document go to assets/images/uploads/word/<slug>/.
# Re-uploading a document updates the same post or page, and keeps any
# front matter (categories, excerpt, ...) you have added to it by hand.
#
# Usage: scripts/word-to-markdown.sh [file.docx ...]   (no args = all of word/)
set -euo pipefail
cd "$(dirname "$0")/.."

if [ "$#" -eq 0 ]; then
  mapfile -d '' files < <(find word -type f -name '*.docx' ! -name '~$*' -print0)
  set -- "${files[@]}"
fi

title_template=$(mktemp)
trap 'rm -f "$title_template"' EXIT
printf '%s\n' '$title$' > "$title_template"

misplaced=()
for src in "$@"; do
  [ -f "$src" ] || { echo "Skipping $src (not found)"; continue; }
  name=$(basename "$src" .docx)

  date=""
  if [[ "$name" =~ ^([0-9]{4}-[0-9]{2}-[0-9]{2})[-_\ ]+(.*)$ ]]; then
    date=${BASH_REMATCH[1]}
    name=${BASH_REMATCH[2]}
  fi
  slug=$(printf '%s' "$name" | iconv -f utf-8 -t ascii//TRANSLIT 2>/dev/null || printf '%s' "$name")
  slug=$(printf '%s' "$slug" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g; s/^-+|-+$//g')
  [ -n "$slug" ] || { echo "Skipping $src (no usable file name)"; continue; }

  # Blog posts, My Approach and Data Work entries are dated files in their
  # folder; pages are named after the file.
  case "$src" in
    word/midlife-musings/*) kind=post; dir=_posts ;;
    word/my-approach/*) kind=post; dir=_my_approach ;;
    word/data-work/*) kind=post; dir=_data_work ;;
    word/pages/*) kind=page ;;
    *) misplaced+=("$src"); continue ;;
  esac

  case "$kind" in
    page) out="_pages/$slug.md" ;;
    post)
      existing=$(find "$dir" -name "*-$slug.md" 2>/dev/null | sort | head -n1)
      if [ -z "$date" ] && [ -n "$existing" ]; then
        out=$existing
      else
        out="$dir/${date:-$(date -u +%F)}-$slug.md"
      fi
      ;;
  esac

  media="assets/images/uploads/word/$slug"
  rm -rf "$media"
  body=$(pandoc "$src" --from=docx --to=gfm --wrap=none --extract-media="$media")
  # Root-relative image paths, as used by the rest of the site.
  body=$(printf '%s\n' "$body" | sed -E "s#(\]\(|src=\")$media/#\1/$media/#g")

  # Title: the document's Title property, else a leading "# Heading", else the file name.
  title=$(pandoc "$src" --from=docx --to=plain --template="$title_template" | head -n1)
  first=$(printf '%s\n' "$body" | sed -n '/[^[:space:]]/{p;q}')
  if [[ "$first" =~ ^#\ +(.+)$ ]]; then
    [ -n "$title" ] || title=${BASH_REMATCH[1]}
    if [ "${BASH_REMATCH[1]}" = "$title" ]; then
      # The layout already shows the title, so drop the duplicate heading.
      body=$(printf '%s\n' "$body" | sed '0,/[^[:space:]]/{/[^[:space:]]/d}')
    fi
  fi
  [ -n "$title" ] || title=$(printf '%s' "$name" | sed -E 's/[-_]+/ /g')

  if [ -f "$out" ] && [ "$(head -n1 "$out")" = "---" ]; then
    front=$(awk 'NR==1 { print; next } { print } /^---$/ { exit }' "$out")
  else
    esc=${title//\\/\\\\}
    esc=${esc//\"/\\\"}
    front="---"$'\n'"title: \"$esc\""
    if [ "$kind" = page ]; then
      front+=$'\n'"permalink: /$slug/"
    fi
    front+=$'\n'"---"
  fi

  mkdir -p "$(dirname "$out")"
  printf '%s\n\n%s\n' "$front" "$(printf '%s\n' "$body" | sed '/./,$!d')" > "$out"
  echo "Converted $src -> $out"
done

if [ "${#misplaced[@]}" -gt 0 ]; then
  echo
  echo "Not converted, because these are not in one of the word/ section folders"
  echo "(midlife-musings, my-approach, data-work or pages). Move them into one:"
  printf '  %s\n' "${misplaced[@]}"
  exit 1
fi
