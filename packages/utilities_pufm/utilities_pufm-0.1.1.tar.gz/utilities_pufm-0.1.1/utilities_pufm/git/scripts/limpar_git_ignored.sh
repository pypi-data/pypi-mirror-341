#!/bin/bash

REPO_DIR=$1
COMMIT_MSG=$2

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Carrega variáveis do .env
if [ -f "$SCRIPT_DIR/.env" ]; then
    export $(grep -v '^#' "$SCRIPT_DIR/.env" | xargs)
else
    echo "❌ Arquivo .env não encontrado em $SCRIPT_DIR"
    exit 1
fi

if [ -z "$REPO_DIR" ] || [ -z "$COMMIT_MSG" ]; then
    echo "❌ Uso: $0 /caminho/para/repositorio \"mensagem do commit\""
    exit 1
fi

cd "$REPO_DIR" || { echo "❌ Diretório não encontrado: $REPO_DIR"; exit 1; }

if [ ! -d ".git" ]; then
    echo "❌ Este diretório não é um repositório Git."
    exit 1
fi

# Verifica identidade
if ! git config user.name > /dev/null || ! git config user.email > /dev/null; then
    echo "⚠️  Configurando identidade do Git localmente..."
    git config user.name "$NAME"
    git config user.email "$EMAIL"
fi

echo "🔍 Listando arquivos ignorados que estão versionados..."
ignored_files=$(git ls-files --cached --exclude-standard -i -o)

if [ -z "$ignored_files" ]; then
    echo "✅ Nenhum arquivo ignorado foi encontrado no versionamento."
else
    echo "🗑️  Removendo do versionamento os arquivos ignorados:"
    while IFS= read -r file; do
        echo "   → $file"
        git rm --cached "$file" 2>/dev/null
    done <<< "$ignored_files"

    git commit -m "Remove arquivos ignorados do versionamento - $COMMIT_MSG"
    echo "✅ Commit feito com a mensagem:"
    echo "   \"Remove arquivos ignorados do versionamento - $COMMIT_MSG\""
fi

echo "🧹 Limpando histórico com git filter-repo..."
git filter-repo $(echo "$ignored_files" | sed 's/^/--path /') --invert-paths || {
    echo "❌ Falha ao executar git filter-repo. Você tem ele instalado?"
    exit 1
}

echo "🧽 Limpando objetos antigos..."
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Push forçado com token
REMOTE_URL=$(git remote get-url origin)
REMOTE_WITH_TOKEN=$(echo "$REMOTE_URL" | sed "s#https://#https://${GITHUB_USER}:${GITHUB_TOKEN}@#")

echo "🚀 Enviando para o repositório remoto com token (push --force)..."
git push "$REMOTE_WITH_TOKEN" HEAD:$(git rev-parse --abbrev-ref HEAD) --force

echo "✅ Processo concluído com sucesso!"
