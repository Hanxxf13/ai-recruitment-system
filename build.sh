#!/usr/bin/env bash
set -o errexit

echo "=== Installing dependencies ==="
pip install --upgrade pip
pip install -r requirements.txt

echo "=== Creating data directories ==="
mkdir -p backend/data/resumes

echo "=== Build complete ==="
