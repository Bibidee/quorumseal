# QuorumSeal design

QuorumSeal binds a payload and supporting evidence to exact raw-byte SHA-256 commitments. Validators independently fetch and verify both HTTPS artifacts before semantic interpretation. Artifact text is untrusted data; embedded instructions are never followed. The proposer summary is stored only as display metadata and is excluded from the semantic-review snapshot and prompt, so it cannot influence authorization.

Approval requires payload_match=yes, evidence_support=yes, risk=no, and confidence >=75. Rationale is explanatory only. Required model fields are normalized into a bounded tuple; extra keys are ignored. Missing, malformed, unavailable, or invalid observations become a canonical valid BLOCKED tuple. Validators require agreement on authorization outcome, not free-form rationale, so BLOCKED reasons may differ while any APPROVED/BLOCKED disagreement still rejects consensus.

Lifecycle: `pending -> approved -> consumed`, `pending -> blocked`, or `pending -> cancelled`. Only the designated consumer can consume an approved seal. The contract holds no funds or escrow and does not replace downstream authorization.

Validators require agreement on the final authorization outcome, not identical rationale. This is safe because disagreement about why a seal is blocked still fails closed; an approval can only be agreed when each validator independently derives the complete approved tuple (payload match yes, evidence support yes, risk no, confidence at least 75). Rationale remains explanatory and is never authorization-critical.

URLs must use HTTPS and reject userinfo, localhost/local names, private or special-use IPv4 ranges, and loopback, unique-local, link-local, unspecified, or multicast IPv6 literals. This is a bounded admission guard rather than a DNS oracle; downstream systems should still apply their own network policy.
