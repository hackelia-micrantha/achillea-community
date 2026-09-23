# Application state/effect contract — draft v0.1

Status: **proposal for review, not an adopted public API or SDK release**. This is an independently written, product-neutral description of the existing *reduce → publish → induce* architectural pattern and the questions that must be resolved before claiming multi-language conformance. It does not publish private implementation source, game rules or product content.

## Scope and vocabulary

- **State**: a feature's immutable logical snapshot; implementations MAY retain private mutable runtime bookkeeping, not mutable state exposed to consumers.
- **Intent**: a typed request presented to the feature boundary. An intent is not proof that its payload is authorized or valid.
- **Reducer**: a synchronous, deterministic, side-effect-free transition `reduce(state, intent) → nextState`.
- **Publisher**: exposes the current snapshot to observers.
- **Interactor**: owns dispatch, orchestration and invoking effects after state reduction/publication.
- **Effect**: IO, navigation, timers, remote operations, persistence or other work outside the pure reducer. An effect MAY emit a follow-up intent.
- **Host adapter**: product-specific presentation, storage, navigation, telemetry, security and lifecycle integration. The core architecture does not know their concrete implementations.

**Normative terminology:** MUST, SHOULD and MAY below describe the **candidate portable contract** for implementations claiming conformance. They are not statements that an existing TypeScript or Kotlin implementation has already passed. Any rule marked *unresolved* is explicitly **not** normative.

## Candidate minimum contract (non-reentrant, controlled-effect path)

1. Each feature MUST have an initial state and a documented closed set of supported intent shapes, including payload validation rules. A reducer MUST be synchronous, deterministic for the same inputs, and MUST NOT invoke effects, read ambient time, or mutate its input snapshot.
2. For a valid dispatch, the interactor MUST read the feature's current state, invoke its reducer once for that intent, and expose the resulting snapshot before invoking the corresponding effect. A rejected or malformed intent MUST NOT be treated as authorized merely because the UI emitted it.
3. An unchanged transition MAY keep the same state object/snapshot and suppress a redundant observer notification. **Effect invocation MUST NOT be skipped solely because the reducer returned an unchanged snapshot.** Whether an *equal but freshly allocated* state is republished is host-defined; portable fixtures only test explicit no-change transitions.
4. Effects MUST NOT mutate an already-published state snapshot. A follow-up transition MUST go through dispatch so that the reducer and observers can account for it.
5. Presentation MUST consume state plus a dispatch capability (or ecosystem-equivalent); view code MUST NOT reach into storage, privileged IO, game authorization, or the feature reducer as an alternative write path. Dependency direction MUST point from application/host adapters toward domain and public contracts, never from domain to product UI or infrastructure.
6. Dependencies for use cases, clocks, repositories and effects SHOULD be injected at a composition boundary. An implementation claiming production readiness MUST define how it validates boundary inputs, handles effect failures, protects privileged operations and tears down feature-scoped resources. Client-side state alone MUST NOT authorize server-side actions.

### Ordering and delivery: bounded guarantees

For the **fixture path with no reentrant observer dispatch** and a controllable effect completion, the required causal sequence is:

```text
dispatch(intent A)
  → reduce(state 0, A)
  → publish(state 1, if changed)
  → invoke effect(A, post-publication state)
  → effect eventually dispatches intent B
  → reduce(latest state, B)
  → publish(state 2, if changed)
```

- For a synchronous dispatch in this bounded path, reduction and publication MUST happen before that dispatch's effect invocation.
- An effect's follow-up intent MUST be processed against the **state current when the follow-up is dispatched**, not against an earlier captured snapshot.
- The contract does **not** promise that asynchronous effects complete in dispatch order, that effect invocation waits for earlier asynchronous effects, or that all intents are globally serialized.
- Observer notifications MAY synchronously dispatch another intent, depending on the host state container. Nested dispatch can advance the state between the original publication and its effect invocation. Consequently, **the precise state observed by an outer effect during reentrant dispatch is unresolved** for cross-language conformance; clients MUST NOT rely on it until a separate ordering decision and test have been adopted.
- Notification timing, equality for freshly created snapshots, reducer reentrancy policy, effect parallelism/ordering and the treatment of dispatch during teardown are *unresolved*. Implementations MUST document their actual behavior and MUST NOT claim portable conformance for those paths based on this draft.
- Cancellation and feature lifetime ownership are *unresolved*. A producer MUST NOT infer that a pending effect is cancelled on unmount or reinitialization. Production implementations SHOULD introduce explicit lifecycle ownership and stale-result handling before initiating consequential effects.

