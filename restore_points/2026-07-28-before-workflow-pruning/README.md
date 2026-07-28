# Restore point before workflow pruning

Created before removing obsolete automatic GitHub Actions workflows.

Kept:
- `.github/workflows/deploy-pages.yml` because it deploys the live GitHub Pages build.

Removed after this restore point:
- `.github/workflows/test.yml` because it validates the legacy Python physics/Parquet stack rather than the current V9 JavaScript computation engine.
- `.github/workflows/topology-parquet.yml` because it builds the legacy Python Parquet topology store and is not part of the current V9 build.

The removed workflow contents remain recoverable from Git history and from the parent commit immediately before pruning.
