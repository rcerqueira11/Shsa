 #!/usr/bin/env bash

Comentario="$1"

echo "Git status"
git status

echo "Git add all"
git add --all

echo "Git commit"
git commit -m "$Comentario"

echo "PUSH!"
git push
