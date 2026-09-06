# QuorumSeal design

QuorumSeal binds a payload and supporting evidence to exact raw-byte SHA-256 commitments. Validators independently fetch and verify both HTTPS artifacts before semantic interpretation. Artifact text is untrusted data; embedded instructions are never followed.

Approval requires payload_match=yes, evidence_support=yes, risk=no, and confidence >=75. Rationale is explanatory only. Required model fields are normalized into a bounded tuple; extra keys are ignored. Missing, malformed, unavailable, or invalid observations become a canonical valid BLOCKED tuple. Validators compare only the derived authorization result, so BLOCKED reasons may differ while any APPROVED/BLOCKED disagreement still rejects consensus.

Lifecycle: `pending -> approved -> consumed`, `pending -> blocked`, or `pending -> cancelled`. Only the designated consumer can consume an approved seal. The contract holds no funds or escrow and does not replace downstream authorization.
