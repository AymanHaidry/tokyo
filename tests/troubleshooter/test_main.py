"""Test main entry point."""
import pytest
from troubleshooter import main


def test_main_runs_flow_1(monkeypatch):
    monkeypatch.setattr("troubleshooter.ask", lambda *a, **k: "1")
    monkeypatch.setattr("troubleshooter.flow_wont_start", lambda: {})
    monkeypatch.setattr("troubleshooter.ask_yes_no", lambda *a, **k: False)
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 0


def test_main_runs_flow_2(monkeypatch):
    monkeypatch.setattr("troubleshooter.ask", lambda *a, **k: "2")
    monkeypatch.setattr("troubleshooter.flow_voice_not_working", lambda: {})
    monkeypatch.setattr("troubleshooter.ask_yes_no", lambda *a, **k: False)
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 0


def test_main_runs_flow_3(monkeypatch):
    monkeypatch.setattr("troubleshooter.ask", lambda *a, **k: "3")
    monkeypatch.setattr("troubleshooter.flow_tts_silent", lambda: {})
    monkeypatch.setattr("troubleshooter.ask_yes_no", lambda *a, **k: False)
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 0


def test_main_runs_flow_4(monkeypatch):
    monkeypatch.setattr("troubleshooter.ask", lambda *a, **k: "4")
    monkeypatch.setattr("troubleshooter.flow_commands_wrong", lambda: {})
    monkeypatch.setattr("troubleshooter.ask_yes_no", lambda *a, **k: False)
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 0


def test_main_runs_flow_5(monkeypatch):
    monkeypatch.setattr("troubleshooter.ask", lambda *a, **k: "5")
    monkeypatch.setattr("troubleshooter.flow_files_projects", lambda: {})
    monkeypatch.setattr("troubleshooter.ask_yes_no", lambda *a, **k: False)
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 0


def test_main_runs_flow_6(monkeypatch):
    monkeypatch.setattr("troubleshooter.ask", lambda *a, **k: "6")
    monkeypatch.setattr("troubleshooter.flow_slow_laggy", lambda: {})
    monkeypatch.setattr("troubleshooter.ask_yes_no", lambda *a, **k: False)
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 0


def test_main_runs_flow_7(monkeypatch):
    monkeypatch.setattr("troubleshooter.ask", lambda *a, **k: "7")
    monkeypatch.setattr("troubleshooter.flow_install_update", lambda: {})
    monkeypatch.setattr("troubleshooter.ask_yes_no", lambda *a, **k: False)
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 0


def test_main_restart_loop(monkeypatch):
    inputs = iter(["1", "2"])
    monkeypatch.setattr("troubleshooter.ask", lambda *a, **k: next(inputs))
    yn_inputs = iter([True, False])
    monkeypatch.setattr("troubleshooter.ask_yes_no", lambda *a, **k: next(yn_inputs))
    call_count = {"flow1": 0, "flow2": 0}
    def fake_flow1():
        call_count["flow1"] += 1
        return {}
    def fake_flow2():
        call_count["flow2"] += 1
        return {}
    monkeypatch.setattr("troubleshooter.flow_wont_start", fake_flow1)
    monkeypatch.setattr("troubleshooter.flow_voice_not_working", fake_flow2)
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert call_count["flow1"] == 1
    assert call_count["flow2"] == 1


def test_main_invalid_choice_then_valid(monkeypatch, capsys):
    inputs = iter(["99", "1"])
    monkeypatch.setattr("troubleshooter.ask", lambda *a, **k: next(inputs))
    monkeypatch.setattr("troubleshooter.flow_wont_start", lambda: {})
    monkeypatch.setattr("troubleshooter.ask_yes_no", lambda *a, **k: False)
    with pytest.raises(SystemExit) as exc_info:
        main()
    captured = capsys.readouterr()
    assert "Invalid choice" in captured.out


def test_main_quit_choice(monkeypatch):
    monkeypatch.setattr("troubleshooter.ask", lambda *a, **k: "q")
    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 0
