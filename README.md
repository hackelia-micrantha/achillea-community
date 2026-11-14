# Achillea community

**Achillea** is being developed around a catalogue of outdoor games and a future download-to-play-offline experience. **Asterwild** is its first application. The backlog includes 13 named games, with Pentalpha as the only implemented reference in the private pre-release app. Game downloads and a public app release are **not available yet**. *Games to Play in Nature* by Jen Ball is one research source for the candidate list, not a source of redistributable content.

## What is available here

This **public** repository currently contains a project description, a static web page in [`web/`](web/), a draft architecture specification, and a proposed [public/private ownership and publication boundary](docs/public-private-boundary.md). The working Achillea SDK, Pentalpha game engine, and Asterwild application currently live together in a separate **private** development repository; they are **not published SDKs or supported public packages**.

The first private product milestone is a local, account-free Pentalpha experience. Hosted multiplayer, accounts, location features and AI-driven adaptation are future possibilities, not shipping capabilities of this public repository.

## Game catalogue and downloadable content

- [Browse the 13-game catalogue](web/index.html#game-catalogue): three solo, seven two-player and three group games. Only Pentalpha is implemented (pre-release); the other 12 entries are drafts or indexed concepts.
- [Read the planned download-and-offline flow](web/index.html#downloadable-games): select a supported game, acquire its compatible content and play without a network connection. This workflow is **not currently implemented** in Asterwild.
- [See the standalone Shape Hunt browser illustration](web/feature-demo.html): a public data-only example, **not** an Asterwild game download or installable game pack.

The working Pentalpha game remains bundled with the private application. Downloaded content must not become a route for unreviewed executable rules, privileges or third-party assets. The list is a development backlog, **not** a public download catalogue or release commitment.

## Architecture specification (draft)

A [language-neutral application state/effect contract](docs/specifications/application-state-effects-v0.1.md) and [synthetic conformance traces](docs/specifications/conformance/application-cycle-v0.1.json) are available for review. They deliberately distinguish current behavior from **unresolved** dispatch, lifecycle and failure semantics. No implementation has been certified against these fixtures and no public runtime or SDK has been released.

## Public contract validation

Run `python3 -m unittest discover -s tests -p 'test_*.py' -v` and `python3 scripts/validate_public.py` in a clean public checkout. The same read-only, credential-free checks run on GitHub-hosted PR and `main` jobs. They validate local README/docs/site links, JSON syntax, draft scenario IDs and expected trace shapes; **they do not certify an SDK, runtime behavior, release, or deployed website**. See [completed public-validation issue #6](https://github.com/hackelia-micrantha/achillea-community/issues/6) for the original credential-free CI, Cloudflare deployment, and live HTTP evidence. Subsequent site changes require their own deployment and HTTP verification before claiming a live release.

## Architecture and public feature illustration

- [Current architecture and proposed downloadable-feature diagrams](docs/architecture.md): distinguishes today's bundled Expo/React Native Pentalpha implementation from a **future** data-only feature-pack admission path.
- [Shape Hunt public example](web/feature-demo.html) and [sample JSON](web/examples/shape-hunt.v1.json): a synthetic, standalone browser illustration. The page fetches JSON on demand and renders it using already-installed browser code; it is **not** an Achillea SDK, app extension, or signed/offline production loader.
- [Example contract and trust boundaries](docs/examples/downloadable-feature.md): documents capability constraints, source separation, and missing production controls.
- [Earlier Expo hackathon prototype](https://github.com/ryjen/cactus-hackathon): design reference for mobile prototyping, not evidence of shared source or a completed Achillea downloadable-feature implementation.

Downloaded executable code, a production feature catalog, signature verification, offline pack installation, and host/runtime version negotiation **are not currently shipped**. The working game SDK, concrete game engine, and Asterwild source remain private pending review and release gates.

## Platform direction

The proposed public surface is intentionally bounded:

- reviewed language-neutral application and game-definition specifications;
- independently runnable conformance fixtures and reference examples;
- reusable SDK and game-engine code **only after** rights, API, security, build and license review;
- community docs and the project web presence.

Product-specific application code, operations, unreleased assets and private data remain in the private product/development repository. A private package does not become publicly supported merely because its source code is reusable.

See [the proposed repository boundary](docs/public-private-boundary.md) for the intended ownership, dependency direction, promotion checklist and incremental migration order. The document is a proposal until accepted.

## Documentation maintenance

The public documentation and static site follow the [shared Micrantha documentation-sync process](docs/documentation-maintenance.md), with project-specific claim, release, and private/public source boundaries. Public source validation is separate from Cloudflare deployment and live-site verification.

## Contributing and use

Contributions to this repository can improve the public website and documentation through a pull request. Do not submit private repository content, production configuration, credentials, personally identifying or sensitive location data, copyrighted source-book excerpts, or third-party assets without confirmed redistribution rights.

**License:** not yet selected. This public repository does not currently grant an open-source license for reuse of its code or media. A clear license and contributor policy are prerequisites to publishing reusable packages.

**Project status:** early development and public documentation. No public package release, supported installation command, published service API or app download is represented here.
