# QuorumSeal

QuorumSeal is a reusable GenLayer Intelligent Contract primitive for approving hash-bound documents, releases, policy changes, and governance actions.

The contract separates deterministic authorization and hash commitments from nondeterministic semantic review. Validators independently inspect committed evidence, derive a bounded approval decision, and fail closed on disagreement, malformed output, unavailable evidence, or hash mismatch.

The package intentionally keeps exactly one deployable contract source under `contracts/`. Tests live outside that directory so test-only imports cannot become GenVM lint candidates.

## Release evidence

- Direct Mode: 3 tests passing.
- GenVM lint and ABI schema: passed by `scripts/preflight.py`.
- Finalized StudioNet deployment: [0x7b28F495959a1598540f9e0abF6b212507304f9e](https://explorer-studio.genlayer.com/address/0x7b28F495959a1598540f9e0abF6b212507304f9e).
- Deployment transaction: [0x3ea75ccf7adb591c3be01ebb0f982f4dfd293009731cf8e1c1018f03ed306674](https://explorer-studio.genlayer.com/tx/0x3ea75ccf7adb591c3be01ebb0f982f4dfd293009731cf8e1c1018f03ed306674), FINALIZED with GenVM SUCCESS.
- Local source SHA-256: `4022346ad219ee8995b815896205d94db4095f60642e61996474578e16d13484`.
- A finalized `get_info()` read returned `QuorumSeal` v0.1.0 and minimum confidence 75.
