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

- Version: v0.2.4.
- Contract freeze commit: `5334ffae39555ef2565a9482c65071fa6a4de38c`.
- Tests: 12 helper/unit tests and 40 genuine Direct Mode contract tests passed (52 total). The Direct Mode suite covers artifact failures, malformed model output, URL literal bypasses, malicious-summary isolation, lifecycle/access control, and seven actual `run_validator()` disagreement cases.
- StudioNet contract: [0x57f05489B4C9BE96A5bCee43D977a21F18f5B499](https://explorer-studio.genlayer.com/address/0x57f05489B4C9BE96A5bCee43D977a21F18f5B499).
- Deployment: [0x94f45f519572a5fb9cf1d5b3820c1a475c48cee1dab368eb6e5737b7dc924039](https://explorer-studio.genlayer.com/tx/0x94f45f519572a5fb9cf1d5b3820c1a475c48cee1dab368eb6e5737b7dc924039), FINALIZED / MAJORITY_AGREE / GenVM SUCCESS.
- Source SHA-256: `6323d2936ad078e89af3f2ffcc1fe629f41c9042d9af40d5aa9c3c5db5dc6f90`.
- Source parity: VERIFIED through `gen_getContractCode`; the 10,007 deployed bytes match `contracts/quorumseal.py` byte-for-byte.
- Frozen-source CI: [run 34099852220](https://github.com/Bibidee/quorumseal/actions/runs/34099852220), completed successfully.

## Live lifecycle evidence

Seal `QS-LIVE-V024-FINAL` binds [payload](https://raw.githubusercontent.com/Bibidee/quorumseal/9c8085fb282aa92babdd6ff3ee6e880fb96f5eae/docs/live/v024-payload.txt) SHA-256 `0xa82d946b755eb15bdd4817f9e8765f664fef755d4f2eab8b0a3167f5530baff7` and [evidence](https://raw.githubusercontent.com/Bibidee/quorumseal/9c8085fb282aa92babdd6ff3ee6e880fb96f5eae/docs/live/v024-evidence.txt) SHA-256 `0x54823b942892c41f0c457c842cb999bc6009a6de525af52ac90bc18237427c0d`.

- [Proposal](https://explorer-studio.genlayer.com/tx/0x014e2c3ec76b24f9a5e9485776eca9f9d12d6d745b9484cedc85708cd3a45f8b): FINALIZED / MAJORITY_AGREE / GenVM SUCCESS; persisted as `pending` with exact commitments.
- [Semantic review](https://explorer-studio.genlayer.com/tx/0x8166dde57fa962dcb6ffc5ef75461ff56b7ef7180e08adc8c8b034e4bdd79347): FINALIZED / MAJORITY_AGREE / GenVM SUCCESS; `approved`, confidence 90, with model-produced rationale after hash-verified artifact review.
- [Consumption](https://explorer-studio.genlayer.com/tx/0x2621c6203d0770df418a06e1bbfe8548d9be01b2b2cd2d7cd565be30b0249377): FINALIZED / MAJORITY_AGREE / GenVM SUCCESS; final state `consumed`.

The v0.2.3 deployment `0xD944F22d201a472Db68ae408508115DB1f6851A6` (tx `0x54bf3761fb0e0936204b840a27f5d4b70349f1c9ea405db2ac491273c279aa58`), the prior internal-metadata deployment `0x4495e1A63062f7c522A26e7F2b494F72B8aDDee7`, the v0.2.1 contract `0xCfE935A245CDC8963348B3CBb97dFb6b00bB80f9`, and older v0.2.0 deployment are historical/superseded.
