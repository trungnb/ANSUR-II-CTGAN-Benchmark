# Change Policy

All modifications to this repository must respect the following 4-level change hierarchy.

## Change Levels

### LEVEL 0 — Implementation Detail
May change freely.
- Internal refactoring within private functions or modules.
- Local performance optimizations that preserve algorithmic invariants.
- Private helper extraction, code cleanup, formatting.

### LEVEL 1 — Local Behaviour
May change when required by the requested task.
- Adjusting internal error messages or validation text.
- Tuning local timeouts, retry counts, or internal parameters.
- Adding targeted unit tests and test fixtures.

### LEVEL 2 — Product / Research Behaviour
**Preserve unless explicitly requested to change.**
- User-visible workflows, UI interactions, and CLI subcommands.
- Schema extensions and backwards-compatible data model updates.
- Non-breaking API additions.
- Adding secondary analysis pipelines.

### LEVEL 3 — Architecture / Locked Product or Research Decision
**Explicit user approval required.**
- Breaking changes to public APIs or schemas.
- Merging distinct workflows or removing existing capabilities.
- Changing taxonomies, categorization schemas, or validation states.
- Changing security model, authentication, or authorization rules.
- Changing source of truth or persistence guarantees.
- Changing research primary outcome or clinical interpretation.
- Changing validation order (e.g. phantom-before-clinical).
- Altering pre-specified statistical modeling plans.

## Conflict Resolution Protocol
If a requested change conflicts with an `ACCEPTED` or `LOCKED` decision:
1. Do not silently implement the conflict.
2. Identify the affected ADR in `docs/governance/decisions/`.
3. Explain the conflict clearly.
4. Propose compatible alternatives.
5. Require explicit approval before altering any `LOCKED` decision.
