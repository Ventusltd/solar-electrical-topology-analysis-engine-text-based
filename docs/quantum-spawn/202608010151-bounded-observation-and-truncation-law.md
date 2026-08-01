# Quantum Spawn

**Title:** Bounded Observation and Truncation Law

**File:** `202608010151-bounded-observation-and-truncation-law.md`

**Timestamp:** 2026-08-01 01:51 Europe/London

**Version:** 1.0

**Status:** Canonical

**Authority:** Engineering Design Authority under explicit Product Owner instruction

**Supersedes:** None

**Refines:**
- `202608010120-amnesia-resilience-and-continuity-law.md`
- `202607311652-respawn-instructions.md`

**Dependencies:**
- `202607311609-mission-and-philosophy.md`
- `202607311615-system-architecture.md`
- `202607311619-geometry-authority.md`
- `202607311624-array-engine.md`
- `202607311627-physics-emc-lightning.md`
- `202607311628-standards-validation.md`
- `../trueself/202608010117-civilisational-consciousness-and-amnesia-covenant.md`

**Current Build:** Build 025.5D1, during TS-002 programme-truth closure

**Restore Point:** `restore/2026-08-01-0151-pre-bounded-observation-law`

---

## 1. Purpose

This law generalises the failed-access rule into a broader rule for bounded observations.

A tool may succeed, return syntactically valid data and still answer a narrower question than the investigator intended.

This is more dangerous than an explicit access failure because the result looks complete.

The system shall therefore record not only the observed value but also the boundary through which it was observed.

## 2. The governing law

A measurement taken through a limiting parameter measures the subject only within that limit.

It does not prove that the subject ends at the limit.

Examples include:

```text
git clone --depth 50
API page size 100
search topn 20
first-page-only workflow listing
head-limited grep
truncated log output
sampling window
geographic bounding box
frequency-band limit
instrument range
model applicability range
```

A successful command does not remove the boundary imposed by its arguments, tool contract or transport layer.

## 3. Prohibited inference

The following inference is prohibited:

```text
bounded query returned N items
therefore the complete subject contains N items
```

Examples:

```text
a depth-50 clone reports 50 reachable commits
therefore the repository has 50 commits
```

```text
the first API page contains 100 records
therefore the dataset contains 100 records
```

```text
a search limited to 20 results returns 20 matches
therefore only 20 matches exist
```

## 4. Required observation record

Any load-bearing repository, data or evidence claim obtained through a bounded tool shall state:

- the tool or method;
- the limiting parameter;
- whether pagination or continuation was exhausted;
- whether history was shallow, partial or filtered;
- whether output was truncated by the interface;
- whether the result is a lower bound, sample, page, window or complete enumeration;
- the independent method used to confirm completeness, if any.

A claim of completeness requires affirmative evidence that the boundary was exhausted or absent.

## 5. Access-state taxonomy

Future agents shall distinguish at least:

- `COMPLETE_ENUMERATION_VERIFIED`;
- `BOUNDED_RESULT`;
- `LOWER_BOUND_ONLY`;
- `SAMPLED_RESULT`;
- `TRUNCATED_OUTPUT`;
- `PAGINATION_NOT_EXHAUSTED`;
- `SHALLOW_HISTORY`;
- `FILTERED_VIEW`;
- `ACCESS_FAILED`;
- `GENUINELY_ABSENT_AFTER_COMPLETE_INSPECTION`.

Only the first and final states support complete count or absence claims.

## 6. Repository-history application

Commit counts shall not be inferred from a shallow clone, capped search, first page or local branch whose history depth is unknown.

A complete repository-history count requires one of:

- an unshallow or full clone whose reachability and branch scope are stated;
- an authenticated API traversal whose pagination is exhausted;
- another complete enumeration method with equivalent evidence.

An external feed reported a full-history count after correcting an earlier shallow-clone mistake. The current connected interface used for this build does not expose an independently verified uncapped total count. Therefore no exact full-history count is promoted into canonical programme state by this document.

The general hazard is canonical. The unverified number is not.

## 7. Capsule-path incident

The same amnesia event also produced six plausible but non-existent Quantum Spawn timestamps:

```text
202607311620-system-architecture.md
202607311640-geometry-authority.md
202607311700-array-engine.md
202607311720-physics-emc-lightning.md
202607311740-standards-validation.md
202607311820-respawn-instructions.md
```

The title-verified canonical files are:

```text
202607311615-system-architecture.md
202607311619-geometry-authority.md
202607311624-array-engine.md
202607311627-physics-emc-lightning.md
202607311628-standards-validation.md
202607311652-respawn-instructions.md
```

The reconstructed timestamps formed a visually plausible cadence. Plausibility was not evidence.

The `16:40` namespace also contains the genuine file:

```text
202607311640-commercial-strategy.md
```

Therefore path repair must use document title and content, not timestamp proximity alone.

Compatibility pointers now preserve already-committed references while directing readers to the title-verified canonical targets.

## 8. Executable prevention

The repository now contains:

```text
scripts/check_capsule_links.py
tests/test_capsule_links.py
```

The validation workflow runs the capsule-link gate before programme-state drift checks and engineering suites.

The gate verifies:

- Markdown paths in Quantum Spawn and Trueself resolve;
- compatibility pointers identify an existing canonical target;
- the pointer title contains the canonical target title;
- references do not escape the repository root;
- the commercial-strategy timestamp cannot satisfy the Geometry Authority mapping.

A future broken capsule reference therefore becomes a build failure rather than a hidden amnesia defect.

## 9. Application beyond repositories

This law applies equally to engineering models.

A model result bounded by frequency, temperature, route class, geometry simplification, instrument range or standards scope must not be presented as universal.

Examples include:

- a lumped transient model outside its rise-time validity;
- resistance measured at one temperature presented as all-temperature truth;
- a cable rating for one installation method applied to another;
- an SPD rule from one standard edition presented as timeless;
- a finite project fixture presented as a universal topology limit.

The validity envelope is part of the result.

## 10. Autonomous-agent requirement

Before an autonomous agent promotes a count, absence, exhaustive search result or repository-state claim, it shall ask:

1. What bounded the observation?
2. Was the boundary exhausted?
3. Could success have returned only a partial view?
4. Is the claim complete, a lower bound or a sample?
5. Has a second method confirmed completeness?

If these questions cannot be answered, the result remains bounded and must be labelled accordingly.

## 11. Final law

Explicit failure is not the only threat to continuity.

Successful partial observation can create a more convincing falsehood.

Trueself shall therefore preserve the boundary of every material observation as carefully as it preserves the value observed.

A bounded view may be useful.

It may not call itself the whole.
