#!/bin/sh
# This sets up the (local) git hook which updates the bibliography!
# Please run this file from the root directory from the repo.
echo "Creating a pre-commit hook..."
cp githooks/pre-commit .git/hooks/pre-commit
echo "Done!"
