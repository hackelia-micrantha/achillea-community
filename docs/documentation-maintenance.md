# Public documentation maintenance

**Adoption:** The [Micrantha documentation-sync skill](https://github.com/hackelia-micrantha/.github/blob/main/skills/documentation-sync/SKILL.md) applies unchanged. This project-local contract adds only Achillea-specific authority, evidence, validation, and publication boundaries.

## Ownership and publication boundary

- This **public** repository owns its project description, [static site](../web/index.html), draft [application state/effect contract](specifications/application-state-effects-v0.1.md), [synthetic conformance traces](specifications/conformance/application-cycle-v0.1.json), and [public/private boundary description](public-private-boundary.md).
- The separate **private** Achillea/Asterwild development repository remains authoritative for unreleased SDK, game-engine, product source and assets, product integrations, and actual runtime qualification. No public checkout, package, SDK, app download, or privately supported implementation can be inferred from the documents here.
- The **current split** (public community surface, private implementation/product) is real. The boundary document's **future package-promotion and licensing plan remains a proposal** until its own rights, source/history exposure, build, security, release/provenance, downstream-consumer, and approval gates are met. Do not reclassify an unreleased private package as a published public contract or copy private source/history to settle documentation drift.
- The public repository has **no selected open-source license grant**. Reusable code/media, product assets, game/source-book text, and private or sensitive location/player data must not be promoted merely to complete documentation.

## Claim reconciliation

Review the [README](../README.md), [site source](../web/index.html), [boundary](public-private-boundary.md), [draft specification](specifications/application-state-effects-v0.1.md), and [conformance fixture](specifications/conformance/application-cycle-v0.1.json) together when describing platform maturity or support.

- Achillea is under development; Asterwild is its first in-development product. Account-free/local-first Pentalpha is a development target, **not** a public app/SDK release.
- The draft `0.1` specification contains **candidate** state/effect rules. Dispatch reentrancy, publication/equality timing, effect failures, cancellation, teardown and cross-language TypeScript/Kotlin equivalence remain unqualified or unresolved. No implementation has been certified against the synthetic fixture.
- Distinguish **proposed architecture**, **public draft/fixture**, **privately implemented behavior**, **independently validated behavior**, and **supported, published artifact**. Site source and link correctness do not establish production deployment or a feature release.
- Multiplay, hosted accounts, location-aware behavior, AI adaptation and a reusable publicly installable engine are future directions unless separate released evidence qualifies them. Avoid unverified security/privacy promises.

## Validation at the exact candidate revision

The repository now runs unprivileged, credential-free public validation on pull requests and `main` ([community #6](https://github.com/hackelia-micrantha/achillea-community/issues/6), delivered 2026-10-28). From a clean public checkout, run:

```sh
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 scripts/validate_public.py
```

The checks cover public documentation/site links, JSON syntax and fixture structure, duplicate scenario IDs and malformed expected traces, and the standalone data-only example's source contract. They **do not** prove actual SDK/game runtime conformance, an Asterwild app release, a signed feature-pack admission system, or a production installation.

The public Cloudflare site and example have separate build/live HTTP evidence recorded in community #6. Site-source tests alone cannot substitute for deployment and HTTP evidence after a site change. Keep source-only PR checks read-only and unprivileged; never provide fork code with private runner access, private source, or credentials. Publication or public-license claims require their own explicit gate.

## Maintenance triggers and decisions

Reconcile these documents after public specification/fixture changes, private product release milestones, rights/licensing or publication decisions, site deployment changes, platform/runtime parity evidence, and new security/privacy claims. Prefer the owning public-validation issue over duplicate CI plans.

Use the shared `DOC-Q*` queue for material unresolved license, release-support, publication or normative-behavior decisions. This adoption authorizes no repository visibility change, private-source promotion, release, site deployment, or infrastructure mutation.
