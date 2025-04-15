#!/bin/bash
set -e

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf dist/ target/wheels/

# Build with maturin
echo "Building package with maturin..."
maturin build --uv

# List contents of the wheel file to check what's included
echo ""
echo "Contents of the wheel file:"
cd dist
WHEEL_FILE=$(ls *.whl | head -1)
echo "Wheel file: $WHEEL_FILE"
echo ""
echo "Checking wheel contents..."
unzip -l "$WHEEL_FILE" | grep -v "__pycache__" | head -40

echo ""
echo "Checking for test files..."
unzip -l "$WHEEL_FILE" | grep -E 'test|data/' || echo "No test files found (good!)"

echo ""
echo "Build completed successfully"