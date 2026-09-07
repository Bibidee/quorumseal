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

- Version: v0.2.5.
- Contract freeze commit: `424c5b9382fe15766540e542fb769b50b6efe04f`.
- Tests: 12 helper/unit tests and 43 genuine Direct Mode contract tests passed (55 total). The Direct Mode suite covers artifact failures, malformed model output, URL-number-form bypasses, malicious-summary isolation, lifecycle/access control, and validator disagreement cases.
- StudioNet contract: [0xdEF0De3EbDB187301A95972E8e2e27999dE5aFf2](https://explorer-studio.genlayer.com/address/0xdEF0De3EbDB187301A95972E8e2e27999dE5aFf2).
- Deployment: [0xfabced18096383e5ca57af550e592d641bdc1510b4c5eff10868197c5bb9a3ba](https://explorer-studio.genlayer.com/tx/0xfabced18096383e5ca57af550e592d641bdc1510b4c5eff10868197c5bb9a3ba), FINALIZED / MAJORITY_AGREE / GenVM SUCCESS.
- `get_info()`: QuorumSeal v0.2.5, minimum confidence 75, maximum payload 24000 bytes.
- Source SHA-256: `9d8bcea60ac7a2955b15f504ae44171bab3d674de005db57881727cd10b6c399`.
- Source parity: VERIFIED through `gen_getContractCode`; the 10,252 deployed bytes match `contracts/quorumseal.py` byte-for-byte.
- Frozen-source CI: [run 34105136989](https://github.com/Bibidee/quorumseal/actions/runs/34105136989), completed successfully.

## Live lifecycle evidence

Seal `QS-LIVE-V025-FINAL` binds [payload](https://raw.githubusercontent.com/Bibidee/quorumseal/9c8085fb282aa92babdd6ff3ee6e880fb96f5eae/docs/live/v024-payload.txt) SHA-256 `0xa82d946b755eb15bdd4817f9e8765f664fef755d4f2eab8b0a3167f5530baff7` and [evidence](https://raw.githubusercontent.com/Bibidee/quorumseal/9c8085fb282aa92babdd6ff3ee6e880fb96f5eae/docs/live/v024-evidence.txt) SHA-256 `0x54823b942892c41f0c457c842cb999bc6009a6de525af52ac90bc18237427c0d`.

- [Proposal](https://explorer-studio.genlayer.com/tx/0xd6ac8d85e64e72fa9885c140eec78d691c1c683ada302446d9efff31ec84556c): FINALIZED / MAJORITY_AGREE / GenVM SUCCESS; persisted as `pending` with exact commitments.
- [Semantic review](https://explorer-studio.genlayer.com/tx/0x0c139601719d0f206680b9ccbe0295d0413d3eff320b1e570467b55badc5fe43): FINALIZED / MAJORITY_AGREE / GenVM SUCCESS; `approved`, confidence 100, with model-produced rationale after hash-verified artifact review.
- [Consumption](https://explorer-studio.genlayer.com/tx/0xf10bad8244707fe9943fa199554402d16c0e0770c905b3a527b79701d2115151): FINALIZED / MAJORITY_AGREE / GenVM SUCCESS; final state `consumed`.

The v0.2.4 deployment [0x57f05489B4C9BE96A5bCee43D977a21F18f5B499](https://explorer-studio.genlayer.com/address/0x57f05489B4C9BE96A5bCee43D977a21F18f5B499) (tx [0x94f45f519572a5fb9cf1d5b3820c1a475c48cee1dab368eb6e5737b7dc924039](https://explorer-studio.genlayer.com/tx/0x94f45f519572a5fb9cf1d5b3820c1a475c48cee1dab368eb6e5737b7dc924039)) and its v0.2.4 live evidence are historical/superseded by v0.2.5. The v0.2.3 deployment `0xD944F22d201a472Db68ae408508115DB1f6851A6` (tx `0x54bf3761fb0e0936204b840a27f5d4b70349f1c9ea405db2ac491273c279aa58`), the prior internal-metadata deployment `0x4495e1A63062f7c522A26e7F2b494F72B8aDDee7`, the v0.2.1 contract `0xCfE935A245CDC8963348B3CBb97dFb6b00bB80f9`, and older v0.2.0 deployment are also historical/superseded.
