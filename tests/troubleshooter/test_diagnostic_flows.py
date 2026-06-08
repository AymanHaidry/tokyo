"""Test diagnostic flow functions."""
import pytest
from troubleshooter import (
    flow_wont_start,
    flow_voice_not_working,
    flow_tts_silent,
    flow_commands_wrong,
    flow_files_projects,
    flow_slow_laggy,
    flow_install_update,
)


def test_flow_wont_start_returns_dict(monkeypatch):
    monkeypatch.setattr("troubleshooter.ask_yes_no", lambda *a, **k: False)
    monkeypatch.setattr("troubleshooter.check_file_exists", lambda *a, **k: True)
    monkeypatch.setattr("troubleshooter.check_module", lambda *a, **k: True)
    monkeypatch.setattr("troubleshooter.run_cmd", lambda *a, **k: (True, "ok", ""))
    results = flow_wont_start()
    assert isinstance(results, dict)
    assert "python_version" in results


def test_flow_wont_start_detects_bad_python(monkeypatch):
    monkeypatch.setattr("troubleshooter.ask_yes_no", lambda *a, **k: False)
    monkeypatch.setattr("troubleshooter.check_python_version", lambda: (False, "3.8.0"))
    results = flow_wont_start()
    assert results["python_version"] is False


def test_flow_wont_start_detects_missing_repo(monkeypatch):
    monkeypatch.setattr("troubleshooter.ask_yes_no", lambda *a, **k: False)
    monkeypatch.setattr("troubleshooter.check_python_version", lambda: (True, "3.11.0"))
    monkeypatch.setattr("troubleshooter.check_file_exists", lambda *a, **k: False)
    results = flow_wont_start()
    assert results["in_repo"] is False


def test_flow_voice_not_working_returns_dict(monkeypatch):
    monkeypatch.setattr("troubleshooter.ask_yes_no", lambda *a, **k: True)
    monkeypatch.setattr("troubleshooter.check_microphone_os", lambda: True)
    monkeypatch.setattr("troubleshooter.check_mic_permissions", lambda: True)
    monkeypatch.setattr("troubleshooter.check_pyaudio", lambda: True)
    monkeypatch.setattr("troubleshooter.check_internet", lambda: True)
    results = flow_voice_not_working()
    assert isinstance(results, dict)
    assert results["typing_works"] is True


def test_flow_voice_not_working_typing_fails_short_circuits(monkeypatch):
    monkeypatch.setattr("troubleshooter.ask_yes_no", lambda *a, **k: False)
    results = flow_voice_not_working()
    assert results["typing_works"] is False


def test_flow_voice_not_working_detects_self_listening(monkeypatch):
    inputs = iter([True, True])
    monkeypatch.setattr("troubleshooter.ask_yes_no", lambda *a, **k: next(inputs))
    monkeypatch.setattr("troubleshooter.check_microphone_os", lambda: True)
    monkeypatch.setattr("troubleshooter.check_mic_permissions", lambda: True)
    monkeypatch.setattr("troubleshooter.check_pyaudio", lambda: True)
    monkeypatch.setattr("troubleshooter.check_internet", lambda: True)
    results = flow_voice_not_working()
    assert results["self_listening"] is True


def test_flow_tts_silent_returns_dict(monkeypatch):
    monkeypatch.setattr("troubleshooter.check_module", lambda *a, **k: True)
    monkeypatch.setattr("troubleshooter.check_internet", lambda: True)
    monkeypatch.setattr("troubleshooter.check_edge_tts_connectivity", lambda: True)
    monkeypatch.setattr("troubleshooter.run_cmd", lambda *a, **k: (True, "", ""))
    monkeypatch.setattr("pathlib.Path.exists", lambda self: True)
    results = flow_tts_silent()
    assert isinstance(results, dict)
    assert "edge_tts" in results


def test_flow_tts_silent_detects_missing_edge_tts(monkeypatch):
    monkeypatch.setattr("troubleshooter.check_module", lambda *a, **k: False)
    monkeypatch.setattr("troubleshooter.ask_yes_no", lambda *a, **k: False)
    monkeypatch.setattr("troubleshooter.check_internet", lambda: True)
    monkeypatch.setattr("troubleshooter.check_edge_tts_connectivity", lambda: False)
    results = flow_tts_silent()
    assert results["edge_tts"] is False


def test_flow_commands_wrong_choice_1_help(monkeypatch):
    monkeypatch.setattr("troubleshooter.ask", lambda *a, **k: "1")
    results = flow_commands_wrong()
    assert results["issue"] == "help_unresponsive"


def test_flow_commands_wrong_choice_2_exam_board(monkeypatch):
    monkeypatch.setattr("troubleshooter.ask", lambda *a, **k: "2")
    results = flow_commands_wrong()
    assert results["issue"] == "exam_board_nlp"