### Failure and security boundaries

- Reducer exceptions, synchronous effect exceptions and asynchronous effect failures have different propagation surfaces. The portable fixture tests only successful transitions. The failure policy (propagate, typed failure intent, supervisory handler, cancellation, retry/idempotency) is *unresolved* and requires a dedicated decision and tests before adoption as a production runtime contract.
- Rejections or completion callbacks from asynchronous effects MUST NOT silently authorize a privileged operation, and production effect owners MUST route failures to a defined error/telemetry policy rather than relying on an unobserved promise.
- Validate restored/untrusted persisted state before a reducer consumes it. Product-specific persistence schema, storage, and lifetime policy are host concerns; game-engine state validation and recovery belong to separate game/runtime contracts.
- This specification supplies no sandbox or access-control mechanism. A model, UI or reducer cannot grant capabilities by emitting a typed intent; privileged adapters must independently enforce authorization and least privilege.

## Evidence boundary / mappings

This document is derived from general application architecture, not a source copy. The current private TypeScript/React Native implementation is the extraction input for the proposal, **not a conformance certificate**:

| Topic | Observed development implementation | Portable status |
| --- | --- | --- |
| Transition | Synchronous reducer followed by state publication, then effect hook | Candidate rule for the bounded fixture |
| No change | A retained state identity suppresses publication; effect hook still runs | Fixture covers retained-snapshot transition |
| Store/adapter | Observable feature store and presentation hook | Host-specific; StateFlow/ViewModel or other adapters MAY be used |
| Reentrancy | Synchronous subscribers can cause nested dispatch before an outer effect | Unresolved for portable guarantees |
| Async effects | Invoked without awaiting completion | Completion ordering, cancellation and failure handling unresolved |
| Error behavior | No general cross-runtime effect error/cancellation protocol | **Gap**, not a production-ready guarantee |

### Idiomatic adaptation (illustrative, not normative public API)

- **TypeScript/React Native:** discriminated intent unions; a pure synchronous reducer; a feature store and hook exposing `state + dispatch`; injected use cases; an interactor that owns effect invocation. Do not rely on `void`-discarded promises as a failure policy.
- **Kotlin:** sealed intents; immutable state data types; a reducer; a `StateFlow`-like observable state holder; a ViewModel/presenter or another lifecycle owner; coroutines for effects. Default StateFlow conflation/equality, coroutine scope cancellation and collector scheduling **do not automatically match** identity-based TypeScript publication or synchronous subscriber reentrancy. Define an adapter/event trace before asserting conformance.
- Neither mapping requires a shared binary, UI framework, JSON wire format or identical public method names.

## Conformance work and evolution

The adjacent [synthetic conformance fixtures](conformance/application-cycle-v0.1.json) test two **bounded** flows: successful effect completion and an unchanged-state intent whose effect still executes. They contain no game content, private code, location or network identifiers. Fixture traces describe logical events, not framework render order or an async wall-clock schedule.

Before closing the architecture-spec issue: demonstrate the same logical event traces in TypeScript and Kotlin, decide reentrancy, subscriber publication semantics, effect concurrency/failure/cancellation and stale-response policy in a reviewed ADR, and extend fixtures with those cases. The alternate design `reduce(state, intent) → state + effects` remains an option for a subsequent revision, **not** an implied change to the current `reduce → publish → induce` architecture.

No public application runtime, conformance runner, SDK package or release is included with this document.
