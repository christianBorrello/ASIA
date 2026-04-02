#!/usr/bin/env bash
# ============================================================================
# ASIA — Start/Stop Script
# Avvia tutti i servizi e li termina pulitamente con Ctrl+C
# ============================================================================
set -eo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# ---------------------------------------------------------------------------
# Colori
# ---------------------------------------------------------------------------
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
DIM='\033[2m'
RESET='\033[0m'

# ---------------------------------------------------------------------------
# Log directory
# ---------------------------------------------------------------------------
LOG_DIR="$SCRIPT_DIR/.logs"
mkdir -p "$LOG_DIR"

# ---------------------------------------------------------------------------
# PID tracking
# ---------------------------------------------------------------------------
BACKEND_PID=""
FRONTEND_PID=""
DB_STARTED=false

# ---------------------------------------------------------------------------
# Cleanup — chiamato su SIGINT, SIGTERM, o EXIT
# ---------------------------------------------------------------------------
cleanup() {
    echo ""
    echo -e "${BOLD}${YELLOW}Arresto servizi ASIA...${RESET}"

    # Kill frontend
    if [[ -n "$FRONTEND_PID" ]] && kill -0 "$FRONTEND_PID" 2>/dev/null; then
        echo -e "  ${CYAN}[frontend]${RESET} Arresto (PID $FRONTEND_PID)..."
        kill "$FRONTEND_PID" 2>/dev/null || true
        wait "$FRONTEND_PID" 2>/dev/null || true
    fi

    # Kill backend
    if [[ -n "$BACKEND_PID" ]] && kill -0 "$BACKEND_PID" 2>/dev/null; then
        echo -e "  ${BLUE}[backend]${RESET}  Arresto (PID $BACKEND_PID)..."
        kill "$BACKEND_PID" 2>/dev/null || true
        wait "$BACKEND_PID" 2>/dev/null || true
    fi

    # Stop database
    if $DB_STARTED; then
        echo -e "  ${GREEN}[database]${RESET} Arresto container..."
        docker compose down 2>/dev/null || true
    fi

    # Kill eventuali processi orfani sulla porta 8000 e 3000
    lsof -ti:8000 2>/dev/null | xargs kill -9 2>/dev/null || true
    lsof -ti:3000 2>/dev/null | xargs kill -9 2>/dev/null || true

    echo -e "${BOLD}${GREEN}Tutti i servizi ASIA sono stati arrestati.${RESET}"
    exit 0
}

trap cleanup SIGINT SIGTERM EXIT

# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------
echo -e "${BOLD}"
echo "  ╔═══════════════════════════════════════════╗"
echo "  ║   ASIA — Aggregated Scientific            ║"
echo "  ║          Intelligence for Animals          ║"
echo "  ╚═══════════════════════════════════════════╝"
echo -e "${RESET}"

# ---------------------------------------------------------------------------
# Verifica prerequisiti
# ---------------------------------------------------------------------------
echo -e "${DIM}Verifica prerequisiti...${RESET}"

if ! command -v docker &>/dev/null; then
    echo -e "${RED}Errore: Docker non trovato. Installa Docker Desktop.${RESET}"; exit 1
fi
if ! docker info &>/dev/null; then
    echo -e "${RED}Errore: Docker non è in esecuzione. Avvia Docker Desktop.${RESET}"; exit 1
fi
if ! command -v node &>/dev/null; then
    echo -e "${RED}Errore: Node.js non trovato. Installa Node.js 20+.${RESET}"; exit 1
fi
if ! command -v python3 &>/dev/null; then
    echo -e "${RED}Errore: Python3 non trovato.${RESET}"; exit 1
fi

# .env con GROQ_API_KEY
if [[ ! -f .env ]]; then
    if [[ -f .env.example ]]; then
        echo -e "${YELLOW}File .env non trovato. Creazione da .env.example...${RESET}"
        cp .env.example .env
    else
        echo -e "${YELLOW}File .env non trovato. Creazione...${RESET}"
        echo "GROQ_API_KEY=" > .env
    fi
    echo -e "${YELLOW}Configura GROQ_API_KEY in .env (gratis su https://console.groq.com)${RESET}"
fi

set -a
source .env 2>/dev/null || true
set +a

if [[ -z "${GROQ_API_KEY:-}" ]]; then
    echo -e "${YELLOW}Attenzione: GROQ_API_KEY non configurata in .env${RESET}"
    echo -e "${YELLOW}Le query RAG non funzioneranno. Ottienila su: https://console.groq.com${RESET}"
    echo ""
fi

echo -e "${GREEN}Prerequisiti OK${RESET}"
echo ""

# ---------------------------------------------------------------------------
# 1. Database (PostgreSQL + pgvector)
# ---------------------------------------------------------------------------
echo -e "${GREEN}[database]${RESET} Avvio PostgreSQL + pgvector..."
docker compose up db -d 2>&1 | while read -r line; do echo -e "  ${DIM}${line}${RESET}"; done
DB_STARTED=true

echo -e "${GREEN}[database]${RESET} Attesa connessione..."
for i in $(seq 1 30); do
    if docker compose exec -T db pg_isready -U asia &>/dev/null; then
        echo -e "${GREEN}[database]${RESET} ${BOLD}Pronto${RESET} (porta 5432)"
        break
    fi
    if [[ $i -eq 30 ]]; then
        echo -e "${RED}[database] Timeout: il database non risponde dopo 30 secondi${RESET}"
        exit 1
    fi
    sleep 1
done
echo ""

