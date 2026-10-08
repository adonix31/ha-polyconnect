# Automatic app-version recovery (proposed follow-up)

The v9 outage has two independent causes: the login payload requires av=9.0, and the app URL is supplied by the authentication server. PR #6 fixes these immediately.

## Design

1. Persist the last successfully validated application version in the add-on's /data directory, defaulting to 9.0.
2. On application load, detect the dedicated update-required HTML page before attempting Blazor discovery.
3. Fetch /config.js **only** from the authenticated application origin, requiring HTTPS and the expected pool.mytech-connect.io host family. Parse only the version string under APP_CONFIG.minVersion.
4. Compare dotted numeric versions; never downgrade or accept arbitrary JavaScript content as code.
5. If newer, record the version, call the existing auth manager to obtain a fresh login session, and restart the browser navigation using the **new server-provided URL**.
6. Limit to one upgrade/retry per browser startup. Surface a clear error if authentication or page navigation still fails.
7. Do not clear terminal registration or saved heat-pump IDs.
8. Avoid a shared mutable BASE across unrelated sessions; make the application origin instance-scoped before merging.

## Tests to add

- v9 happy path uses persisted 9.0, requires no retry.
- Legacy app route displays update page with minVersion 9.0 and triggers one reauthentication.
- Already-current version displayed on update page fails clearly with no loop.
- Missing/invalid config.js fails clearly.
- Untrusted host is never queried for version information.
- Version greater than 9.0 upgrades once; lower/equal version does not.
- Updated login returns a different origin; all subsequent SPA navigation follows that origin.
- Existing session and terminal IDs are not destroyed on failed version check.

This design is intentionally separate from the minimal outage fix and is not implemented by this document.
