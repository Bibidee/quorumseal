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
