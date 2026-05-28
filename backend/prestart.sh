#!/bin/bash

set -e

echo "Running prestart.sh script..."
alembic upgrade head
echo "Prestart.sh script completed."

exec "$@"
