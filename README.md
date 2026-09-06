# QuorumSeal

QuorumSeal is a reusable GenLayer Intelligent Contract primitive for hash-bound semantic approval. It binds payload and evidence URLs to SHA-256 commitments of exact raw bytes, verifies them before review, and presents verified content as untrusted quoted data to independent semantic validators.

Approval is deterministic and fail-closed: payload_match=yes, evidence_support=yes, risk=no, and confidence >=75 are all required. Malformed output, unavailable or oversized artifacts, invalid UTF-8, hash mismatch, or validator disagreement never authorizes an action. Lifecycle: `pending -> approved -> consumed`, `pending -> blocked`, or `pending -> cancelled`; only the designated consumer can consume.

QuorumSeal holds no funds or escrow and does not prove external-world truth. Exactly one deployable source is kept under `contracts/`; tests and tooling are outside it.

## Release evidence

- Version: v0.2.1.
- Contract freeze commit: `524db3f820aa3b47ed1cb469800990be382b41a7`.
- Tests: 11 helper/unit tests and 6 genuine Direct Mode contract tests passed (17 total); preflight, GenVM lint, and ABI schema passed.
- StudioNet contract: [0xCfE935A245CDC8963348B3CBb97dFb6b00bB80f9](https://explorer-studio.genlayer.com/address/0xCfE935A245CDC8963348B3CBb97dFb6b00bB80f9).
- Deployment: [0x0a16af48d1b99ae811110f31a20f722429770156e22a03b9889b1a61732f58a0](https://explorer-studio.genlayer.com/tx/0x0a16af48d1b99ae811110f31a20f722429770156e22a03b9889b1a61732f58a0), FINALIZED / MAJORITY_AGREE / GenVM SUCCESS.
- Source SHA-256: `a2723c637bbdbc5bbd054c4cb2bf57fd0d53e233a3746884a53e8c568de33601`.
- Source parity: VERIFIED through `gen_getContractCode`; the 8,887 deployed bytes match `contracts/quorumseal.py` byte-for-byte.
- Freeze-commit CI: [run 34050038366](https://github.com/Bibidee/quorumseal/actions/runs/34050038366), completed successfully.

## Live lifecycle evidence

Seal `QS-LIVE-V021-001` binds [payload](https://raw.githubusercontent.com/Bibidee/quorumseal/0aad42764e6b9ca6e6f182b0054891ca7d9264d9/docs/live/payload.txt) SHA-256 `0xd9ae2ce9d991b991b1d72c7b06058e20d91710f011b25e3c3ba98b34a776ee24` and [evidence](https://raw.githubusercontent.com/Bibidee/quorumseal/0aad42764e6b9ca6e6f182b0054891ca7d9264d9/docs/live/evidence.txt) SHA-256 `0xeb94cbea09fa3935b9d9e5e29320d7bd99d644021d3bdd70271e0d3d34d010d0`.

- [Proposal](https://explorer-studio.genlayer.com/tx/0x5803969ff872f399318e0f21b82df84850793731b95d4533beed1ec08b8a7a98): persisted as `pending` with exact commitments.
- [Semantic review](https://explorer-studio.genlayer.com/tx/0x17d6d6a9dbcf6054914d2ae7b4964e4efbddf8ea4464b6a741e5c36741138fb0): FINALIZED / MAJORITY_AGREE / GenVM SUCCESS; `approved`, confidence 100, rationale “The evidence explicitly authorizes the exact payload specified.”
- [Consumption](https://explorer-studio.genlayer.com/tx/0xfc90c4fce6b5f66cba9f42b8108c9666afe95bd9fc326477483050f8cc244939): FINALIZED / MAJORITY_AGREE / GenVM SUCCESS; final state `consumed`.

The older v0.2.0 contract `0x7ad42e7f6f2A0f2C10402a55e5B158d0E320CAde` is historical and is not the current release.
