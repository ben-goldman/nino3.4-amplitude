#!/usr/bin/env bash
set -euo pipefail

source="articles/references.bib"

targets=(
    "presentations/presentation/references.bib"
    "paperwork/paper/references.bib"
)

for t in $targets
do
    cp $source $t
done
