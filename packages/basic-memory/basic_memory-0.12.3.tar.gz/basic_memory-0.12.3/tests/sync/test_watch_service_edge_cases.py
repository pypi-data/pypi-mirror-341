"""Test edge cases in the WatchService."""

from pathlib import Path
from unittest.mock import patch

import pytest
from watchfiles import Change


def test_filter_changes_valid_path(watch_service, test_config):
    """Test the filter_changes method with valid non-hidden paths."""
    # Regular file path
    assert (
        watch_service.filter_changes(Change.added, str(test_config.home / "valid_file.txt")) is True
    )

    # Nested path
    assert (
        watch_service.filter_changes(
            Change.added, str(test_config.home / "nested" / "valid_file.txt")
        )
        is True
    )


def test_filter_changes_hidden_path(watch_service, test_config):
    """Test the filter_changes method with hidden files/directories."""
    # Hidden file (starts with dot)
    assert (
        watch_service.filter_changes(Change.added, str(test_config.home / ".hidden_file.txt"))
        is False
    )

    # File in hidden directory
    assert (
        watch_service.filter_changes(
            Change.added, str(test_config.home / ".hidden_dir" / "file.txt")
        )
        is False
    )

    # Deeply nested hidden directory
    assert (
        watch_service.filter_changes(
            Change.added, str(test_config.home / "valid" / ".hidden" / "file.txt")
        )
        is False
    )


def test_filter_changes_invalid_path(watch_service, test_config):
    """Test the filter_changes method with invalid paths."""
    # Path outside of config.home
    outside_path = Path("/tmp/outside_path.txt")
    assert watch_service.filter_changes(Change.added, str(outside_path)) is False


@pytest.mark.asyncio
async def test_handle_changes_empty_set(watch_service, test_config):
    """Test handle_changes with an empty set (no processed files)."""
    # Mock write_status to avoid file operations
    with patch.object(watch_service, "write_status", return_value=None):
        # Capture console output to verify
        with patch.object(watch_service.console, "print") as mock_print:
            # Call handle_changes with empty set
            await watch_service.handle_changes(test_config.home, set())

            # Verify divider wasn't printed (processed is empty)
            mock_print.assert_not_called()

            # Verify last_scan was updated
            assert watch_service.state.last_scan is not None

            # Verify synced_files wasn't changed
            assert watch_service.state.synced_files == 0
