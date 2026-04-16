#!/usr/bin/env bash
set -euo pipefail

BASE_BRANCH="${1:-main}"

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Este script debe ejecutarse dentro de un repositorio git."
  exit 1
fi

if ! git remote get-url origin >/dev/null 2>&1; then
  echo "No existe remoto 'origin'. Configúralo primero:"
  echo "git remote add origin <URL_DEL_REPO>"
  exit 1
fi

CURRENT_BRANCH="$(git rev-parse --abbrev-ref HEAD)"

echo "Configurando git para actualizaciones más limpias..."
git config pull.rebase true
git config rebase.autoStash true
git config fetch.prune true

echo "Sincronizando con origin/${BASE_BRANCH}..."
git fetch origin

echo "Rebase de ${CURRENT_BRANCH} sobre origin/${BASE_BRANCH}..."
if git rebase "origin/${BASE_BRANCH}"; then
  echo "✅ Rama actualizada sin conflictos."
else
  echo "⚠️ Hay conflictos. Resuélvelos y luego ejecuta:"
  echo "git add ."
  echo "git rebase --continue"
  exit 2
fi

echo "Listo. Si tu rama ya existe en remoto, publica cambios con:"
echo "git push --force-with-lease"
