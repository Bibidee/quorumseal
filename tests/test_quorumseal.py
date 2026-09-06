import importlib.util
import sys
import types
from pathlib import Path

spec = importlib.util.spec_from_file_location("quorumseal", Path("contracts/quorumseal.py"))
module = importlib.util.module_from_spec(spec)

def load():
    if "genlayer" not in sys.modules:
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

def test_malformed_outputs_never_consensus():
    m = load()
    assert not m.equivalent(analysis(risk="yes"), {"garbage": True})
    assert not m.equivalent({"garbage": True}, {"garbage": False})

def test_decision_fails_closed_for_unclear_and_low_confidence():
    m = load()
    assert m.decision(analysis(payload="unclear")) == m.BLOCKED
    assert m.decision(analysis(evidence="unclear")) == m.BLOCKED
    assert m.decision(analysis(confidence=74)) == m.BLOCKED

def test_validation_rejects_extra_missing_and_bad_fields():
    m = load()
    assert not m.valid({"payload_match": "yes"})
    bad = analysis(); bad["extra"] = True
    assert not m.valid(bad)
    assert not m.valid(analysis(confidence=True))
    assert not m.valid(analysis(risk="maybe"))

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
