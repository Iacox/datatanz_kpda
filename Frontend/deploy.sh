#!/usr/bin/env sh

# остановить публикацию при ошибках
set -e

# сборка
# cd C:/Users/Mi/Desktop/Projects/datatanz_kpda/Frontend
npm run build

# коммит сборки
# ВАЖНО! путь /dist должен быть удален из .gitignore
git add dist
git commit -m 'Initial deploy commit'
cd ../
git subtree push --prefix Frontend/dist origin gh-pages