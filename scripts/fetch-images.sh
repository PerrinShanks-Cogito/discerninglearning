#!/usr/bin/env bash
# Downloads the images used by the migrated pages from the original WordPress
# site into assets/images/uploads/. Files that already exist are skipped, so
# once you have committed the images this does nothing.
#
# Usage: ./scripts/fetch-images.sh
set -u
cd "$(dirname "$0")/.."

missing=0
while read -r url; do
  [ -z "$url" ] && continue
  dest="assets/images/uploads/${url#*/wp-content/uploads/}"
  [ -f "$dest" ] && continue
  mkdir -p "$(dirname "$dest")"
  if curl -fsSL --retry 3 -o "$dest.tmp" "$url"; then
    mv "$dest.tmp" "$dest"
    echo "fetched $dest"
  else
    rm -f "$dest.tmp"
    echo "warning: could not download $url" >&2
    missing=$((missing + 1))
  fi
done < scripts/wp-images.txt

# Never fail the build over images; report instead.
[ "$missing" -gt 0 ] && echo "warning: $missing image(s) missing" >&2
exit 0
