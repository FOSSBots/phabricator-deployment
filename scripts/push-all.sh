git submodule foreach 'git push --tags origin $(git name-rev --name-only HEAD) || true'
