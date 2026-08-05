---
name: add-just-doctor
description: Add and run a repository-level just doctor command that validates the local environment file and its configured service dependencies.
---

# Add Just Doctor

Create a repository-native `just doctor` command, execute it against the current local environment, and leave the command covered by focused tests. Treat the dependency inventory as the single source of truth.

## 1. Read The Repository Contract

Read the applicable agent instructions and setup docs, resolving repository file references from the repository root. Check `./Justfile` and then `./justfile`; inspect configuration modules, environment examples such as `./.env.example`, and test conventions. When a filename varies by repository, start the search at the repository root and record the discovered path in `./relative/path` form. Find the canonical local environment file and the repository's existing dotenv loader. In linked worktrees, follow the repository's documented rule for locating the primary worktree environment.

Completion criterion: identify the exact recipe file, runtime/config entrypoint, canonical local environment file, test layer, and validation commands before editing.

## 2. Build The Dependency Inventory

Trace environment lookups from runtime code, configuration schemas, `./.env.example`-style contracts, Compose/Helm manifests, and existing provider clients. For every runtime dependency controlled by environment configuration, record:

- service name and ownership: first-party, third-party, or infrastructure;
- endpoint or connection-string variables and runtime defaults;
- credential variable names and authentication placement;
- enablement flags and the value that activates the integration;
- protocol and the cheapest side-effect-free health probe;
- whether configuration is required, optional, or disabled by default.

Keep ordinary application settings outside the service inventory. Reproduce runtime fallback behavior instead of inventing doctor-only endpoints or defaults.

Completion criterion: every enabled environment-backed service reachable from production configuration is represented, and every inventory entry maps back to runtime code or a documented configuration contract.

## 3. Define Environment Health

Make the command check the canonical local environment file before probing services.

- `PASS`: configuration is present and the protocol-level health check succeeds.
- `WARN`: the service responds, but a side-effect-free probe cannot prove business availability; include the bounded reason.
- `FAIL`: the environment file is absent, required or enabled configuration is missing/invalid, DNS/TCP/TLS/protocol connection fails, expected authentication is rejected, or the service reports an unhealthy/server-error state.
- `SKIP`: an optional integration is explicitly disabled or not configured.

Exit `0` when no row is `FAIL`; exit nonzero when configuration or an enabled dependency fails. Keep timeouts short, concurrency bounded, and result ordering deterministic.

Completion criterion: status and exit-code behavior are explicit for missing environment, incomplete configuration, disabled integrations, reachable services, and unhealthy services.

## 4. Add The SOPS Recovery Hint

Print a concrete SOPS sync hint when the local environment file is absent or objectively behind the current configuration contract. Valid lag signals include missing required keys, missing keys for enabled integrations, a documented config revision/hash mismatch, or newer encrypted-source metadata discoverable without exposing secret values. Treat file modification time alone as a possible-lag warning rather than proof.

Resolve the SOPS repository name or path from repository docs, scripts, Git remotes, or sibling workspace conventions when available. Otherwise print a generic action: check the SOPS repository that owns this project's environment, then sync the latest approved local environment file. Keep synchronization a separate user-authorized action.

Completion criterion: missing and objectively stale fixtures both emit the SOPS action, while a current environment and ordinary provider outage do not claim the file is stale.

## 5. Implement The Native Command

Use the repository's existing language, dependency manager, configuration loader, logging/output library, and module boundaries. Add a small typed inventory plus protocol probes rather than embedding shell checks in the recipe. The recipe should be a stable entrypoint:

```just
doctor:
    <repository-native command>
```

Load secret values through the existing configuration mechanism and keep them in memory. Render only service name, ownership, status, environment variable names when useful, sanitized `host:port`, and a bounded reason class/status code. Strip URL userinfo, paths, query strings, headers, response bodies, credential values, and exception messages from output.

Prefer a documented `/health`, readiness, ping, or metadata endpoint. Otherwise use a side-effect-free HTTP request and classify an inconclusive application status as `WARN`. Use protocol-native checks for databases, queues, gRPC, caches, and similar infrastructure. Never perform billable search/generation, mutate remote state, or send business data as a health probe.

Completion criterion: `just doctor` performs bounded checks for the full inventory and its stdout/stderr remain secret-free under success and failure.

## 6. Cover The Contract

Add focused tests in the nearest repository test layer for:

- environment file present and absent;
- required, optional, disabled, and malformed configuration;
- at least one protocol success and failure;
- authentication placement without credential disclosure;
- endpoint and exception redaction;
- deterministic summary and exit code;
- SOPS hint on missing/stale configuration and no false stale claim on provider outage;
- the `just doctor` recipe contract.

Update the repository's setup or command documentation with the status meanings and exit behavior.

Completion criterion: focused tests, formatting, lint, and type checks pass using repository-native commands.

## 7. Execute The Doctor

Run `just doctor` from the repository root using the current local environment. A nonzero exit caused by accurately identified unavailable services is a valid doctor result, not a passing environment. Inspect the rendered table and confirm it contains no secrets or credential-bearing URLs.

Report the exact `PASS/WARN/FAIL/SKIP` counts, failed service names with sanitized reasons, whether the local environment file was found/current, and whether the SOPS hint appeared. Separate command correctness from environment health.

Completion criterion: the command has been observed on the real local configuration, automated validations are green, and the handoff states both implementation status and current environment status.
