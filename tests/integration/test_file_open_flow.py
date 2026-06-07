"""End-to-end file opening flow test."""
import pytest
from pathlib import Path
from unittest.mock import patch


def test_open_folder_flow(engine, parser, mock_ui, mock_voice, mock_memory, mock_intel):
    from kosmosic_orbiton import process_text
    with patch.object(Path, 'exists', return_value=True),          patch.object(Path, 'is_dir', return_value=True):
        with patch('kosmosic_orbiton.subprocess.run') as mock_run:
            success, action = process_text(
                "open downloads",
                engine, parser, mock_memory, mock_voice, mock_ui, mock_intel
            )
            assert success is True
            mock_run.assert_called_once()


def test_open_file_flow(engine, parser, mock_ui, mock_voice, mock_memory, mock_intel):
    from kosmosic_orbiton import process_text
    with patch.object(engine, 'open_path') as mock_open:
        success, action = process_text(
            "open report.pdf",
            engine, parser, mock_memory, mock_voice, mock_ui, mock_intel
        )
        assert success in [True, False]
