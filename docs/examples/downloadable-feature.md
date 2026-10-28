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
