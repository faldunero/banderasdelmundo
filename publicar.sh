#!/bin/bash
# Publica el proyecto "Banderas del Mundo" en GitHub.
# Uso: desde Terminal en tu Mac, ejecuta:
#     cd "/Users/felipealdunate/Documents/Claude/Projects/Banderas del mundo"
#     bash publicar.sh

set -e

REPO_URL="https://github.com/faldunero/banderasdelmundo.git"
COMMIT_MSG="Inicial: explorador + 42 cartas + script de generación"

cd "$(dirname "$0")"

if [ ! -d .git ]; then
    echo "→ Inicializando repositorio git…"
    git init -b main
    git config user.email "faldunate@gmail.com"
    git config user.name "Felipe Aldunate"
fi

echo "→ Agregando archivos…"
git add -A

if git diff --cached --quiet; then
    echo "   (sin cambios que commitear)"
else
    echo "→ Creando commit…"
    git commit -m "$COMMIT_MSG"
fi

if ! git remote | grep -q '^origin$'; then
    echo "→ Agregando remote origin…"
    git remote add origin "$REPO_URL"
else
    echo "→ Remote origin ya existe"
    git remote set-url origin "$REPO_URL"
fi

echo "→ Push a GitHub (se te pedirán credenciales si no las tienes configuradas)…"
git push -u origin main

echo ""
echo "✓ Listo. Ya está publicado en: $REPO_URL"
