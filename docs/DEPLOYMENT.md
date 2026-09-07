# Deployment

The v0.2.3 release gate passed: 12 helper/unit tests and 34 genuine Direct Mode contract tests (46 total), plus syntax, GenVM lint, ABI schema, and preflight. Direct Mode includes explicit artifact-failure, malformed-output, summary-injection, lifecycle/access-control, and `run_validator()` disagreement coverage.

- Contract freeze commit: `ae58e66fdb4442f5154c709b8e694e7b5c4738c3`.
- Contract: [0xD944F22d201a472Db68ae408508115DB1f6851A6](https://explorer-studio.genlayer.com/address/0xD944F22d201a472Db68ae408508115DB1f6851A6)
- Deployment transaction: [0x54bf3761fb0e0936204b840a27f5d4b70349f1c9ea405db2ac491273c279aa58](https://explorer-studio.genlayer.com/tx/0x54bf3761fb0e0936204b840a27f5d4b70349f1c9ea405db2ac491273c279aa58)
- Status: FINALIZED; GenVM SUCCESS.
- Constructor: no arguments (permissionless deployment).
- Source SHA-256: `98588934c90e834450779f1a60c8b0a12bbc1a2a93e021a239616e34fe61f0a3`.
- `get_info()`: QuorumSeal v0.2.3, minimum confidence 75, maximum payload 24000 bytes.
- Deployed-source parity: VERIFIED through StudioNet `gen_getContractCode`. The returned source decoded to 9,949 bytes and matched `contracts/quorumseal.py` byte-for-byte.
- Final-head GitHub Actions run [34089315537](https://github.com/Bibidee/quorumseal/actions/runs/34089315537) completed successfully.

## Live lifecycle

- Proposal: [0xc884ed732ac621370e1f5debec41cd29a68cc0500f771e5d92c5a91e801afa24](https://explorer-studio.genlayer.com/tx/0xc884ed732ac621370e1f5debec41cd29a68cc0500f771e5d92c5a91e801afa24); FINALIZED / MAJORITY_AGREE / GenVM SUCCESS; seal `QS-LIVE-V023-FINAL` persisted as `pending` with exact URLs and SHA-256 commitments.
- Review: [0xf6bb8c04c1ed99d471490a4fecc6a989ae93ae7536131a00499aa0cb46b87b50](https://explorer-studio.genlayer.com/tx/0xf6bb8c04c1ed99d471490a4fecc6a989ae93ae7536131a00499aa0cb46b87b50); FINALIZED / MAJORITY_AGREE / GenVM SUCCESS; status `approved`, confidence 85.
- Review rationale: model-produced rationale after exact raw-byte payload/evidence verification; rationale text is diagnostic and not consensus-critical.
- Consumption: [0x05402db29eef31667614ab685e5e1ea983417c8563079c1cb312de698c4248b4](https://explorer-studio.genlayer.com/tx/0x05402db29eef31667614ab685e5e1ea983417c8563079c1cb312de698c4248b4); FINALIZED / MAJORITY_AGREE / GenVM SUCCESS; final state `consumed`.

The prior v0.2.3-internal-metadata deployment `0x4495e1A63062f7c522A26e7F2b494F72B8aDDee7` (tx `0x0812a35ba4bd5a113af536c34f38bedad2639fb74b66f8e6dd786ae2ae9ec312`), the v0.2.1 deployment `0xCfE935A245CDC8963348B3CBb97dFb6b00bB80f9`, and the v0.2.0 deployment remain historical/superseded evidence only.
