# Deployment

The v0.2.5 release gate passed: 12 helper/unit tests and 43 genuine Direct Mode contract tests (55 total), plus syntax, GenVM lint, ABI schema, and preflight. Direct Mode includes explicit artifact-failure, malformed-output, URL-number-form-bypass, summary-injection, lifecycle/access-control, and validator-disagreement coverage.

- Contract freeze commit: `424c5b9382fe15766540e542fb769b50b6efe04f`.
- Contract: [0xdEF0De3EbDB187301A95972E8e2e27999dE5aFf2](https://explorer-studio.genlayer.com/address/0xdEF0De3EbDB187301A95972E8e2e27999dE5aFf2)
- Deployment transaction: [0xfabced18096383e5ca57af550e592d641bdc1510b4c5eff10868197c5bb9a3ba](https://explorer-studio.genlayer.com/tx/0xfabced18096383e5ca57af550e592d641bdc1510b4c5eff10868197c5bb9a3ba)
- Status: FINALIZED; GenVM SUCCESS.
- Constructor: no arguments (permissionless deployment).
- Source SHA-256: `9d8bcea60ac7a2955b15f504ae44171bab3d674de005db57881727cd10b6c399`.
- `get_info()`: QuorumSeal v0.2.5, minimum confidence 75, maximum payload 24000 bytes.
- Deployed-source parity: VERIFIED through StudioNet `gen_getContractCode`. The returned source decoded to 10,252 bytes and matched `contracts/quorumseal.py` byte-for-byte.
- Frozen-source GitHub Actions run [34105136989](https://github.com/Bibidee/quorumseal/actions/runs/34105136989) completed successfully.

## Live lifecycle

- Proposal: [0xd6ac8d85e64e72fa9885c140eec78d691c1c683ada302446d9efff31ec84556c](https://explorer-studio.genlayer.com/tx/0xd6ac8d85e64e72fa9885c140eec78d691c1c683ada302446d9efff31ec84556c); FINALIZED / MAJORITY_AGREE / GenVM SUCCESS; seal `QS-LIVE-V025-FINAL` persisted as `pending` with exact URLs and SHA-256 commitments.
- Review: [0x0c139601719d0f206680b9ccbe0295d0413d3eff320b1e570467b55badc5fe43](https://explorer-studio.genlayer.com/tx/0x0c139601719d0f206680b9ccbe0295d0413d3eff320b1e570467b55badc5fe43); FINALIZED / MAJORITY_AGREE / GenVM SUCCESS; status `approved`, confidence 100.
- Review rationale: model-produced rationale after exact raw-byte payload/evidence verification; rationale text is diagnostic and not consensus-critical.
- Consumption: [0xf10bad8244707fe9943fa199554402d16c0e0770c905b3a527b79701d2115151](https://explorer-studio.genlayer.com/tx/0xf10bad8244707fe9943fa199554402d16c0e0770c905b3a527b79701d2115151); FINALIZED / MAJORITY_AGREE / GenVM SUCCESS; final state `consumed`.

The v0.2.4 deployment [0x57f05489B4C9BE96A5bCee43D977a21F18f5B499](https://explorer-studio.genlayer.com/address/0x57f05489B4C9BE96A5bCee43D977a21F18f5B499) (tx [0x94f45f519572a5fb9cf1d5b3820c1a475c48cee1dab368eb6e5737b7dc924039](https://explorer-studio.genlayer.com/tx/0x94f45f519572a5fb9cf1d5b3820c1a475c48cee1dab368eb6e5737b7dc924039)) and its v0.2.4 live evidence are historical/superseded by v0.2.5. The v0.2.3 deployment `0xD944F22d201a472Db68ae408508115DB1f6851A6` (tx `0x54bf3761fb0e0936204b840a27f5d4b70349f1c9ea405db2ac491273c279aa58`), prior internal-metadata deployment `0x4495e1A63062f7c522A26e7F2b494F72B8aDDee7` (tx `0x0812a35ba4bd5a113af536c34f38bedad2639fb74b66f8e6dd786ae2ae9ec312`), v0.2.1, and v0.2.0 deployments remain historical/superseded evidence only.
