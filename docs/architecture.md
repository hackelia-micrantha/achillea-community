# Achillea architecture: bundled v0.1 and proposed downloadable features

**Status:** public architecture review and design illustration, October 2026. This is **not** a published SDK, certified conformance suite, deployed feature downloader, or production release. This describes the private application's boundaries at a high level; it does not expose implementation code.

## What exists today

Asterwild is the Expo/React Native host. Its first local Pentalpha experience uses **bundled** packages: portable game definitions and deterministic rules depend on Achillea SDK contracts, while the host controls presentation, navigation, lifecycle, local storage, and native integration. Versioned local-session admission verifies saved records before reuse. Product release and physical-device acceptance remain in qualification.

~~~mermaid
flowchart TD
  Host["Asterwild - Expo / React Native host"]
  SDK["Achillea SDK - contracts and runtime"]
  Game["Pentalpha - bundled game package"]
  Surfaces["Host-owned views and navigation"]
  Storage["Host-owned local sessions / validated replay and recovery"]
  Native["Android / iOS / web adapters"]

  Host --> Game
  Host --> SDK
  Game --> SDK
  Host --> Surfaces
  Host --> Storage
  Host --> Native
~~~

**Boundary:** the SDK must not import Asterwild or a concrete game; a portable game package depends inward on the SDK, not on React Native screens. The application interprets semantic game surfaces and owns privileged effects. The first release requires no hosted account, downloaded runtime packages, or network game authority.

## Future direction: feature packs acquired on demand

Dynamic content is a **proposed extension after the local v0.1 slice**, not a verified Achillea runtime feature today. The important separation is between **downloading inert, declarative content** and **installing executable code**.

~~~mermaid
flowchart LR
  Publish["Reviewed feature definition and release metadata"] --> Catalog["Proposed versioned content catalog"]
  Catalog --> Fetch["Host-owned download client"]
  Fetch --> Gate{"Admission gate - proposed"}
  Gate -->|"reject"| No["No feature activation"]
  Gate -->|"allow"| Cache["Versioned verified cache - proposed"]
  Cache --> Resolve["Host capability / renderer registry"]
  Resolve --> Screen["Bundled views and trusted rules"]
  Screen --> Save["Host-owned session and recovery"]
~~~

For a future production downloader, the **host** would enforce an explicit origin/catalog policy, bounded download and parsing limits, schema and version checks, authenticated signing/integrity rooted in a separately trusted key/catalog, capability allowlists, dependency compatibility, safe offline caching, rollback, and reviewed lifecycle/failure semantics. A digest supplied by the same untrusted source **alone** would not prove authenticity. Versioned content may propose supported semantic surfaces but may not grant network, location, billing, file-system, background execution, or other privileges.

**Do not fetch and run JavaScript/TSX, arbitrary React components, game-rule functions, native modules, or dynamic eval as a feature pack.** If a feature needs new executable rules or host capabilities, ship a reviewed application/runtime update (or later design a separately reviewed, constrained interpreter) first. Downloaded definitions select only already-installed, explicitly allowed renderers and logic.

~~~mermaid
sequenceDiagram
  participant User
  participant Host as Host application
  participant Source as Public content origin
  participant Gate as Feature admission
  participant Render as Bundled renderer

  User->>Host: Request optional feature
  Host->>Source: Fetch versioned data pack (proposed)
  Source-->>Host: Declarative JSON
  Host->>Gate: Verify publisher, schema, compatibility and capabilities
  alt Admission denied
    Gate-->>Host: Reject without effects
    Host-->>User: Unavailable; keep existing state
  else Admission allowed
    Gate-->>Host: Validated definition
    Host->>Render: Bind to known host renderer
    Render-->>User: Guided steps and controls
  end
~~~

## Public example: Shape Hunt

The [standalone Shape Hunt demonstration](../web/feature-demo.html) **does** fetch a static, synthetic JSON definition on demand from the same public site, validates its small fixed shape, and uses pre-bundled browser JavaScript to present a three-step activity. The file [shape-hunt.v1.json](../web/examples/shape-hunt.v1.json) is human-readable and contains no executable code, credentials, location information, network addresses, or private Asterwild content. Serve the public site through an HTTP static server; opening the HTML as a file URL may block fetch.

The demo shows **data-driven user experience**, not Asterwild native integration or secure package admission. It deliberately lacks cryptographic authenticity, a trusted catalog, offline cache, rollback, native plugins, server authority, app distribution, and the full Achillea game-rule contract. The downloadable-pack path above remains proposed even though the independent browser illustration is executable.

## Source and publication boundaries

- Private implementation source: hackelia-micrantha/achillea (not published by this document).
- Public contract: [application state/effect draft](specifications/application-state-effects-v0.1.md), with unresolved reentrancy and failure semantics.
- Public release boundary: [proposed public/private policy](public-private-boundary.md).
- The earlier public [React Native / Expo hackathon prototype](https://github.com/ryjen/cactus-hackathon) is a reference for mobile experimentation, **not** proof of shared Achillea implementation, feature-download support, or product release.

The only executable sample published here is a new synthetic browser demonstration, not extracted private product source or a claim that private package code is available under a public license.
