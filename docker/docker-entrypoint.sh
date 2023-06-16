#!/bin/sh

# exit the script if any statement returns a non-true return value.
set -o errexit
# exit in case of uninitialised variable in shell script
set -o nounset

function start_runserver_local() {
  cd /app/backend/
  uvicorn backend.app:app --host 0.0.0.0 --reload --port 8000
}

case "$1" in
  runserver_local)
    start_runserver_local
  ;;
  *)
   exec $@
  ;;
esac
