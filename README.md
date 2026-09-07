# QuorumSeal

QuorumSeal is a reusable GenLayer Intelligent Contract primitive for hash-bound semantic approval. It binds payload and evidence URLs to SHA-256 commitments of exact raw bytes, verifies them before review, and presents verified content as untrusted quoted data to independent semantic validators.

Approval is deterministic and fail-closed: payload_match=yes, evidence_support=yes, risk=no, and confidence >=75 are all required. Malformed output, unavailable or oversized artifacts, invalid UTF-8, hash mismatch, or validator disagreement never authorizes an action. Lifecycle: `pending -> approved -> consumed`, `pending -> blocked`, or `pending -> cancelled`; only the designated consumer can consume.

QuorumSeal holds no funds or escrow and does not prove external-world truth. Exactly one deployable source is kept under `contracts/`; tests and tooling are outside it.

## Why GenLayer / what breaks without GenLayer?

The security decision is intentionally distributed. A single off-chain LLM or centralized verifier could selectively approve a convenient interpretation, hide an unavailable artifact, or change its answer without an auditable consensus boundary. QuorumSeal instead makes every validator independently fetch the exact HTTPS payload and evidence bytes, verify their SHA-256 commitments, and perform its own semantic authorization judgment. The deterministic contract approves only when the independent outcomes agree and every approval condition is satisfied. Without GenLayer, downstream users would need to trust one operator or build and operate an equivalent independent-review quorum themselves.

## Downstream integration

Another Intelligent Contract can use QuorumSeal as an authorization gate before applying a sensitive change:

```python
seal = quorumseal.get_seal("release-2026-09")
if seal["status"] != "approved":
    raise gl.vm.UserError("[EXPECTED] QuorumSeal approval required")
quorumseal.consume("release-2026-09")  # called by the designated consumer
apply_committed_change()
```

The integrating contract must use the designated consumer identity, verify the committed payload again if its own policy requires it, and treat every other status—including `pending`, `blocked`, `cancelled`, and `consumed`—as non-authorizing.

## Release evidence

- Version: v0.2.2.
- Contract freeze commit: `4f39e5b5ef023aceb13263269a75bfafee9a4138`.
- Tests: 12 helper/unit tests and 34 genuine Direct Mode contract tests passed (46 total). The Direct Mode suite covers artifact failures, malformed model output, malicious-summary isolation, lifecycle/access control, and seven actual `run_validator()` disagreement cases.
- StudioNet contract: [0x4495e1A63062f7c522A26e7F2b494F72B8aDDee7](https://explorer-studio.genlayer.com/address/0x4495e1A63062f7c522A26e7F2b494F72B8aDDee7).
- Deployment: [0x0812a35ba4bd5a113af536c34f38bedad2639fb74b66f8e6dd786ae2ae9ec312](https://explorer-studio.genlayer.com/tx/0x0812a35ba4bd5a113af536c34f38bedad2639fb74b66f8e6dd786ae2ae9ec312), FINALIZED / MAJORITY_AGREE / GenVM SUCCESS.
- Source SHA-256: `8130be01c3ceccf2dbf9209b1f0149365e1f1a00ff27b0515275f4a3b84098c1`.
- Source parity: VERIFIED through `gen_getContractCode`; the 8,853 deployed bytes match `contracts/quorumseal.py` byte-for-byte.
- Freeze-commit CI: [run 34052207874](https://github.com/Bibidee/quorumseal/actions/runs/34052207874), completed successfully.

## Live lifecycle evidence

Seal `QS-LIVE-V022-001` binds [payload](https://raw.githubusercontent.com/Bibidee/quorumseal/89c836a775af6a153ff81c7af7a382d67b36657a/docs/live/v022-payload.txt) SHA-256 `0x2a575d94b9ccfd6c2f4ca7d114169b55edd55d717a2e1384d6d7b8e4c3a096a9` and [evidence](https://raw.githubusercontent.com/Bibidee/quorumseal/89c836a775af6a153ff81c7af7a382d67b36657a/docs/live/v022-evidence.txt) SHA-256 `0x40209cae06836a028b467f55812abab891bd99b551e22e1aa6d58e20473fefe8`.

- [Proposal](https://explorer-studio.genlayer.com/tx/0xa9e6bb1fc667a05709ceeacd974bd81b5f4c2a22fc06c72d0288e218a1a45ca9): FINALIZED / MAJORITY_AGREE / GenVM SUCCESS; persisted as `pending` with exact commitments.
- [Semantic review](https://explorer-studio.genlayer.com/tx/0xc8928e6e4d6857d5196ef5309d07b3cb22b49a0476a4b4687ecf80e646927ee7): FINALIZED / MAJORITY_AGREE / GenVM SUCCESS; `approved`, confidence 96, rationale “Evidence explicitly authorizes the exact QuorumSeal v0.2.2 live verification ID in the payload.”
- [Consumption](https://explorer-studio.genlayer.com/tx/0xa2ed5e6249eb3b95a18d4b2625a9263a7cf2b5b3f51a3f4be84cae4a5d53163b): FINALIZED / MAJORITY_AGREE / GenVM SUCCESS; final state `consumed`.

The v0.2.1 contract `0xCfE935A245CDC8963348B3CBb97dFb6b00bB80f9` and older v0.2.0 deployment are historical.
