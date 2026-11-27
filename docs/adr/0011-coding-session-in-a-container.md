---
status: accepted
---

# Coding sessions run in a container with a token scoped to this repository

ADR 0010 isolates the Holdout Scenarios with permission rules, which a shell command that never names the holdout folder can get around. The coding session also runs with the owner's own GitHub login, so it could clone the private holdout repository. We replace "permissions and discipline" with a barrier on both paths.

## Decision

- **Disk:** the coding session (Claude Code that implements tickets) runs inside a dev container that mounts only this repository. The holdout clone is never mounted, so it does not exist for that session.
- **GitHub:** inside the container, `gh` and `git` use a fine-grained personal access token that grants access to `ricmotta/nyc-residential-registry` only. The owner creates it and passes it in; it never lives in the repository. Without it, a disk barrier could be bypassed with a clone.
- **No Docker socket in the container.** Mounting the host's Docker socket would let the session start a container that mounts any host folder, holdout included. The local environment (`docker compose`) keeps running on the host. The container reaches its ports through the host name `host.docker.internal` (to confirm on Docker Desktop for Windows), and CI checks need no Docker at all.
- **Evaluator and scenario author stay on the host**, in sessions opened in the holdout repository, with the owner's normal login.
- The `.claude/settings.json` deny rules from ADR 0010 stay as a second layer.

## Considered options

- A separate Windows user with NTFS permissions on the holdout folder: also a real barrier, but switching users is awkward day to day.
- Cloud coding sessions: a strong barrier, but they lose access to the local environment.
- Encrypting the scenarios (`age` or `git-crypt`): it protects content even when it is read, but adds key management. We can revisit it if scenarios ever need to live closer to the code.

## Consequences

- Inside the container, the coding session can use the Claude Code sandbox, which per its docs runs on Linux but not on native Windows (to confirm inside the container).
- The owner keeps two contexts: the container for coding, the host for the holdout repository and the evaluator.
- The token expires and has to be renewed; a coding session that cannot reach GitHub must report that rather than fall back to the owner's login.
