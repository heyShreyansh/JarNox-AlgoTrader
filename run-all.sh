#!/usr/bin/env bash
set -euo pipefail

# config — edit if your folders differ
BACKEND_DIR="$HOME/jarnox_algo_trader/jarnox_algo_trader"
FRONTEND_DIR="$HOME/jarnox-dashboard"
CONDA_ENV="jarnox"
BACKEND_LOG="$HOME/jarnox_algo_trader/backend.log"
BACKEND_PORT=5000
FRONTEND_URL="http://localhost:3000"

echo "=== run-all.sh starting — cleaning port ${BACKEND_PORT} if needed ==="
# kill anything on port 5000 (no error if nothing found)
lsof -ti :${BACKEND_PORT} | xargs -r kill -9 || true

# start backend in conda env, background, log to file
echo "Starting backend in conda env '${CONDA_ENV}' (logging to ${BACKEND_LOG})..."
# use 'conda run' so we don't rely on interactive 'source activate' semantics
conda run -n "${CONDA_ENV}" python "${BACKEND_DIR}/app.py" > "${BACKEND_LOG}" 2>&1 &

BACK_PID=$!
echo "Backend PID: ${BACK_PID}"
# give backend a few seconds to bootstrap
echo -n "Waiting for backend to accept connections"
for i in {1..12}; do
  if nc -z 127.0.0.1 ${BACKEND_PORT}; then
    echo " -> backend is up."
    break
  fi
  echo -n "."
  sleep 1
done
echo

if ! nc -z 127.0.0.1 ${BACKEND_PORT}; then
  echo "WARNING: backend did not start within timeout. Check ${BACKEND_LOG} for details."
  echo "tail -n 200 ${BACKEND_LOG}"
fi

# open frontend URL in default browser
echo "Opening frontend at ${FRONTEND_URL}"
open "${FRONTEND_URL}" || echo "Could not open browser automatically."

# start the frontend in the foreground (so you can ctrl+c to stop)
echo "Starting frontend (run 'Ctrl+C' here to stop the frontend)."
cd "${FRONTEND_DIR}"
npm start
