#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$SCRIPT_DIR"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
ENV_FILE="$ROOT_DIR/.env"
VENV_DIR="$PROJECT_DIR/.venv"
PROFILES_DIR="$PROJECT_DIR/.dbt"

if [[ ! -f "$ENV_FILE" ]]; then
  echo "Missing env file: $ENV_FILE"
  exit 1
fi

if [[ ! -d "$VENV_DIR" ]]; then
  echo "Missing virtualenv: $VENV_DIR"
  echo "Create it first with: python3 -m venv $VENV_DIR"
  exit 1
fi

if [[ ! -f "$PROFILES_DIR/profiles.yml" ]]; then
  echo "Missing dbt profile: $PROFILES_DIR/profiles.yml"
  exit 1
fi

DATABASE_URL_LINE="$(grep -E '^DATABASE_URL=' "$ENV_FILE" || true)"
if [[ -z "$DATABASE_URL_LINE" ]]; then
  echo "DATABASE_URL not found in $ENV_FILE"
  exit 1
fi

DATABASE_URL_VALUE="${DATABASE_URL_LINE#DATABASE_URL=}"
DATABASE_URL_VALUE="${DATABASE_URL_VALUE%\"}"
DATABASE_URL_VALUE="${DATABASE_URL_VALUE#\"}"
DATABASE_URL_VALUE="${DATABASE_URL_VALUE%\'}"
DATABASE_URL_VALUE="${DATABASE_URL_VALUE#\'}"

if [[ "$DATABASE_URL_VALUE" != postgresql://* ]]; then
  echo "DATABASE_URL does not look valid"
  exit 1
fi

PASSWORD_PART="${DATABASE_URL_VALUE#postgresql://}"
PASSWORD_PART="${PASSWORD_PART#*:}"
PASSWORD_PART="${PASSWORD_PART%@*}"

if [[ -z "$PASSWORD_PART" ]]; then
  echo "Unable to parse password from DATABASE_URL"
  exit 1
fi

export DBT_ENV_SECRET_PG_PASSWORD="$PASSWORD_PART"

# shellcheck source=/dev/null
source "$VENV_DIR/bin/activate"

cd "$PROJECT_DIR"

echo "Running dbt debug..."
dbt debug --profiles-dir "$PROFILES_DIR"

echo "Running dbt run..."
dbt run --profiles-dir "$PROFILES_DIR"

echo "dbt completed successfully."
