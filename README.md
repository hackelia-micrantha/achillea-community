# Achillea

<div align="center">

[![Status](https://img.shields.io/badge/status-active-2ea44f?style=for-the-badge)](#)
[![Platform](https://img.shields.io/badge/platform-mobile%20%7C%20backend%20%7C%20web-0969da?style=for-the-badge)](#)
[![Architecture](https://img.shields.io/badge/architecture-modular-8250df?style=for-the-badge)](#)
[![License](https://img.shields.io/badge/license-TBD-orange?style=for-the-badge)](#license)
[![AI Assisted](https://img.shields.io/badge/AI-assisted-8b5cf6?style=for-the-badge)](#ai-assisted-features)

**Achillea** is the platform and SDK for building playful, guided outdoor experiences.  
**Asterwild** is the first product built on top of it.

</div>

---

## Overview

Achillea provides the foundation for outdoor, game-like experiences that blend:

- guided play
- lightweight multiplayer interactions
- tutorials and onboarding for unfamiliar games
- location/context-aware experiences
- reusable game and content primitives

The platform is designed to support products like **Asterwild**, where users can discover, learn, and play outdoor games with minimal setup and clear guidance.

## Why this exists

Many outdoor games are simple once understood, but difficult to start well:

- players may not know the rules
- setup can be awkward
- turn order and scoring may be unclear
- multiplayer coordination is often more annoying than the game itself

Achillea exists to reduce that friction.

It aims to make outdoor games more approachable through structured onboarding, game-state support, and a platform model that can scale from single-player tutorials to live multiplayer sessions.

## Core ideas

- **Platform first**: Achillea is the reusable foundation.
- **Product on top**: Asterwild is the first concrete user-facing application.
- **Tutorial-driven UX**: wizard flows and guided play are first-class, not an afterthought.
- **Simple multiplayer**: optimized for cheap, maintainable turn-based interaction rather than heavyweight realtime systems.
- **Composable game model**: shared primitives for rules, turns, actions, scoring, and progression.
- **AI-assisted surfaces**: selective use of AI for content generation, adaptation, and player assistance.

## Architecture direction

The exact implementation may evolve, but the project is being shaped around a few pragmatic principles:

- keep the hosting model simple and inexpensive
- favor long-term maintainability over novelty
- use infrastructure that is understandable by one small team
- support both synchronous and async turn-based play
- allow multiple apps/services to coexist cleanly

Potential building blocks include:

- shared backend services for identity, game state, and notifications
- mobile-first client applications
- optional web/admin surfaces
- a compact multiplayer service for lobby/session management
- modular storage boundaries for app-specific and shared data

## Features

### Current / planned

- onboarding flows for learning outdoor games
- game tutorials and rules walkthroughs
- turn-based multiplayer sessions
- lobby creation and invitations
- notifications for player turns and session changes
- reusable game definitions and content packs
- player profiles and lightweight progression
- admin/content tooling

### AI-assisted features

- tutorial adaptation based on player familiarity
- rule explanation and clarification
- content generation support for game prompts or activities
- future experimentation with AI-assisted UI/content specs

## Repository goals

This repository is intended to be the home for:

- platform architecture
- shared libraries / SDKs
- backend and multiplayer services
- client applications
- documentation, RFCs, and design decisions

## Proposed repository structure

```text
.
├── apps/
│   ├── asterwild/          # product application
│   ├── admin/              # admin or content tools
│   └── web/                # optional web surfaces
├── packages/
│   ├── sdk/                # shared Achillea SDK
│   ├── game-model/         # turns, rules, actions, scoring
│   ├── ui/                 # shared UI components
│   └── content/            # content schemas and assets
├── services/
│   ├── api/                # primary backend API
│   ├── multiplayer/        # lobby/session orchestration
│   └── notifications/      # push/email/background events
├── docs/
│   ├── architecture/
│   ├── product/
│   ├── gameplay/
│   └── decisions/
├── infra/
│   ├── local/
│   ├── deploy/
│   └── ops/
└── README.md
```

## Design principles

- **Clarity over cleverness**
- **Small-team operability**
- **Strong boundaries between platform and product**
- **Cheap to run, cheap to change**
- **Incremental evolution over premature complexity**
- **Documentation as part of the system**

## Multiplayer approach

This project is intentionally oriented toward **turn-based multiplayer**, which changes the architecture tradeoffs:

- low-latency realtime sync is less important than correctness and reliability
- lobbies, invitations, session state, and notifications matter more than twitch performance
- durable game state and simple operational behavior usually beat complex realtime stacks

That makes this a good fit for simpler backend models, especially early on.

## Getting started

> Replace this section with actual commands once the repository layout is finalized.

### Prerequisites

- Git
- Node.js / pnpm or npm
- mobile toolchain as needed
- backend runtime as needed

### Clone

```bash
git clone https://github.com/your-org/achillea.git
cd achillea
```

### Install

```bash
# example only
pnpm install
```

### Run

```bash
# example only
pnpm dev
```

## Development workflow

Recommended expectations for contributors:

1. read the relevant docs and architecture notes
2. keep changes modular and reviewable
3. document meaningful design decisions
4. prefer pragmatic implementations over speculative abstractions
5. keep product concerns separated from reusable platform concerns

## Documentation

Suggested documentation areas:

- product vision
- gameplay models
- system architecture
- multiplayer lifecycle
- onboarding/tutorial design
- AI usage boundaries and guardrails
- deployment and operational notes

## Roadmap

### Near term

- establish repository structure
- define platform vs product boundaries
- formalize game/session data model
- ship first tutorial flows
- ship first multiplayer prototype

### Mid term

- richer notifications and session recovery
- content tooling for adding games
- analytics and playtesting feedback loops
- stronger admin and moderation surfaces

### Longer term

- additional games and content packs
- cross-platform SDK hardening
- AI-enhanced content and customization flows
- broader ecosystem around Achillea-based products

## Contributing

Contributions should align with the project principles:

- prefer simple, operable designs
- surface tradeoffs explicitly
- avoid hidden coupling between product and platform layers
- write docs when changing architecture or workflows

If contribution guidelines do not yet exist, treat small, well-explained pull requests as the default.

## Security notes

A few baseline expectations for a project like this:

- do not trust client state for authoritative multiplayer decisions
- protect invitation/session flows against abuse and spoofing
- treat notifications and identity edges as security boundaries
- avoid leaking location or player metadata unnecessarily
- document AI usage and keep human-review boundaries explicit

## License

**TBD**

Add the project license here once selected.

## Status

This project is in active design and early implementation.

Expect iteration in:

- architecture
- naming
- repository structure
- infrastructure choices
- product scope boundaries

---

## Related names

- **Achillea** — platform / SDK / shared foundation
- **Asterwild** — user-facing product built on the platform

---

Built with a platform-first mindset for playful outdoor systems.
