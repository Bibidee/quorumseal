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
- Contract freeze commit: `08c00104d573f347d6389ed78bdd56c84ed12b02`.
- Tests: 12 helper/unit tests and 34 genuine Direct Mode contract tests passed (46 total). The Direct Mode suite covers artifact failures, malformed model output, malicious-summary isolation, lifecycle/access control, and seven actual `run_validator()` disagreement cases.
- StudioNet contract: [0x4495e1A63062f7c522A26e7F2b494F72B8aDDee7](https://explorer-studio.genlayer.com/address/0x4495e1A63062f7c522A26e7F2b494F72B8aDDee7).
- Deployment: [0x0812a35ba4bd5a113af536c34f38bedad2639fb74b66f8e6dd786ae2ae9ec312](https://explorer-studio.genlayer.com/tx/0x0812a35ba4bd5a113af536c34f38bedad2639fb74b66f8e6dd786ae2ae9ec312), FINALIZED / MAJORITY_AGREE / GenVM SUCCESS.
- Source SHA-256: `e21b6c47fffc2af43f178a334f18c6a07fc688520ca9b0fc39e65bc239c86b2b`.
- Source parity: VERIFIED through `gen_getContractCode`; the 8,853 deployed bytes match `contracts/quorumseal.py` byte-for-byte.
- Final-head CI: [run 34088281175](https://github.com/Bibidee/quorumseal/actions/runs/34088281175), completed successfully.

## Live lifecycle evidence

Seal `QS-LIVE-V023-001` binds [payload](https://raw.githubusercontent.com/Bibidee/quorumseal/dcd516763eb755ad275208c5462ce67d27217de9/docs/live/v023-payload.txt) SHA-256 `0x8e6d49bcf5ababf38f10dd746a045bd51af1442b518e0b7bacd69e0b85232811` and [evidence](https://raw.githubusercontent.com/Bibidee/quorumseal/0e16b74546e238db05efd8b3f7d9655719f92bd0/docs/live/v023-evidence.txt) SHA-256 `0x2b29b72019d8a0a257f18cb6c141c0f96ce25348d0572a08036f509665066775`.

- [Proposal](https://explorer-studio.genlayer.com/tx/0x7cd32e68ecfbb80008c320ae925f32de94eee94c76dc17182c41e4d6cef2a3ac): FINALIZED / MAJORITY_AGREE / GenVM SUCCESS; persisted as `pending` with exact commitments.
- [Semantic review](https://explorer-studio.genlayer.com/tx/0x036d7c660234bbb0f0fe9c3c893f8ee7f78e10d70d96bd09a6bb52b12994f822): FINALIZED / MAJORITY_AGREE / GenVM SUCCESS; `approved`, confidence 90, rationale “Evidence explicitly authorizes the exact payload content.”
- [Consumption](https://explorer-studio.genlayer.com/tx/0x5d25a1b031b8fbcdffa8c34f9457aeaa9afe28c17c07957bc819124bb1c3ff3d): FINALIZED / MAJORITY_AGREE / GenVM SUCCESS; final state `consumed`.

The v0.2.1 contract `0xCfE935A245CDC8963348B3CBb97dFb6b00bB80f9` and older v0.2.0 deployment are historical.
