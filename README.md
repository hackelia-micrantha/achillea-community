# Achillea community

**Achillea** is a platform under development for guided outdoor play, reusable game definitions, and portable application architecture. **Asterwild** is the first product built using Achillea.

## What is available here

This **public** repository currently contains a project description, a static web page in [`web/`](web/), a draft architecture specification, and a proposed [public/private ownership and publication boundary](docs/public-private-boundary.md). The working Achillea SDK, Pentalpha game engine, and Asterwild application currently live together in a separate **private** development repository; they are **not published SDKs or supported public packages**.

The first private product milestone is a local, account-free Pentalpha experience. Hosted multiplayer, accounts, location features and AI-driven adaptation are future possibilities, not shipping capabilities of this public repository.

## Architecture specification (draft)

A [language-neutral application state/effect contract](docs/specifications/application-state-effects-v0.1.md) and [synthetic conformance traces](docs/specifications/conformance/application-cycle-v0.1.json) are available for review. They deliberately distinguish current behavior from **unresolved** dispatch, lifecycle and failure semantics. No implementation has been certified against these fixtures and no public runtime or SDK has been released.

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

## Contributing and use

Contributions to this repository can improve the public website and documentation through a pull request. Do not submit private repository content, production configuration, credentials, personally identifying or sensitive location data, copyrighted source-book excerpts, or third-party assets without confirmed redistribution rights.

**License:** not yet selected. This public repository does not currently grant an open-source license for reuse of its code or media. A clear license and contributor policy are prerequisites to publishing reusable packages.

**Project status:** early development and public documentation. No public package release, supported installation command, published service API or app download is represented here.
