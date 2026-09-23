# Achillea community

**Achillea** is a platform under development for guided outdoor play, reusable game definitions, and portable application architecture. **Asterwild** is the first product built using Achillea.

## What is available here

This **public** repository currently contains a project description, a static web page in [`web/`](web/), and a proposed [public/private ownership and publication boundary](docs/public-private-boundary.md). The working Achillea SDK, Pentalpha game engine, and Asterwild application currently live together in a separate **private** development repository; they are **not published SDKs or supported public packages**.

The first private product milestone is a local, account-free Pentalpha experience. Hosted multiplayer, accounts, location features and AI-driven adaptation are future possibilities, not shipping capabilities of this public repository.

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
