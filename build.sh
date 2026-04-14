#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

if [ -n "${ADMIN_NAME:-}" ] && [ -n "${ADMIN_EMAIL:-}" ] && [ -n "${ADMIN_USERNAME:-}" ] && [ -n "${ADMIN_PASSWORD:-}" ]; then
  python manage.py create_admin_user \
    --name "$ADMIN_NAME" \
    --email "$ADMIN_EMAIL" \
    --username "$ADMIN_USERNAME" \
    --password "$ADMIN_PASSWORD" \
    --status active
fi
