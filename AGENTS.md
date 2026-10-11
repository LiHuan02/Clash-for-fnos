# fnOS packaging repository

- Shared Vue / Go / translations and Docker are maintained in ../Clash-Manager, not copied into this repository.
- Pin shared source with upstream.lock (full commit SHA + VERSION); never silently build a branch head or dirty source.
- Preserve fnOS appname, paths, lifecycle, data compatibility and icon configuration.
- fpk/manifest is the FPK version source. Compile it into the isolated shared build and package its matching CHANGELOG.
- For a new user-requested FPK build, increment the manifest patch version automatically unless the user specifies a version; do not ask for a separate reminder or confirmation.
- Run ./scripts/check.sh; build x86 / arm / all serially and run scripts/audit-fpk.py for packaging changes.
- Keep final artifacts in dist/. Archive proof does not prove real-device installation or TUN behavior.
- GitHub Releases must upload only the three FPKs (x86_64, arm64, all). Keep SHA-256 files and build audit reports locally in dist/; do not upload them as release assets or describe them as downloadable attachments.
- A user request to package authorizes the necessary local commits of task changes in either repository, updating upstream.lock, and building the FPKs; do not request separate authorization for these steps. Preserve unrelated changes.
- Git push, FPK publication and Docker publication still require an explicit user request.

## Version management before packaging

- Before a new FPK containing changed shared application code, increment Clash-Manager/VERSION (patch by default; honor an explicit version), update its CHANGELOG.md, run its scripts/sync-version.sh and commit the shared changes with matching version metadata. New functionality must not keep the previous packaged source's version label.
- After shared-source checks, update upstream.lock to that committed source's full SHA and exact VERSION. The lock's version and commit must be updated together and validated against each other; never change only the version label.
- Keep fpk/manifest as the installed application's version source, follow the existing FPK version increment rule and prepare its matching CHANGELOG.md before building. Inject the FPK version only into the isolated shared export.
- Packaging-only fnOS changes may reuse an unchanged shared commit and version while incrementing the FPK version independently.
- Before delivery, verify the shared VERSION, pinned SHA, FPK manifest version, matching changelog and package audit's source/version records. Report the shared source version/commit and FPK version clearly.
- Preserve the existing authorization boundaries for commits, Git pushes and artifact publication; a version update does not authorize publishing or replacing an existing release.
