#!/usr/bin/env bash
# ============================================================================
# ASIA — Start/Stop Script
# ============================================================================
set -eo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

G='\033[0;32m' B='\033[0;34m' C='\033[0;36m' Y='\033[0;33m' R='\033[0;31m'
BOLD='\033[1m' DIM='\033[2m' RST='\033[0m'

LOG_DIR="$SCRIPT_DIR/.logs"
mkdir -p "$LOG_DIR"
: > "$LOG_DIR/backend.log"
: > "$LOG_DIR/frontend.log"

BACKEND_PID="" ; FRONTEND_PID="" ; DB_STARTED=false

# Kill orphans
lsof -ti:8000 2>/dev/null | xargs kill -9 2>/dev/null || true
lsof -ti:3000 2>/dev/null | xargs kill -9 2>/dev/null || true

cleanup() {
    echo ""
    echo -e "${Y}Arresto servizi...${RST}"
    [[ -n "$FRONTEND_PID" ]] && kill "$FRONTEND_PID" 2>/dev/null; wait "$FRONTEND_PID" 2>/dev/null || true
    [[ -n "$BACKEND_PID" ]]  && kill "$BACKEND_PID"  2>/dev/null; wait "$BACKEND_PID"  2>/dev/null || true
    $DB_STARTED && docker compose down -t 5 >/dev/null 2>&1 || true
    lsof -ti:8000 2>/dev/null | xargs kill -9 2>/dev/null || true
    lsof -ti:3000 2>/dev/null | xargs kill -9 2>/dev/null || true
    echo -e "${G}Fatto.${RST}"
    exit 0
}
trap cleanup SIGINT SIGTERM EXIT

echo -e "${BOLD}"
echo "  ╔═══════════════════════════════════════════╗"
echo "  ║   ASIA — Aggregated Scientific            ║"
echo "  ║          Intelligence for Animals          ║"
echo "  ╚═══════════════════════════════════════════╝"
echo -e "${RST}"

# Prerequisites
command -v docker &>/dev/null || { echo -e "${R}Docker non trovato${RST}"; exit 1; }
docker info &>/dev/null       || { echo -e "${R}Docker non in esecuzione${RST}"; exit 1; }
command -v node &>/dev/null   || { echo -e "${R}Node.js non trovato${RST}"; exit 1; }
command -v python3 &>/dev/null|| { echo -e "${R}Python3 non trovato${RST}"; exit 1; }

if [[ ! -f .env ]]; then
    [[ -f .env.example ]] && cp .env.example .env || echo "GROQ_API_KEY=" > .env
    echo -e "${Y}Creato .env — configura GROQ_API_KEY (https://console.groq.com)${RST}"
fi
set -a; source .env 2>/dev/null || true; set +a
[[ -z "${GROQ_API_KEY:-}" ]] && echo -e "${Y}GROQ_API_KEY non configurata${RST}"

# --- 1. Database ---
echo -e "${G}[db]${RST}       Avvio PostgreSQL..."
docker compose up db -d >/dev/null 2>&1
DB_STARTED=true
for i in $(seq 1 30); do
    docker compose exec -T db pg_isready -U asia &>/dev/null && break
    [[ $i -eq 30 ]] && { echo -e "${R}DB timeout${RST}"; exit 1; }
    sleep 1
done
echo -e "${G}[db]${RST}       Pronto"

# --- 2. Backend (completely detached via script) ---
echo -e "${B}[backend]${RST}  Avvio FastAPI..."
export DATABASE_URL="postgresql+asyncpg://asia:asia@localhost:5432/asia"

# Write a launcher script to fully isolate the process
cat > "$LOG_DIR/.run_backend.sh" << 'LAUNCHER'
#!/usr/bin/env bash
export HF_HUB_DISABLE_PROGRESS_BARS=1
export TOKENIZERS_PARALLELISM=false
export PYTHONWARNINGS="ignore"
export TRANSFORMERS_VERBOSITY=error
export HF_HUB_DISABLE_TELEMETRY=1
export HF_HUB_OFFLINE=0
exec python3 -m uvicorn asia.main:app --host 0.0.0.0 --port 8000 --reload --log-level error
LAUNCHER
chmod +x "$LOG_DIR/.run_backend.sh"

cd backend
nohup bash "$LOG_DIR/.run_backend.sh" >"$LOG_DIR/backend.log" 2>&1 &
BACKEND_PID=$!
cd "$SCRIPT_DIR"

for i in $(seq 1 90); do
    curl -sf http://localhost:8000/api/health >/dev/null 2>&1 && break
    kill -0 "$BACKEND_PID" 2>/dev/null || { echo -e "${R}Backend crashato. Vedi .logs/backend.log${RST}"; exit 1; }
    [[ $i -eq 90 ]] && { echo -e "${R}Backend timeout. Vedi .logs/backend.log${RST}"; exit 1; }
    sleep 1
done
echo -e "${B}[backend]${RST}  Pronto"

# --- 3. Frontend (completely detached via nohup) ---
echo -e "${C}[frontend]${RST} Avvio Next.js..."

cd frontend
npm install --silent >/dev/null 2>&1 || true
nohup env NEXT_PUBLIC_API_URL=http://localhost:8000 npm run dev >"$LOG_DIR/frontend.log" 2>&1 &
FRONTEND_PID=$!
cd "$SCRIPT_DIR"

for i in $(seq 1 30); do
    curl -sf http://localhost:3000 >/dev/null 2>&1 && break
    [[ $i -eq 30 ]] && echo -e "${Y}Frontend lento...${RST}"
    sleep 1
done
echo -e "${C}[frontend]${RST} Pronto"

# --- Ready ---
echo ""
echo -e "${BOLD}${G}  ASIA pronta!${RST}"
echo -e "  Frontend  ${BOLD}http://localhost:3000${RST}"
echo -e "  Backend   ${BOLD}http://localhost:8000${RST}"
echo -e "  API docs  ${BOLD}http://localhost:8000/docs${RST}"
echo -e "  ${DIM}Ctrl+C per arrestare${RST}"
echo ""

# Wait silently
while kill -0 "$BACKEND_PID" 2>/dev/null && kill -0 "$FRONTEND_PID" 2>/dev/null; do
    sleep 2
done
