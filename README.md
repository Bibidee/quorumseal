# QuorumSeal

QuorumSeal is a reusable GenLayer Intelligent Contract primitive for hash-bound semantic approval. It binds payload and evidence URLs to SHA-256 commitments of exact raw bytes, verifies them before review, and presents verified content as untrusted quoted data to independent semantic validators.

Approval is deterministic and fail-closed: payload_match=yes, evidence_support=yes, risk=no, and confidence >=75 are all required. Malformed output, unavailable or oversized artifacts, invalid UTF-8, hash mismatch, or validator disagreement never authorizes an action. Lifecycle: `pending -> approved -> consumed`, `pending -> blocked`, or `pending -> cancelled`; only the designated consumer can consume.

QuorumSeal holds no funds or escrow and does not prove external-world truth. Exactly one deployable source is kept under `contracts/`; tests and tooling are outside it.

## Release evidence

- Version: v0.2.0.
- Direct Mode: 7 tests passing; preflight, GenVM lint, and ABI schema passing locally.
- Current deployment: [0x7ad42e7f6f2A0f2C10402a55e5B158d0E320CAde](https://explorer-studio.genlayer.com/address/0x7ad42e7f6f2A0f2C10402a55e5B158d0E320CAde).
- Deployment transaction: [0x3c0d835a2104936dd5e8c37acdfcf09733b7eb56bc0ba1008a5a31d55e8e8dc5](https://explorer-studio.genlayer.com/tx/0x3c0d835a2104936dd5e8c37acdfcf09733b7eb56bc0ba1008a5a31d55e8e8dc5), FINALIZED with GenVM SUCCESS.
- Source SHA-256: `f5193fb375cf27f16bfc8abc3535f660c2c9980cc49d49807348a43a991ee9c5`.
- GitHub Actions release gate: [run 34037930541](https://github.com/Bibidee/quorumseal/actions/runs/34037930541), completed successfully for the final documentation HEAD.
