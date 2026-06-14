"""Test fix and install helpers."""
import sys
import os
_repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _repo_root not in sys.path:
    sys.path.insert(0, _repo_root)

import json
import pytest
from pathlib import Path
from troubleshooter import (
    install_module,
    install_from_requirements,
    fix_corrupted_json,
    get_docs_url,
    generate_bug_report,
    LAST_RESULTS,
)

def test_install_module_user_declines(monkeypatch):
    monkeypatch.setattr("troubleshooter.ask_yes_no", lambda *a, **k: False)
    assert install_module("fake_mod") is False

def test_install_module_user_accepts_success(monkeypatch):
    monkeypatch.setattr("troubleshooter.ask_yes_no", lambda *a, **k: True)
    monkeypatch.setattr("troubleshooter.run_cmd", lambda *a, **k: (True, "ok", ""))
    assert install_module("fake_mod") is True

def test_install_module_user_accepts_failure(monkeypatch):
    monkeypatch.setattr("troubleshooter.ask_yes_no", lambda *a, **k: True)
    monkeypatch.setattr("troubleshooter.run_cmd", lambda *a, **k: (False, "", "error"))
    assert install_module("fake_mod") is False

def test_install_from_requirements_no_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert install_from_requirements() is False

def test_install_from_requirements_success(tmp_path, monkeypatch):
    req = tmp_path / "requirements.txt"
    req.write_text("pytest\n")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("troubleshooter.ask_yes_no", lambda *a, **k: True)
    monkeypatch.setattr("troubleshooter.run_cmd", lambda *a, **k: (True, "ok", ""))
    assert install_from_requirements() is True

def test_fix_corrupted_json_user_declines(monkeypatch, tmp_path):
    monkeypatch.setattr("troubleshooter.ask_yes_no", lambda *a, **k: False)
    f = tmp_path / "bad.json"
    assert fix_corrupted_json(str(f)) is False

def test_fix_corrupted_json_user_accepts(monkeypatch, tmp_path):
    monkeypatch.setattr("troubleshooter.ask_yes_no", lambda *a, **k: True)
    f = tmp_path / "bad.json"
    assert fix_corrupted_json(str(f)) is True
    assert json.loads(f.read_text()) == {}

def test_get_docs_url_local_exists(tmp_path):
    f = tmp_path / "MANUAL.md"
    f.write_text("docs")
    url = get_docs_url(str(f), "https://online")
    assert url.startswith("file://")
    assert "MANUAL.md" in url

def test_get_docs_url_fallback_online(tmp_path):
    url = get_docs_url(str(tmp_path / "nope.md"), "https://online")
    assert url == "https://online"

def test_generate_bug_report_creates_file(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("builtins.input", lambda: "")
    results = {"python_version": True, "internet": False}
    filename = generate_bug_report(results)
    assert filename is not None
    path = tmp_path / filename
    assert path.exists()
    content = path.read_text()
    assert "ORBITON BUG REPORT" in content
    assert "python_version: PASS" in content
    assert "internet: FAIL" in content
    assert sys.platform in content or "OS:" in content

def test_generate_bug_report_empty_results_returns_none(monkeypatch, capsys):
    """Empty results dict now returns None with a helpful message."""
    monkeypatch.setattr("builtins.input", lambda: "")
    filename = generate_bug_report({})
    assert filename is None
    captured = capsys.readouterr()
    assert "No scan data available" in captured.out

def test_generate_bug_report_none_uses_last_results(tmp_path, monkeypatch):
    """generate_bug_report(None) falls back to LAST_RESULTS."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("builtins.input", lambda: "")
    LAST_RESULTS.clear()
    LAST_RESULTS.update({"test_key": True})
    filename = generate_bug_report(None)
    assert filename is not None
    path = tmp_path / filename
    assert path.exists()
    content = path.read_text()
    assert "test_key: PASS" in content
    LAST_RESULTS.clear()

def test_generate_bug_report_none_with_empty_last_results(monkeypatch, capsys):
    """generate_bug_report(None) with empty LAST_RESULTS returns None."""
    monkeypatch.setattr("builtins.input", lambda: "")
    LAST_RESULTS.clear()
    filename = generate_bug_report(None)
    assert filename is None
    captured = capsys.readouterr()
    assert "No scan data available" in captured.out
