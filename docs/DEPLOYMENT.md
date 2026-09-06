# Deployment

## StudioNet deployment

The release gate passed before deployment: Direct Mode 3/3, Python syntax, GenVM lint, ABI schema generation, and preflight all passed. The finalized deployment is:

- Contract: [0x7b28F495959a1598540f9e0abF6b212507304f9e](https://explorer-studio.genlayer.com/address/0x7b28F495959a1598540f9e0abF6b212507304f9e)
- Deployment transaction: [0x3ea75ccf7adb591c3be01ebb0f982f4dfd293009731cf8e1c1018f03ed306674](https://explorer-studio.genlayer.com/tx/0x3ea75ccf7adb591c3be01ebb0f982f4dfd293009731cf8e1c1018f03ed306674)
- Status: FINALIZED; leader GenVM result SUCCESS.
- Constructor owner: `0x79b3ecbe6a65bee93b2fcda78e6909892671507f`.
- Local source SHA-256: `4022346ad219ee8995b815896205d94db4095f60642e61996474578e16d13484`.

The Explorer source should be retrieved and compared byte-for-byte against `contracts/quorumseal.py` before external submission. The first deployment attempt used an incorrectly typed constructor argument and was rejected; it is not the release deployment. A finalized `get_info()` read from the release address returned `QuorumSeal` v0.1.0.
