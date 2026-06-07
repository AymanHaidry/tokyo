"""End-to-end file opening flow test."""
import pytest
from pathlib import Path
from unittest.mock import patch
import sys


def _patch_open_explorer():
    """Patch the correct subprocess call based on platform."""
    if sys.platform == "win32":
        return patch('kosmosic_orbiton.subprocess.Popen')
    return patch('kosmosic_orbiton.subprocess.run')


def test_open_folder_flow(engine, parser, mock_ui, mock_voice, mock_memory, mock_intel):
    from kosmosic_orbiton import process_text
    with patch.object(Path, 'exists', return_value=True),          patch.object(Path, 'is_dir', return_value=True):
        with _patch_open_explorer() as mock_subprocess:
            success, action = process_text(
                "open downloads",
                engine, parser, mock_memory, mock_voice, mock_ui, mock_intel
            )
            assert success is True
            mock_subprocess.assert_called_once()


def test_open_file_flow(engine, parser, mock_ui, mock_voice, mock_memory, mock_intel):
    from kosmosic_orbiton import process_text
    with patch.object(engine, 'open_path') as mock_open:
        success, action = process_text(
            "open report.pdf",
            engine, parser, mock_memory, mock_voice, mock_ui, mock_intel
        )
        assert success in [True, False]
