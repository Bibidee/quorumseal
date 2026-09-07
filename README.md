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

- Version: v0.2.3.
- Contract freeze commit: `ae58e66fdb4442f5154c709b8e694e7b5c4738c3`.
- Tests: 12 helper/unit tests and 34 genuine Direct Mode contract tests passed (46 total). The Direct Mode suite covers artifact failures, malformed model output, malicious-summary isolation, lifecycle/access control, and seven actual `run_validator()` disagreement cases.
- StudioNet contract: [0xD944F22d201a472Db68ae408508115DB1f6851A6](https://explorer-studio.genlayer.com/address/0xD944F22d201a472Db68ae408508115DB1f6851A6).
- Deployment: [0x54bf3761fb0e0936204b840a27f5d4b70349f1c9ea405db2ac491273c279aa58](https://explorer-studio.genlayer.com/tx/0x54bf3761fb0e0936204b840a27f5d4b70349f1c9ea405db2ac491273c279aa58), FINALIZED / MAJORITY_AGREE / GenVM SUCCESS.
- Source SHA-256: `98588934c90e834450779f1a60c8b0a12bbc1a2a93e021a239616e34fe61f0a3`.
- Source parity: VERIFIED through `gen_getContractCode`; the 9,949 deployed bytes match `contracts/quorumseal.py` byte-for-byte.
- Final-head CI: [run 34089315537](https://github.com/Bibidee/quorumseal/actions/runs/34089315537), completed successfully.

## Live lifecycle evidence

Seal `QS-LIVE-V023-FINAL` binds [payload](https://raw.githubusercontent.com/Bibidee/quorumseal/dcd516763eb755ad275208c5462ce67d27217de9/docs/live/v023-payload.txt) SHA-256 `0x8e6d49bcf5ababf38f10dd746a045bd51af1442b518e0b7bacd69e0b85232811` and [evidence](https://raw.githubusercontent.com/Bibidee/quorumseal/0e16b74546e238db05efd8b3f7d9655719f92bd0/docs/live/v023-evidence.txt) SHA-256 `0x2b29b72019d8a0a257f18cb6c141c0f96ce25348d0572a08036f509665066775`.

- [Proposal](https://explorer-studio.genlayer.com/tx/0xc884ed732ac621370e1f5debec41cd29a68cc0500f771e5d92c5a91e801afa24): FINALIZED / MAJORITY_AGREE / GenVM SUCCESS; persisted as `pending` with exact commitments.
- [Semantic review](https://explorer-studio.genlayer.com/tx/0xf6bb8c04c1ed99d471490a4fecc6a989ae93ae7536131a00499aa0cb46b87b50): FINALIZED / MAJORITY_AGREE / GenVM SUCCESS; `approved`, confidence 85, with model-produced rationale after hash-verified artifact review.
- [Consumption](https://explorer-studio.genlayer.com/tx/0x05402db29eef31667614ab685e5e1ea983417c8563079c1cb312de698c4248b4): FINALIZED / MAJORITY_AGREE / GenVM SUCCESS; final state `consumed`.

The prior v0.2.3-internal-metadata deployment `0x4495e1A63062f7c522A26e7F2b494F72B8aDDee7` (tx `0x0812a35ba4bd5a113af536c34f38bedad2639fb74b66f8e6dd786ae2ae9ec312`), the v0.2.1 contract `0xCfE935A245CDC8963348B3CBb97dFb6b00bB80f9`, and older v0.2.0 deployment are historical/superseded.