def test_flow_commands_wrong_choice_3_math(monkeypatch):
    monkeypatch.setattr("troubleshooter.ask", lambda *a, **k: "3")
    results = flow_commands_wrong()
    assert "issue" not in results or results.get("issue") == "math_tests"


def test_flow_commands_wrong_choice_4_project(monkeypatch):
    monkeypatch.setattr("troubleshooter.ask", lambda *a, **k: "4")
    results = flow_commands_wrong()
    assert "vs_code" in results


def test_flow_commands_wrong_choice_5_clipboard(monkeypatch):
    monkeypatch.setattr("troubleshooter.ask", lambda *a, **k: "5")
    results = flow_commands_wrong()
    assert results["issue"] == "clipboard"


def test_flow_commands_wrong_choice_6_other(monkeypatch):
    monkeypatch.setattr("troubleshooter.ask", lambda *a, **k: "6")
    results = flow_commands_wrong()
    assert results["issue"] == "other"


def test_flow_files_projects_choice_1_open_file(monkeypatch):
    monkeypatch.setattr("troubleshooter.ask", lambda *a, **k: "1")
    monkeypatch.setattr("troubleshooter.check_chrome", lambda: True)
    results = flow_files_projects()
    assert results["issue"] == "open_file"


def test_flow_files_projects_choice_2_project(monkeypatch):
    monkeypatch.setattr("troubleshooter.ask", lambda *a, **k: "2")
    monkeypatch.setattr("troubleshooter.check_vs_code", lambda: True)
    results = flow_files_projects()
    assert results["issue"] == "project"


def test_flow_files_projects_choice_3_run_script(monkeypatch):
    monkeypatch.setattr("troubleshooter.ask", lambda *a, **k: "3")
    monkeypatch.setattr("troubleshooter.check_file_exists", lambda *a, **k: True)
    results = flow_files_projects()
    assert results["issue"] == "run_script"


def test_flow_files_projects_choice_4_folder_nav(monkeypatch):
    monkeypatch.setattr("troubleshooter.ask", lambda *a, **k: "4")
    monkeypatch.setattr("troubleshooter.check_file_exists", lambda *a, **k: True)
    results = flow_files_projects()
    assert results["issue"] == "folder_nav"


def test_flow_files_projects_choice_5_other(monkeypatch):
    monkeypatch.setattr("troubleshooter.ask", lambda *a, **k: "5")
    results = flow_files_projects()
    assert results["issue"] == "other"


def test_flow_slow_laggy_returns_dict(monkeypatch):
    monkeypatch.setattr("troubleshooter.ask_yes_no", lambda *a, **k: False)
    monkeypatch.setattr("troubleshooter.check_internet", lambda: True)
    monkeypatch.setattr("troubleshooter.check_edge_tts_connectivity", lambda: True)
    results = flow_slow_laggy()
    assert isinstance(results, dict)
    assert "internet" in results


def test_flow_slow_laggy_detects_slow_internet(monkeypatch):
    monkeypatch.setattr("troubleshooter.ask_yes_no", lambda *a, **k: False)
    monkeypatch.setattr("troubleshooter.check_internet", lambda: False)
    results = flow_slow_laggy()
    assert results["internet"] is False


def test_flow_install_update_choice_1_fresh_install(monkeypatch):
    monkeypatch.setattr("troubleshooter.ask", lambda *a, **k: "1")
    monkeypatch.setattr("troubleshooter.ask_yes_no", lambda *a, **k: False)
    monkeypatch.setattr("troubleshooter.check_python_version", lambda: (True, "3.11.0"))
    monkeypatch.setattr("troubleshooter.check_module", lambda *a, **k: True)
    monkeypatch.setattr("troubleshooter.check_file_exists", lambda *a, **k: True)
    monkeypatch.setattr("troubleshooter.run_cmd", lambda *a, **k: (True, "ok", ""))
    results = flow_install_update()
    assert isinstance(results, dict)
    assert results["python_version"] is True


def test_flow_install_update_choice_2_update(monkeypatch):
    monkeypatch.setattr("troubleshooter.ask", lambda *a, **k: "2")
    monkeypatch.setattr("troubleshooter.ask_yes_no", lambda *a, **k: False)
    monkeypatch.setattr("troubleshooter.check_python_version", lambda: (True, "3.11.0"))
    monkeypatch.setattr("troubleshooter.check_module", lambda *a, **k: True)
    monkeypatch.setattr("troubleshooter.check_file_exists", lambda *a, **k: True)
    monkeypatch.setattr("troubleshooter.run_cmd", lambda *a, **k: (True, "ok", ""))
    results = flow_install_update()
    assert results["git_pull"] is True


def test_flow_install_update_choice_3_dependencies(monkeypatch):
    monkeypatch.setattr("troubleshooter.ask", lambda *a, **k: "3")
    monkeypatch.setattr("troubleshooter.ask_yes_no", lambda *a, **k: False)
    monkeypatch.setattr("troubleshooter.check_module", lambda *a, **k: False)
    results = flow_install_update()
    assert results.get("speech_recognition") is False
