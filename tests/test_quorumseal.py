import importlib.util
import sys
import types
import hashlib
from pathlib import Path

spec = importlib.util.spec_from_file_location("quorumseal", Path("contracts/quorumseal.py"))
module = importlib.util.module_from_spec(spec)

def load():
    injected = False
    if "genlayer" not in sys.modules:
        injected = True
        gl = types.SimpleNamespace()
        gl.Contract = type("Contract", (), {})
        gl.Event = type("Event", (), {})
        gl.public = types.SimpleNamespace(write=lambda f: f, view=lambda f: f)
        gl.vm = types.SimpleNamespace(UserError=Exception)
        fake = types.ModuleType("genlayer")
        fake.gl = gl
        fake.Address = type("Address", (), {"__init__": lambda self, value="": setattr(self, "as_hex", value)})
        fake.u256 = int
        fake.TreeMap = dict
        fake.allow_storage = lambda cls: cls
        sys.modules["genlayer"] = fake
    spec.loader.exec_module(module)
    if injected:
        sys.modules.pop("genlayer", None)
    return module

def analysis(payload="yes", evidence="yes", risk="no", confidence=90):
    return {"payload_match": payload, "evidence_support": evidence, "risk": risk, "confidence": confidence, "rationale": "bounded rationale"}

def test_approval_requires_complete_safe_tuple():
    m = load()
    assert m.decision(analysis()) == m.APPROVED
    assert m.decision(analysis(risk="yes")) == m.BLOCKED
    assert m.decision(analysis(confidence=74)) == m.BLOCKED

def test_equivalence_compares_valid_derived_decision():
    m = load()
    assert m.equivalent(analysis(confidence=75), analysis(confidence=99))
    assert m.equivalent(analysis(risk="yes"), analysis(payload="no"))
    assert not m.equivalent(analysis(), analysis(risk="yes"))

def test_malformed_outputs_normalize_to_safe_consensus():
    m = load()
    left = m.normalize_review({"garbage": True})
    right = m.normalize_review({"garbage": False})
    assert m.valid(left) and m.decision(left) == m.BLOCKED
    assert m.equivalent(left, right)
    assert not m.equivalent(left, analysis())

def test_decision_fails_closed_for_unclear_and_low_confidence():
    m = load()
    assert m.decision(analysis(payload="unclear")) == m.BLOCKED
    assert m.decision(analysis(evidence="unclear")) == m.BLOCKED
    assert m.decision(analysis(confidence=74)) == m.BLOCKED

def test_normalization_accepts_extra_and_rejects_missing_and_bad_fields():
    m = load()
    assert m.normalize_review({"payload_match": "yes"})["rationale"] == "malformed_model_output"
    bad = analysis(); bad["extra"] = True
    assert m.normalize_review(bad) == analysis()
    assert m.normalize_review(analysis(confidence=True))["rationale"] == "malformed_model_output"
    assert m.normalize_review(analysis(risk="maybe"))["rationale"] == "malformed_model_output"

def test_normalization_handles_case_whitespace_and_bounds():
    m = load()
    value = analysis(); value.update({"payload_match": " YES ", "evidence_support": "YES", "risk": " NO "})
    assert m.decision(m.normalize_review(value)) == m.APPROVED
    for bad in (None, analysis(confidence=-1), analysis(confidence=101), analysis(confidence=True)):
        assert m.decision(m.normalize_review(bad)) == m.BLOCKED

def test_hash_and_url_guards_are_strict():
    m = load()
    assert m.digest("0x" + "ab" * 32) == "0x" + "ab" * 32
    for value in ("0x00", "ab" * 32, "0x" + "zz" * 32):
        try: m.digest(value)
        except Exception: pass
        else: assert False
    assert m.url("https://example.com/evidence")
    for value in ("http://example.com", "https://localhost/x", "https://127.0.0.1/x", "https://user:pass@example.com/x"):
        try: m.url(value)
        except Exception: pass
        else: assert False

def test_approved_outputs_with_different_rationales_remain_equivalent():
    m = load()
    left, right = analysis(confidence=75), analysis(confidence=100)
    right["rationale"] = "different bounded explanation"
    assert m.equivalent(left, right)

def test_fetch_verified_hashes_raw_bytes_and_decodes_utf8():
    m = load(); raw = b"payload bytes"
    m.gl.nondet = types.SimpleNamespace(web=types.SimpleNamespace(get=lambda _: types.SimpleNamespace(status=200, body=raw)))
    assert m.fetch_verified("https://example.com/p", "0x" + hashlib.sha256(raw).hexdigest()) == "payload bytes"

def test_fetch_verified_rejects_hash_mismatch_and_http_failure():
    m = load(); raw = b"payload bytes"
    m.gl.nondet = types.SimpleNamespace(web=types.SimpleNamespace(get=lambda _: types.SimpleNamespace(status=404, body=raw)))
    try: m.fetch_verified("https://example.com/p", "0x" + hashlib.sha256(raw).hexdigest())
    except ValueError: pass
    else: assert False
    m.gl.nondet = types.SimpleNamespace(web=types.SimpleNamespace(get=lambda _: types.SimpleNamespace(status=200, body=raw)))
    try: m.fetch_verified("https://example.com/p", "0x" + "00" * 32)
    except ValueError: pass
    else: assert False

def test_fetch_verified_rejects_empty_and_non_utf8():
    m = load()
    m.gl.nondet = types.SimpleNamespace(web=types.SimpleNamespace(get=lambda _: types.SimpleNamespace(status=200, body=b"")))
    try: m.fetch_verified("https://example.com/p", "0x" + "00" * 32)
    except ValueError: pass
    else: assert False
    raw = b"\xff\xfe"
    m.gl.nondet = types.SimpleNamespace(web=types.SimpleNamespace(get=lambda _: types.SimpleNamespace(status=200, body=raw)))
    try: m.fetch_verified("https://example.com/p", "0x" + hashlib.sha256(raw).hexdigest())
    except ValueError: pass
    else: assert False
