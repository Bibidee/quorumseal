# QuorumSeal

QuorumSeal is a reusable GenLayer Intelligent Contract primitive for approving hash-bound documents, releases, policy changes, and governance actions.

The contract will separate deterministic authorization, commitments, timing, and accounting from nondeterministic semantic review. Validators will independently inspect committed artifacts, derive a bounded approval decision, and fail closed on disagreement, malformed output, unavailable evidence, or hash mismatch.

The package intentionally keeps exactly one deployable contract source under `contracts/`. Tests live outside that directory so test-only imports cannot become GenVM lint candidates.
