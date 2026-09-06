# Deployment

The v0.2.1 release gate passed: 11 helper/unit tests and 6 genuine Direct Mode contract tests (17 total), plus syntax, GenVM lint, ABI schema, and preflight.

- Contract freeze commit: `524db3f820aa3b47ed1cb469800990be382b41a7`.
- Contract: [0xCfE935A245CDC8963348B3CBb97dFb6b00bB80f9](https://explorer-studio.genlayer.com/address/0xCfE935A245CDC8963348B3CBb97dFb6b00bB80f9)
- Deployment transaction: [0x0a16af48d1b99ae811110f31a20f722429770156e22a03b9889b1a61732f58a0](https://explorer-studio.genlayer.com/tx/0x0a16af48d1b99ae811110f31a20f722429770156e22a03b9889b1a61732f58a0)
- Status: FINALIZED; GenVM SUCCESS.
- Constructor: no arguments (permissionless deployment).
- Source SHA-256: `a2723c637bbdbc5bbd054c4cb2bf57fd0d53e233a3746884a53e8c568de33601`.
- `get_info()`: QuorumSeal v0.2.1, minimum confidence 75, maximum payload 24000 bytes.
- Deployed-source parity: VERIFIED through StudioNet `gen_getContractCode`. The returned source decoded to 8,887 bytes and matched `contracts/quorumseal.py` byte-for-byte.
- Freeze-commit GitHub Actions run [34050038366](https://github.com/Bibidee/quorumseal/actions/runs/34050038366) completed successfully.

## Live lifecycle

- Proposal: [0x5803969ff872f399318e0f21b82df84850793731b95d4533beed1ec08b8a7a98](https://explorer-studio.genlayer.com/tx/0x5803969ff872f399318e0f21b82df84850793731b95d4533beed1ec08b8a7a98); seal `QS-LIVE-V021-001` persisted as `pending` with exact URLs and SHA-256 commitments.
- Review: [0x17d6d6a9dbcf6054914d2ae7b4964e4efbddf8ea4464b6a741e5c36741138fb0](https://explorer-studio.genlayer.com/tx/0x17d6d6a9dbcf6054914d2ae7b4964e4efbddf8ea4464b6a741e5c36741138fb0); FINALIZED / MAJORITY_AGREE / GenVM SUCCESS; status `approved`, confidence 100.
- Review rationale: `The evidence explicitly authorizes the exact payload specified.` This confirms the live result was model-produced rather than a canonical malformed-output fallback.
- Consumption: [0xfc90c4fce6b5f66cba9f42b8108c9666afe95bd9fc326477483050f8cc244939](https://explorer-studio.genlayer.com/tx/0xfc90c4fce6b5f66cba9f42b8108c9666afe95bd9fc326477483050f8cc244939); FINALIZED / MAJORITY_AGREE / GenVM SUCCESS; final state `consumed`.

The v0.2.0 deployment `0x7ad42e7f6f2A0f2C10402a55e5B158d0E320CAde` and its transaction `0x3c0d835a2104936dd5e8c37acdfcf09733b7eb56bc0ba1008a5a31d55e8e8dc5` remain historical evidence only.
