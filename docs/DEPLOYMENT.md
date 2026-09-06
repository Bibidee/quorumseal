# Deployment

The v0.2.2 release gate passed: 12 helper/unit tests and 34 genuine Direct Mode contract tests (46 total), plus syntax, GenVM lint, ABI schema, and preflight. Direct Mode includes explicit artifact-failure, malformed-output, summary-injection, lifecycle/access-control, and `run_validator()` disagreement coverage.

- Contract freeze commit: `4f39e5b5ef023aceb13263269a75bfafee9a4138`.
- Contract: [0x4495e1A63062f7c522A26e7F2b494F72B8aDDee7](https://explorer-studio.genlayer.com/address/0x4495e1A63062f7c522A26e7F2b494F72B8aDDee7)
- Deployment transaction: [0x0812a35ba4bd5a113af536c34f38bedad2639fb74b66f8e6dd786ae2ae9ec312](https://explorer-studio.genlayer.com/tx/0x0812a35ba4bd5a113af536c34f38bedad2639fb74b66f8e6dd786ae2ae9ec312)
- Status: FINALIZED; GenVM SUCCESS.
- Constructor: no arguments (permissionless deployment).
- Source SHA-256: `8130be01c3ceccf2dbf9209b1f0149365e1f1a00ff27b0515275f4a3b84098c1`.
- `get_info()`: QuorumSeal v0.2.2, minimum confidence 75, maximum payload 24000 bytes.
- Deployed-source parity: VERIFIED through StudioNet `gen_getContractCode`. The returned source decoded to 8,853 bytes and matched `contracts/quorumseal.py` byte-for-byte.
- Freeze-commit GitHub Actions run [34052207874](https://github.com/Bibidee/quorumseal/actions/runs/34052207874) completed successfully.

## Live lifecycle

- Proposal: [0xa9e6bb1fc667a05709ceeacd974bd81b5f4c2a22fc06c72d0288e218a1a45ca9](https://explorer-studio.genlayer.com/tx/0xa9e6bb1fc667a05709ceeacd974bd81b5f4c2a22fc06c72d0288e218a1a45ca9); FINALIZED / MAJORITY_AGREE / GenVM SUCCESS; seal `QS-LIVE-V022-001` persisted as `pending` with exact URLs and SHA-256 commitments.
- Review: [0xc8928e6e4d6857d5196ef5309d07b3cb22b49a0476a4b4687ecf80e646927ee7](https://explorer-studio.genlayer.com/tx/0xc8928e6e4d6857d5196ef5309d07b3cb22b49a0476a4b4687ecf80e646927ee7); FINALIZED / MAJORITY_AGREE / GenVM SUCCESS; status `approved`, confidence 96.
- Review rationale: `Evidence explicitly authorizes the exact QuorumSeal v0.2.2 live verification ID in the payload.` This is model-produced, not a canonical fallback.
- Consumption: [0xa2ed5e6249eb3b95a18d4b2625a9263a7cf2b5b3f51a3f4be84cae4a5d53163b](https://explorer-studio.genlayer.com/tx/0xa2ed5e6249eb3b95a18d4b2625a9263a7cf2b5b3f51a3f4be84cae4a5d53163b); FINALIZED / MAJORITY_AGREE / GenVM SUCCESS; final state `consumed`.

The v0.2.1 deployment `0xCfE935A245CDC8963348B3CBb97dFb6b00bB80f9` and the v0.2.0 deployment remain historical evidence only.
