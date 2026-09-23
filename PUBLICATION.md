# Publication boundary

This standalone package contains reusable guidance, fictional fixtures and local tooling. It contains no application source, operational inventory, private project audit, personal installation report or inherited repository history.

release-files.json is the reviewed publication inventory. scripts/check-release.py rejects extra or missing files, links outside the package, unapproved external URL hosts and recognizable credential/personal-path patterns. Changes to the inventory and URL hosts require human review. Passing this check is not proof that all confidential prose or every possible secret has been detected.

Before each publication, review the actual content and Git history, run the package and release checks, and inspect Git author/committer metadata. Archive only the reviewed inventory; do not copy a source repository's Git directory, local locators, environment files, caches or external application evidence. Deleting a sensitive file from the current tree does not remove it from older history.

No license has been selected. Remote repository creation and publication are separate from preparing this local package; confirm the destination, visible author identity and intended audience before publishing.
