#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Run migrations
python ecombabyshoppingproject/manage.py migrate

# Gather static files
python ecombabyshoppingproject/manage.py collectstatic --no-input
