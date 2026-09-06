import hashlib
import json
import os

import pytest
from gltest.direct import sdk_loader

# Pin Direct Mode to the supported runtime release; GitHub's latest release
# currently points at an unavailable prerelease artifact.
sdk_loader.get_latest_version = lambda: "v0.2.12"


@pytest.fixture(autouse=True)
def windows_tempfile_cleanup(monkeypatch):
    # gltest 0.29.2 closes the temporary fd asynchronously on Windows.
    # Preserve the official fixture path while making cleanup retry-safe.
    unlink = os.unlink
    def safe_unlink(path, *args, **kwargs):
        try:
            unlink(path, *args, **kwargs)
        except PermissionError:
            pass
    monkeypatch.setattr(os, "unlink", safe_unlink)


PAYLOAD = b"Authorize QuorumSeal release QS-TEST-001."
EVIDENCE = b"Evidence QS-TEST-001 supports the exact authorized release."
PAYLOAD_HASH = "0x" + hashlib.sha256(PAYLOAD).hexdigest()
EVIDENCE_HASH = "0x" + hashlib.sha256(EVIDENCE).hexdigest()
PAYLOAD_URL = "https://payload.example/qs-001"
EVIDENCE_URL = "https://evidence.example/qs-001"


def _configure(vm, result):
    vm.mock_web(PAYLOAD_URL, {"status": 200, "body": PAYLOAD})
    vm.mock_web(EVIDENCE_URL, {"status": 200, "body": EVIDENCE})
    vm.mock_llm("QS-TEST-001", json.dumps(result))


@pytest.mark.direct
def test_real_direct_propose_read_and_consume(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = direct_deploy("contracts/quorumseal.py")
    direct_vm.sender = direct_alice
    contract.propose("QS-TEST-001", direct_bob, PAYLOAD_URL, PAYLOAD_HASH, EVIDENCE_URL, EVIDENCE_HASH, "bounded summary")
    assert contract.get_seal("QS-TEST-001")["status"] == "pending"
    _configure(direct_vm, {"payload_match": "yes", "evidence_support": "yes", "risk": "no", "confidence": 90, "rationale": "supported"})
    contract.review("QS-TEST-001")
    assert contract.get_seal("QS-TEST-001")["status"] == "approved"
    direct_vm.sender = direct_bob
    contract.consume("QS-TEST-001")
    assert contract.get_seal("QS-TEST-001")["status"] == "consumed"


@pytest.mark.direct
def test_real_direct_cancel_only_pending(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = direct_deploy("contracts/quorumseal.py")
    direct_vm.sender = direct_alice
    contract.propose("QS-CANCEL", direct_bob, PAYLOAD_URL, PAYLOAD_HASH, EVIDENCE_URL, EVIDENCE_HASH, "summary")
    contract.cancel("QS-CANCEL")
    assert contract.get_seal("QS-CANCEL")["status"] == "cancelled"


@pytest.mark.direct
def test_real_direct_input_guards(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = direct_deploy("contracts/quorumseal.py")
    direct_vm.sender = direct_alice
    with direct_vm.expect_revert():
        contract.propose("bad id!", direct_bob, PAYLOAD_URL, PAYLOAD_HASH, EVIDENCE_URL, EVIDENCE_HASH, "summary")
    with direct_vm.expect_revert():
        contract.propose("zero", bytes(20), PAYLOAD_URL, PAYLOAD_HASH, EVIDENCE_URL, EVIDENCE_HASH, "summary")
    with direct_vm.expect_revert():
        contract.propose("long", direct_bob, PAYLOAD_URL, PAYLOAD_HASH, EVIDENCE_URL, EVIDENCE_HASH, "x" * 401)


@pytest.mark.direct
def test_real_direct_summary_boundary_and_duplicate(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = direct_deploy("contracts/quorumseal.py")
    direct_vm.sender = direct_alice
    exact = "x" * 400
    contract.propose("QS-BOUNDARY", direct_bob, PAYLOAD_URL, PAYLOAD_HASH, EVIDENCE_URL, EVIDENCE_HASH, exact)
    assert contract.get_seal("QS-BOUNDARY")["summary"] == exact
    with direct_vm.expect_revert():
        contract.propose("QS-BOUNDARY", direct_bob, PAYLOAD_URL, PAYLOAD_HASH, EVIDENCE_URL, EVIDENCE_HASH, "duplicate")
    with direct_vm.expect_revert():
        contract.propose("QS-BLANK", direct_bob, PAYLOAD_URL, PAYLOAD_HASH, EVIDENCE_URL, EVIDENCE_HASH, " \t ")


@pytest.mark.direct
def test_real_direct_access_and_terminal_state_guards(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = direct_deploy("contracts/quorumseal.py")
    direct_vm.sender = direct_alice
    contract.propose("QS-ACCESS", direct_bob, PAYLOAD_URL, PAYLOAD_HASH, EVIDENCE_URL, EVIDENCE_HASH, "summary")
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert():
        contract.cancel("QS-ACCESS")
    direct_vm.sender = direct_alice
    _configure(direct_vm, {"payload_match": "yes", "evidence_support": "yes", "risk": "no", "confidence": 90, "rationale": "supported"})
    contract.review("QS-ACCESS")
    with direct_vm.expect_revert():
        contract.cancel("QS-ACCESS")
    direct_vm.sender = direct_alice
    with direct_vm.expect_revert():
        contract.consume("QS-ACCESS")
    direct_vm.sender = direct_bob
    contract.consume("QS-ACCESS")
    with direct_vm.expect_revert():
        contract.consume("QS-ACCESS")


@pytest.mark.direct
def test_real_direct_blocked_review_is_terminal(direct_vm, direct_deploy, direct_alice, direct_bob):
    contract = direct_deploy("contracts/quorumseal.py")
    direct_vm.sender = direct_alice
    contract.propose("QS-BLOCKED", direct_bob, PAYLOAD_URL, PAYLOAD_HASH, EVIDENCE_URL, EVIDENCE_HASH, "summary")
    _configure(direct_vm, {"payload_match": "yes", "evidence_support": "yes", "risk": "yes", "confidence": 90, "rationale": "material risk"})
    contract.review("QS-BLOCKED")
    assert contract.get_seal("QS-BLOCKED")["status"] == "blocked"
    with direct_vm.expect_revert():
        contract.review("QS-BLOCKED")
    with direct_vm.expect_revert():
        contract.consume("QS-BLOCKED")
    with direct_vm.expect_revert():
        contract.cancel("QS-BLOCKED")
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert():
        contract.consume("QS-BLOCKED")
