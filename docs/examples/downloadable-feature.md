# Downloadable feature illustration: Shape Hunt

**Example status:** public synthetic **browser-only** reference; **not** a working Achillea/Asterwild mobile feature package. No game implementation, proprietary assets, downloaded executable code, or actual player/location data are published.

- [Open the standalone browser example](../../web/feature-demo.html) through an HTTP static server.
- [Read its declarative JSON](../../web/examples/shape-hunt.v1.json).
- [See current and future architecture diagrams](../architecture.md).

## What the example proves

1. The example host starts with *no Shape Hunt content in its JavaScript source*.
2. On a click, the host fetches a **fixed same-origin** JSON file and rejects unknown structure, unsupported schema/version/renderer, duplicate step IDs, oversized fields, and malformed steps.
3. A bundled guided-checklist/v1 renderer displays the downloaded prompts using DOM textContent, not HTML interpretation. User selection moves between three steps; progress exists only in memory.
4. The pack contains **data only**. It cannot define event handlers, permissions, navigation destinations, network calls, rule code, or React Native modules.

The browser demonstrates *on-demand data-driven feature presentation*, not safe offline production installation or the private Achillea SDK. There is no cryptographic signature, trusted catalog, persisted offline cache, entitlement, native integration, host-version negotiation, or production-grade resource isolation.

## Worked feature path (public implementation)

The implementation is the [standalone browser page](../../web/feature-demo.html), its [same-origin fixture](../../web/examples/shape-hunt.v1.json), and [isolated tests](../../tests/feature-demo.test.mjs). This flow does **not** run in the private Asterwild app.

1. **User intent:** Until the visitor presses **Download sample feature**, the page makes no sample request. The click handler fetches the fixed relative URL `./examples/shape-hunt.v1.json` with `credentials: "omit"` and `cache: "no-store"`.
2. **Bounded admission:** The page rejects failed HTTP responses, an announced response longer than 12,000 bytes, missing streaming response bodies, and payloads that exceed 12,000 bytes while being read. Rejected or completed streams are cancelled/released where the implementation permits.
3. **Closed contract:** `validate()` requires the exact pack keys (`schema`, `id`, `version`, `title`, `description`, `renderer`, `steps`), the expected `shape-hunt` identity, schema `achillea.public-demo.feature/v1`, version `1.0.0`, and the already-installed `guided-checklist/v1` renderer. It expects exactly three steps, exact step keys (`id`, `prompt`, `hint`), unique lowercase-hyphenated step identifiers, and nonempty strings of at most 180 JavaScript string units for bounded text fields.
4. **Trusted rendering:** The page's own JavaScript maps the validated prompts and hints into `textContent`. The fetched definition cannot supply HTML, event handlers, URLs, callbacks, or executable rules; unknown fields or renderer IDs are rejected.
5. **Local outcome:** **Found it** and **Skip** advance an in-memory index and count; the page displays a result and can restart locally. Rejected content hides the activity. Refreshing the page discards progress; the example never writes it to storage or sends answers to a server.

**Boundary:** downloaded **data** → bounded/schema-checked admission → **preinstalled** browser renderer → local interaction. This does not establish source authenticity, signed publisher identity, durable offline installation, device permissions, or a general-purpose Achillea feature host. The size/schema checks reduce inputs accepted by this *specific illustration*, not all possible resource or application risks.

### Reproducible evidence and known limits

The public [test suite](../../tests/feature-demo.test.mjs) exercises click-triggered loading, valid progression and replay, unknown schemas/renderers/fields, duplicate step IDs, markup rendered as inert text, oversized streamed responses, early rejection of oversized `Content-Length`, HTTP failures, absent bodies, and malformed JSON. These are synthetic DOM/response tests; they do **not** verify physical mobile devices, browser accessibility, private SDK conformance, trusted remote publishers, or live Cloudflare deployment.

### Earlier Expo application as a design precedent

The separate public [Eyespie / cactus-hackathon repository](https://github.com/ryjen/cactus-hackathon) describes a React Native/Expo camera and clue-generation application. Its public feature folders cover [camera](https://github.com/ryjen/cactus-hackathon/tree/main/src/features/camera), [game creation](https://github.com/ryjen/cactus-hackathon/tree/main/src/features/game-creation), [clue creation](https://github.com/ryjen/cactus-hackathon/tree/main/src/features/clues-creation), and [sharing](https://github.com/ryjen/cactus-hackathon/tree/main/src/features/game-share); its package manifest declares `expo-camera` and `cactus-react-native`. It is a **separate design reference**, not a released Achillea feature, source dependency, proof of integration, or authorization to add camera/AI permissions to this demo. No code or assets from that repository are redistributed here.

## Proposed production contract (not implemented)

A future Achillea content-pack proposal would have to define a schema identifier, immutable package identity/version, approved renderer/rules references, supported host versions, allowed capabilities, a signed publisher/release identity independent of the download transport, strict sizes and parsing bounds, safe update/revocation/rollback, and the behavior for missing or stale content. A version digest alone is insufficient if the adversary also controls its source.

**An updated game engine or new native capability must ship with a reviewed app/runtime release**; never interpret a downloaded JavaScript module as a trusted effect. The host remains authoritative for persistence, routes, permissions, accessibility, lifecycle, and physical device effects.

## Development and documentation checks

From the public repo root:

~~~sh
python3 -m http.server 8000 -d web
# Then open http://localhost:8000/feature-demo.html
~~~

For the isolated browser loader's regression tests, use Node.js 20+ from the repository root:

~~~sh
node --test tests/feature-demo.test.mjs
~~~

The tests use a synthetic DOM and in-memory HTTP responses; they check normal rendering, missing/invalid and oversized content, unsupported renderers, and markup-as-text. They are not a physical mobile test, a browser accessibility audit, or proof of production feature admission.

This serves only static files. It does not require application credentials, an account, backend services, or a downloaded SDK. Keep public/private boundaries and licensing review independent of the example.
