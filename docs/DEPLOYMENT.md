# Deployment

The v0.2.4 release gate passed: 12 helper/unit tests and 40 genuine Direct Mode contract tests (52 total), plus syntax, GenVM lint, ABI schema, and preflight. Direct Mode includes explicit artifact-failure, malformed-output, URL-literal-bypass, summary-injection, lifecycle/access-control, and `run_validator()` disagreement coverage.

- Contract freeze commit: `5334ffae39555ef2565a9482c65071fa6a4de38c`.
- Contract: [0x57f05489B4C9BE96A5bCee43D977a21F18f5B499](https://explorer-studio.genlayer.com/address/0x57f05489B4C9BE96A5bCee43D977a21F18f5B499)
- Deployment transaction: [0x94f45f519572a5fb9cf1d5b3820c1a475c48cee1dab368eb6e5737b7dc924039](https://explorer-studio.genlayer.com/tx/0x94f45f519572a5fb9cf1d5b3820c1a475c48cee1dab368eb6e5737b7dc924039)
- Status: FINALIZED; GenVM SUCCESS.
- Constructor: no arguments (permissionless deployment).
- Source SHA-256: `6323d2936ad078e89af3f2ffcc1fe629f41c9042d9af40d5aa9c3c5db5dc6f90`.
- `get_info()`: QuorumSeal v0.2.4, minimum confidence 75, maximum payload 24000 bytes.
- Deployed-source parity: VERIFIED through StudioNet `gen_getContractCode`. The returned source decoded to 10,007 bytes and matched `contracts/quorumseal.py` byte-for-byte.
- Frozen-source GitHub Actions run [34099852220](https://github.com/Bibidee/quorumseal/actions/runs/34099852220) completed successfully.

## Live lifecycle

- Proposal: [0x014e2c3ec76b24f9a5e9485776eca9f9d12d6d745b9484cedc85708cd3a45f8b](https://explorer-studio.genlayer.com/tx/0x014e2c3ec76b24f9a5e9485776eca9f9d12d6d745b9484cedc85708cd3a45f8b); FINALIZED / MAJORITY_AGREE / GenVM SUCCESS; seal `QS-LIVE-V024-FINAL` persisted as `pending` with exact URLs and SHA-256 commitments.
- Review: [0x8166dde57fa962dcb6ffc5ef75461ff56b7ef7180e08adc8c8b034e4bdd79347](https://explorer-studio.genlayer.com/tx/0x8166dde57fa962dcb6ffc5ef75461ff56b7ef7180e08adc8c8b034e4bdd79347); FINALIZED / MAJORITY_AGREE / GenVM SUCCESS; status `approved`, confidence 90.
- Review rationale: model-produced rationale after exact raw-byte payload/evidence verification; rationale text is diagnostic and not consensus-critical.
- Consumption: [0x2621c6203d0770df418a06e1bbfe8548d9be01b2b2cd2d7cd565be30b0249377](https://explorer-studio.genlayer.com/tx/0x2621c6203d0770df418a06e1bbfe8548d9be01b2b2cd2d7cd565be30b0249377); FINALIZED / MAJORITY_AGREE / GenVM SUCCESS; final state `consumed`.

The v0.2.3 deployment `0xD944F22d201a472Db68ae408508115DB1f6851A6` (tx `0x54bf3761fb0e0936204b840a27f5d4b70349f1c9ea405db2ac491273c279aa58`), prior internal-metadata deployment `0x4495e1A63062f7c522A26e7F2b494F72B8aDDee7` (tx `0x0812a35ba4bd5a113af536c34f38bedad2639fb74b66f8e6dd786ae2ae9ec312`), v0.2.1, and v0.2.0 deployments remain historical/superseded evidence only.
