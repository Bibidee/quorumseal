# QuorumSeal design

QuorumSeal binds a payload and supporting evidence to exact raw-byte SHA-256 commitments. Validators independently fetch and verify both HTTPS artifacts before semantic interpretation. Artifact text is untrusted data; embedded instructions are never followed.

Approval requires payload_match=yes, evidence_support=yes, risk=no, and confidence >=75. Rationale is explanatory only. Valid outputs deriving the same decision are equivalent; malformed output or disagreement fails closed. Structured JSON from `exec_prompt` is accepted directly, with a compatibility parse for textual responses.

Lifecycle: `pending -> approved -> consumed`, `pending -> blocked`, or `pending -> cancelled`. Only the designated consumer can consume an approved seal. The contract holds no funds or escrow and does not replace downstream authorization.
