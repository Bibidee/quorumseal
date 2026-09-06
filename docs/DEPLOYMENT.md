# Deployment

The v0.2.0 release gate passed: 10 helper/unit tests and 3 genuine Direct Mode contract tests (13 total), plus syntax, GenVM lint, ABI schema, and preflight.

- Contract: [0x7ad42e7f6f2A0f2C10402a55e5B158d0E320CAde](https://explorer-studio.genlayer.com/address/0x7ad42e7f6f2A0f2C10402a55e5B158d0E320CAde)
- Deployment transaction: [0x3c0d835a2104936dd5e8c37acdfcf09733b7eb56bc0ba1008a5a31d55e8e8dc5](https://explorer-studio.genlayer.com/tx/0x3c0d835a2104936dd5e8c37acdfcf09733b7eb56bc0ba1008a5a31d55e8e8dc5)
- Status: FINALIZED; GenVM SUCCESS.
- Constructor: no arguments (permissionless deployment).
- Source SHA-256: `f5193fb375cf27f16bfc8abc3535f660c2c9980cc49d49807348a43a991ee9c5`.
- `get_info()`: QuorumSeal v0.2.0, minimum confidence 75, maximum payload 24000 bytes.
- Deployed-source parity: VERIFIED through the StudioNet `gen_getContractCode` RPC method. The returned base64 source decoded to 7,674 bytes and matched `contracts/quorumseal.py` byte-for-byte; both SHA-256 digests are `f5193fb375cf27f16bfc8abc3535f660c2c9980cc49d49807348a43a991ee9c5`.
- GitHub Actions release gate run 34037930541 completed successfully for the pre-parity documentation HEAD.

Live semantic review, consumption, and blocked-path transactions are not claimed by this deployment record.
