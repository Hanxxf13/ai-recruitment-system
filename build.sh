#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Download the Spacy model for AI screening
python -m spacy download en_core_web_sm