# ---------------------------------------------------------------------------
# 2. Backend (FastAPI)
# ---------------------------------------------------------------------------
echo -e "${BLUE}[backend]${RESET}  Installazione dipendenze Python..."
if [[ -f backend/pyproject.toml ]]; then
    (cd backend && pip install -e ".[dev]" --quiet 2>&1 | tail -1) || true
fi

echo -e "${BLUE}[backend]${RESET}  Avvio FastAPI (porta 8000)..."
export DATABASE_URL="postgresql+asyncpg://asia:asia@localhost:5432/asia"

cd backend
python3 -m uvicorn asia.main:app --host 0.0.0.0 --port 8000 --reload \
    > "$LOG_DIR/backend.log" 2>&1 &
BACKEND_PID=$!
cd "$SCRIPT_DIR"

echo -e "${BLUE}[backend]${RESET}  PID: $BACKEND_PID — Log: .logs/backend.log"

echo -e "${BLUE}[backend]${RESET}  Attesa avvio..."
for i in $(seq 1 60); do
    if curl -sf http://localhost:8000/api/health >/dev/null 2>&1; then
        echo -e "${BLUE}[backend]${RESET}  ${BOLD}Pronto${RESET} (porta 8000)"
        break
    fi
    # Controlla che il processo sia ancora vivo
    if ! kill -0 "$BACKEND_PID" 2>/dev/null; then
        echo -e "${RED}[backend] Il processo è terminato. Ultimi log:${RESET}"
        tail -20 "$LOG_DIR/backend.log" 2>/dev/null || true
        exit 1
    fi
    if [[ $i -eq 60 ]]; then
        echo -e "${RED}[backend] Timeout dopo 60 secondi. Ultimi log:${RESET}"
        tail -20 "$LOG_DIR/backend.log" 2>/dev/null || true
        exit 1
    fi
    sleep 1
done
echo ""

# ---------------------------------------------------------------------------
# 3. Frontend (Next.js)
# ---------------------------------------------------------------------------
echo -e "${CYAN}[frontend]${RESET} Installazione dipendenze Node..."
(cd frontend && npm install --silent 2>&1 | tail -1) || true

echo -e "${CYAN}[frontend]${RESET} Avvio Next.js (porta 3000)..."

cd frontend
NEXT_PUBLIC_API_URL=http://localhost:8000 npm run dev \
    > "$LOG_DIR/frontend.log" 2>&1 &
FRONTEND_PID=$!
cd "$SCRIPT_DIR"

echo -e "${CYAN}[frontend]${RESET} PID: $FRONTEND_PID — Log: .logs/frontend.log"

echo -e "${CYAN}[frontend]${RESET} Attesa avvio..."
for i in $(seq 1 30); do
    if curl -sf http://localhost:3000 >/dev/null 2>&1; then
        echo -e "${CYAN}[frontend]${RESET} ${BOLD}Pronto${RESET} (porta 3000)"
        break
    fi
    if [[ $i -eq 30 ]]; then
        echo -e "${YELLOW}[frontend] Potrebbe servire qualche secondo in più...${RESET}"
    fi
    sleep 1
done

# ---------------------------------------------------------------------------
# Tutto pronto
# ---------------------------------------------------------------------------
echo ""
echo -e "${BOLD}${GREEN}╔═══════════════════════════════════════════════╗${RESET}"
echo -e "${BOLD}${GREEN}║                                               ║${RESET}"
echo -e "${BOLD}${GREEN}║${RESET}   ${BOLD}ASIA è pronta!${RESET}                              ${BOLD}${GREEN}║${RESET}"
echo -e "${BOLD}${GREEN}║                                               ║${RESET}"
echo -e "${BOLD}${GREEN}║${RESET}   Frontend:  ${BOLD}http://localhost:3000${RESET}             ${BOLD}${GREEN}║${RESET}"
echo -e "${BOLD}${GREEN}║${RESET}   Backend:   ${BOLD}http://localhost:8000${RESET}             ${BOLD}${GREEN}║${RESET}"
echo -e "${BOLD}${GREEN}║${RESET}   API docs:  ${BOLD}http://localhost:8000/docs${RESET}        ${BOLD}${GREEN}║${RESET}"
echo -e "${BOLD}${GREEN}║                                               ║${RESET}"
echo -e "${BOLD}${GREEN}║${RESET}   Log backend:  ${DIM}.logs/backend.log${RESET}              ${BOLD}${GREEN}║${RESET}"
echo -e "${BOLD}${GREEN}║${RESET}   Log frontend: ${DIM}.logs/frontend.log${RESET}             ${BOLD}${GREEN}║${RESET}"
echo -e "${BOLD}${GREEN}║                                               ║${RESET}"
echo -e "${BOLD}${GREEN}║${RESET}   ${DIM}Premi Ctrl+C per arrestare tutto${RESET}             ${BOLD}${GREEN}║${RESET}"
echo -e "${BOLD}${GREEN}║                                               ║${RESET}"
echo -e "${BOLD}${GREEN}╚═══════════════════════════════════════════════╝${RESET}"
echo ""

# ---------------------------------------------------------------------------
# Tail dei log in tempo reale — il trap si occupa del cleanup
# ---------------------------------------------------------------------------
# -n 0 = solo nuove righe, ignora il contenuto già scritto durante lo startup
tail -n 0 -f "$LOG_DIR/backend.log" "$LOG_DIR/frontend.log" 2>/dev/null &
TAIL_PID=$!

# Attendi — Ctrl+C triggera il trap
wait "$BACKEND_PID" "$FRONTEND_PID" 2>/dev/null || true
kill "$TAIL_PID" 2>/dev/null || true
