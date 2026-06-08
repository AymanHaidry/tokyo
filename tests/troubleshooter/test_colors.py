"""Test ANSI color helpers."""
import pytest
from troubleshooter import Colors


def test_ok_contains_green_check():
    out = Colors.ok("python 3.11")
    assert Colors.GREEN in out
    assert "✓" in out
    assert "python 3.11" in out


def test_fail_contains_red_x():
    out = Colors.fail("missing")
    assert Colors.RED in out
    assert "✗" in out


def test_warn_contains_yellow_warning():
    out = Colors.warn("old version")
    assert Colors.YELLOW in out
    assert "⚠" in out


def test_info_contains_blue_info():
    out = Colors.info("note")
    assert Colors.BLUE in out
    assert "ℹ" in out


def test_arrow_contains_cyan_arrow():
    out = Colors.arrow("next step")
    assert Colors.CYAN in out
    assert "→" in out


def test_title_contains_bold_magenta():
    out = Colors.title("DIAGNOSING")
    assert Colors.BOLD in out
    assert Colors.MAGENTA in out
    assert "DIAGNOSING" in out
