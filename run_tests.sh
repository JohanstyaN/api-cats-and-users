set -euo pipefail

# ------------------------------------------------
# run_tests.sh — Construye, levanta, espera al API,
# ejecuta pytest dentro del contenedor y limpia todo
# ------------------------------------------------

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🔨 Construyendo y arrancando contenedores..."
docker-compose up -d --build

echo -n "⏳ Esperando a que la API esté disponible"
until curl -s http://localhost:8001/breeds >/dev/null 2>&1; do
  printf "."
  sleep 1
done
echo " ✅"

echo "🧪 Ejecutando pruebas con pytest dentro del contenedor cats_users_api..."
docker exec cats_users_api pytest -q --disable-warnings --maxfail=1

TEST_EXIT_CODE=$?

echo "🧹 Deteniendo y limpiando contenedores..."
docker-compose down -v

exit $TEST_EXIT_CODE
