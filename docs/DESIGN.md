# QuorumSeal design

QuorumSeal commits an action payload, baseline, and evidence by SHA-256 of exact raw bytes. Validators verify those commitments before semantic interpretation. The contract derives the final decision deterministically from a strict structured result; rationale is explanatory only.

Approval is fail-closed: malformed output, unavailable artifacts, hash mismatch, or validator disagreement never authorizes an action. Every held bond and escrow balance has a bounded settlement or refund route.
