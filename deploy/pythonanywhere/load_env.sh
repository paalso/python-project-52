#!/bin/bash

# Load environment variables from .env file
# Usage: source deploy/load_env.sh

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  echo "❌ Please run this script with: source ./load_env.sh"
  exit 1
fi

set -o allexport
source ./.env
#source "$(dirname "$0")/../.env"
set +o allexport

echo "✅ Environment variables loaded from .env"
echo "-----------------------------------------"
grep -vE '^\s*#' .env | grep -E '^\s*[A-Za-z_][A-Za-z0-9_]*=' | while IFS='=' read -r key _; do
    value="${!key}"
    if [[ "$key" == "SECRET_KEY" ]]; then
        echo "$key: [hidden]"
    else
        echo "$key: $value"
    fi
done
echo "-----------------------------------------"
