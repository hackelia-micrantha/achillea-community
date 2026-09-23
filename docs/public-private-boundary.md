# Public platform / private product boundary

Status: proposed; review before treating this as an adopted release or licensing policy.

## Current reality

- `achillea-community` is public and currently hosts the project description and a web surface.
- The working Achillea SDK, game packages, and the Asterwild application currently live together in a separate **private** development repository.
- No public SDK artifact, external-consumer contract, license grant, or supported package release is implied by the package names or versions in private development.
- Asterwild is the first product using Achillea. Public documentation may describe its purpose and supported product behavior without publishing product code or operating details.

## Intended ownership

| Public Achillea, once reviewed and published | Private Asterwild / development |
| --- | --- |
| Language-neutral architecture and game-definition specifications | Application wiring, product navigation, branding, and unreleased UX |
| Portable game-engine and SDK contracts, implementations, and conformance fixtures | Product-specific adapters, configuration, analytics, and admin workflows |
| Explicitly cleared reference games, examples, and content with verified rights | Proprietary or unreviewed game content, source extracts, and creative assets |
| Public contribution, compatibility, security, and release documentation | Production infrastructure, deployment inventory, operational runbooks, and sensitive telemetry |

A generic package is **not automatically approved for publication** simply because it lives under `packages/`. Asterwild-specific behavior must not become a dependency of the public SDK or game engine. Public examples must be independently buildable without private source or credentials.

## Dependency and source-of-truth contract

1. Product code may depend on versioned public Achillea releases; public Achillea must not depend on private product code or services.
2. Until extraction is complete, the private monorepo remains the source of truth for its existing packages. Do not create two independently edited copies or a recurring private-to-public mirror.
3. An approved public extraction becomes canonical in the **public repository** only after its public build, tests, licensing, security review, and consumer migration pass. Subsequent changes go through the public repository.
4. The first useful public artifact can be a self-contained specification and conformance cases; there is no need to publish or rename every package at once.
5. Internal `0.1.0` package metadata is not proof of a distributable public release. Agree on versioning, packaging and support scope before publishing artifacts.

## Private-to-public promotion gate

Every proposed extraction needs a bounded review covering:

- **Rights:** copyright, provenance of any adapted games/text/media, dependencies, and an explicit license decision. Do not assume a source book, artwork, or third-party game adaptation is freely redistributable.
- **Information exposure:** code, history, tests, fixtures, generated artifacts, comments and documentation for secrets, internal endpoints, identifying location or player data, telemetry, operational topology, and unreleased product decisions. Removing a secret in the latest commit does not sanitize published history.
- **Architecture:** public code imports no private module, product implementation, or privileged service. Example data is synthetic and safe.
- **Build/supply chain:** build and tests succeed from a clean public checkout. Untrusted fork PRs never receive credentials or privileged/self-hosted runner access.
- **Consumer:** after release, the private product consumes an immutable version or commit/tag with recorded provenance, compatibility tests, and a rollback path.

If any check fails, the extraction remains private until the issue is resolved. Do not run an automatic bulk export from the private repository.

## Sequence and scope

1. Agree on this ownership and promotion contract; correct the public README to describe what actually exists.
2. Publish a reviewed, language-neutral specification and conformance example, separate from Asterwild wiring.
3. After the local/account-free v0.1 Pentalpha product slice is demonstrated, evaluate a single generic package for public extraction.
4. Release and consume that package through a pinned, reproducible dependency; enforce import and dependency boundaries in both CI systems.
5. Consider repository naming only after the split works in practice. No automatic rename or public migration of the private repository is authorized by this document.

This policy must not block the v0.1 playable-product critical path. Until a public release is proven, describe Achillea as a platform under development, not as an available public SDK.
