# v0.1.0
# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
"""QuorumSeal: hash-bound semantic approval for reusable change commitments."""
import hashlib
import json
import re
from dataclasses import dataclass
from genlayer import *

PENDING, REVIEWED, APPROVED, BLOCKED, CONSUMED, CANCELLED = "pending", "reviewed", "approved", "blocked", "consumed", "cancelled"
MAX_ID, MAX_TEXT, MAX_URL, MAX_BYTES = 96, 400, 512, 12000
MIN_CONFIDENCE = 75

@allow_storage
@dataclass
class Seal:
    id: str
    proposer: Address
    consumer: Address
    payload_hash: str
    evidence_url: str
    evidence_hash: str
    summary: str
    status: str
    confidence: u256
    rationale: str
    created_at: u256
    reviewed_at: u256

class SealReviewed(gl.Event):
    def __init__(self, seal_id: str, status: str, /, **blob): ...

def clean(value): return " ".join(str(value).replace("\x00", " ").split())

def ident(value):
    result = str(value).strip()
    if not result or len(result) > MAX_ID or not re.match(r"^[A-Za-z0-9_.:-]+$", result): raise gl.vm.UserError("[EXPECTED] Invalid seal id")
    return result

def digest(value):
    result = str(value).strip().lower()
    if not re.match(r"^0x[0-9a-f]{64}$", result): raise gl.vm.UserError("[EXPECTED] Invalid SHA-256")
    return result

def url(value):
    result = str(value).strip()
    if len(result) > MAX_URL or not result.startswith("https://") or "@" in result or "localhost" in result or result.startswith("https://127.") or result.startswith("https://169.254."):
        raise gl.vm.UserError("[EXPECTED] Invalid evidence URL")
    return result

def valid(value):
    if not isinstance(value, dict) or set(value.keys()) != {"payload_match", "evidence_support", "risk", "confidence", "rationale"}: return False
    if any(value.get(k) not in ("yes", "no", "unclear") for k in ("payload_match", "evidence_support", "risk")): return False
    return isinstance(value.get("confidence"), int) and not isinstance(value.get("confidence"), bool) and 0 <= value["confidence"] <= 100 and bool(clean(value.get("rationale", ""))) and len(clean(value["rationale"])) <= MAX_TEXT

def decision(value):
    if not valid(value): return BLOCKED
    if value["payload_match"] == "yes" and value["evidence_support"] == "yes" and value["risk"] == "no" and value["confidence"] >= MIN_CONFIDENCE: return APPROVED
    return BLOCKED

def equivalent(left, right):
    return valid(left) and valid(right) and decision(left) == decision(right)

def fetch_verified(target, expected):
    try: response = gl.nondet.web.get(target)
    except Exception: raise ValueError("unavailable")
    raw = response.body
    if response.status < 200 or response.status >= 300 or not raw or len(raw) > MAX_BYTES: raise ValueError("http_or_empty")
    if "0x" + hashlib.sha256(raw).hexdigest() != expected: raise ValueError("hash_mismatch")
    try: return raw.decode("utf-8")
    except UnicodeDecodeError: raise ValueError("invalid_utf8")

def observe(seal):
    return {"error": "unused"}

def semantic_review(seal):
    try:
        evidence = fetch_verified(str(seal.evidence_url), str(seal.evidence_hash))
        prompt = "Review this committed action and return strict JSON with payload_match,evidence_support,risk,confidence,rationale. " + json.dumps({"payload_hash": seal.payload_hash, "evidence_hash": seal.evidence_hash, "summary": seal.summary, "evidence": evidence}, sort_keys=True, separators=(",", ":"))
        value = json.loads(gl.nondet.exec_prompt(prompt, response_format="json"))
        return value if valid(value) else {"error": "malformed"}
    except Exception:
        return {"error": "observation_error"}

class QuorumSeal(gl.Contract):
    seals: TreeMap[str, Seal]

    def __init__(self, owner: Address):
        if owner.as_hex.lower() == "0x" + "0" * 40: raise gl.vm.UserError("[EXPECTED] Zero owner")
        self.owner = owner

    @gl.public.write
    def propose(self, seal_id: str, consumer: Address, payload_hash: str, evidence_url: str, evidence_hash: str, summary: str):
        seal_id, payload_hash, evidence_url, evidence_hash = ident(seal_id), digest(payload_hash), url(evidence_url), digest(evidence_hash)
        if consumer.as_hex.lower() == "0x" + "0" * 40 or not clean(summary): raise gl.vm.UserError("[EXPECTED] Invalid proposal")
        if seal_id in self.seals: raise gl.vm.UserError("[EXPECTED] Duplicate seal")
        self.seals[seal_id] = Seal(seal_id, gl.message.sender_address, consumer, payload_hash, evidence_url, evidence_hash, clean(summary), PENDING, u256(0), "", u256(0), u256(0))

    @gl.public.write
    def review(self, seal_id: str):
        seal = self.seals.get(ident(seal_id))
        if seal is None or seal.status != PENDING: raise gl.vm.UserError("[EXPECTED] Not reviewable")
        def leader(): return semantic_review(seal)
        def validator(leader_result):
            if not isinstance(leader_result, gl.vm.Return) or not isinstance(leader_result.calldata, dict): return False
            right = semantic_review(seal)
            return equivalent(leader_result.calldata, right)
        parsed = gl.vm.run_nondet_unsafe(leader, validator)
        seal.status = decision(parsed)
        seal.confidence = u256(parsed.get("confidence", 0)) if valid(parsed) else u256(0)
        seal.rationale = clean(parsed.get("rationale", "")) if valid(parsed) else ""
        SealReviewed(seal.id, seal.status)

    @gl.public.write
    def consume(self, seal_id: str):
        seal = self.seals.get(ident(seal_id))
        if seal is None or seal.status != APPROVED: raise gl.vm.UserError("[EXPECTED] Seal not approved")
        if gl.message.sender_address != seal.consumer: raise gl.vm.UserError("[EXPECTED] Consumer only")
        seal.status = CONSUMED

    @gl.public.write
    def cancel(self, seal_id: str):
        seal = self.seals.get(ident(seal_id))
        if seal is None or gl.message.sender_address != seal.proposer or seal.status in (CONSUMED, CANCELLED): raise gl.vm.UserError("[EXPECTED] Cannot cancel")
        seal.status = CANCELLED

    @gl.public.view
    def get_seal(self, seal_id: str):
        seal = self.seals.get(ident(seal_id))
        if seal is None: raise gl.vm.UserError("[EXPECTED] Seal not found")
        return {"id": seal.id, "proposer": seal.proposer.as_hex, "consumer": seal.consumer.as_hex, "payload_hash": seal.payload_hash, "evidence_url": seal.evidence_url, "evidence_hash": seal.evidence_hash, "summary": seal.summary, "status": seal.status, "confidence": str(seal.confidence), "rationale": seal.rationale}

    @gl.public.view
    def get_info(self): return {"name": "QuorumSeal", "version": "0.1.0", "min_confidence": str(MIN_CONFIDENCE)}
