#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Gather static files
python ecombabyshoppingproject/manage.py collectstatic --no-input
