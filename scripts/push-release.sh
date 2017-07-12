
git submodule foreach 'git push origin $(git describe) wmf/stable || true'
git push origin $(git describe) wmf/stable
