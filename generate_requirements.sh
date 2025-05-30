#!/bin/bash
set -e

PACKAGE_DIR="./pyrsgis"
OUTPUT_FILE="$(pwd)/requirements.txt"

echo "Running pipreqs on $PACKAGE_DIR..."
pipreqs "$PACKAGE_DIR" --force --savepath "$OUTPUT_FILE"

echo "✅ Saved minimal requirements to $OUTPUT_FILE"
