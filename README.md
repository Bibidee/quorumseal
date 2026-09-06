# QuorumSeal

QuorumSeal is a reusable GenLayer Intelligent Contract primitive for hash-bound semantic approval. It binds payload and evidence URLs to SHA-256 commitments of exact raw bytes, verifies them before review, and presents verified content as untrusted quoted data to independent semantic validators.

Approval is deterministic and fail-closed: payload_match=yes, evidence_support=yes, risk=no, and confidence >=75 are all required. Malformed output, unavailable or oversized artifacts, invalid UTF-8, hash mismatch, or validator disagreement never authorizes an action. Lifecycle: `pending -> approved -> consumed`, `pending -> blocked`, or `pending -> cancelled`; only the designated consumer can consume.

QuorumSeal holds no funds or escrow and does not prove external-world truth. Exactly one deployable source is kept under `contracts/`; tests and tooling are outside it.

## Release evidence

- Version: v0.2.0.
- Direct Mode: 7 tests passing; preflight, GenVM lint, and ABI schema passing locally.
- Current deployment: [0xAd9FF5Bd3d9b5E49264bC825A45c30409D236aF0](https://explorer-studio.genlayer.com/address/0xAd9FF5Bd3d9b5E49264bC825A45c30409D236aF0).
- Deployment transaction: [0xad62f6ebb20029a56424bc28af6c0e1f476fe93e7eed64ac13b22db33b6ccc80](https://explorer-studio.genlayer.com/tx/0xad62f6ebb20029a56424bc28af6c0e1f476fe93e7eed64ac13b22db33b6ccc80), FINALIZED with GenVM SUCCESS.
- Source SHA-256: `5e800d049ce1f2b1a032bd9283a4f3a14953e27c6fdba4e7ab4305d6078aa00b`.
