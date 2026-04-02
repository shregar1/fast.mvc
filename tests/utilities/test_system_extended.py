"""Extended tests for system utilities."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Optional
from unittest.mock import patch, MagicMock

import pytest

from utilities.system import SystemUtility


class TestSystemUtilityInit:
    """Test class for SystemUtility initialization."""

    def test_init_with_no_args(self):
        """Test initialization with no arguments."""
        util = SystemUtility()
        assert util._urn is None
        assert util._user_urn is None

    def test_init_with_urn(self):
        """Test initialization with urn."""
        util = SystemUtility(urn="test-urn")
        assert util._urn == "test-urn"

    def test_init_with_user_urn(self):
        """Test initialization with user_urn."""
        util = SystemUtility(user_urn="user-123")
        assert util._user_urn == "user-123"

    def test_init_with_api_name(self):
        """Test initialization with api_name."""
        util = SystemUtility(api_name="test-api")
        assert util._api_name == "api-test"

    def test_init_with_user_id(self):
        """Test initialization with user_id."""
        util = SystemUtility(user_id="user-456")
        assert util._user_id == "user-456"


class TestGitRepositoryFolderName:
    """Tests for git_repository_folder_name method."""

    def test_git_repo_folder_name_in_git_repo(self):
        """Test getting git repo folder name when in a git repo."""
        # This test may pass or fail depending on if we're in a git repo
        result = SystemUtility.git_repository_folder_name()
        # Result should be a string or None
        assert result is None or isinstance(result, str)

    def test_git_repo_folder_name_returns_string_or_none(self):
        """Test git_repository_folder_name returns string or None."""
        result = SystemUtility.git_repository_folder_name()
        assert result is None or isinstance(result, str)

    @patch("subprocess.run")
    def test_git_repo_folder_name_success(self, mock_run):
        """Test git_repository_folder_name with successful git command."""
        mock_run.return_value = MagicMock(returncode=0, stdout="/path/to/repo\n")
        result = SystemUtility.git_repository_folder_name()
        assert result == "repo"

    @patch("subprocess.run")
    def test_git_repo_folder_name_failure(self, mock_run):
        """Test git_repository_folder_name with failed git command."""
        mock_run.return_value = MagicMock(returncode=1, stdout="")
        result = SystemUtility.git_repository_folder_name()
        assert result is None

    @patch("subprocess.run")
    def test_git_repo_folder_name_exception(self, mock_run):
        """Test git_repository_folder_name with exception."""
        mock_run.side_effect = FileNotFoundError()
        result = SystemUtility.git_repository_folder_name()
        assert result is None

    @patch("subprocess.run")
    def test_git_repo_folder_name_timeout(self, mock_run):
        """Test git_repository_folder_name with timeout."""
        mock_run.side_effect = subprocess.TimeoutExpired("git", 3)
        result = SystemUtility.git_repository_folder_name()
        assert result is None


class TestSystemUtilityProperties:
    """Test properties of SystemUtility."""

    def test_urn_property_getter(self):
        """Test urn property getter."""
        util = SystemUtility(urn="test-urn")
        assert util.urn == "test-urn"

    def test_urn_property_setter(self):
        """Test urn property setter."""
        util = SystemUtility()
        util.urn = "new-urn"
        assert util.urn == "new-urn"

    def test_user_urn_property_getter(self):
        """Test user_urn property getter."""
        util = SystemUtility(user_urn="user-test")
        assert util.user_urn == "user-test"

    def test_user_urn_property_setter(self):
        """Test user_urn property setter."""
        util = SystemUtility()
        util.user_urn = "new-user"
        assert util.user_urn == "new-user"

    def test_api_name_property_getter(self):
        """Test api_name property getter."""
        util = SystemUtility(api_name="api-test")
        assert util.api_name == "api-test"

    def test_api_name_property_setter(self):
        """Test api_name property setter."""
        util = SystemUtility()
        util.api_name = "new-api"
        assert util.api_name == "new-api"

    def test_user_id_property_getter(self):
        """Test user_id property getter."""
        util = SystemUtility(user_id="id-test")
        assert util.user_id == "id-test"

    def test_user_id_property_setter(self):
        """Test user_id property setter."""
        util = SystemUtility()
        util.user_id = "new-id"
        assert util.user_id == "new-id"

    def test_logger_property(self):
        """Test logger property."""
        util = SystemUtility()
        assert util.logger is not None


class TestSystemUtilityEdgeCases:
    """Test edge cases for SystemUtility."""

    def test_empty_string_context(self):
        """Test empty string context values."""
        util = SystemUtility(urn="", api_name="")
        assert util.urn == ""
        assert util.api_name == ""

    def test_unicode_context(self):
        """Test unicode in context."""
        util = SystemUtility(urn="系统-urn", api_name="api-测试")
        assert "系统" in util.urn

    def test_special_characters(self):
        """Test special characters in context."""
        special = "test<>!@#$%^&*()"
        util = SystemUtility(urn=special)
        assert util.urn == special

    def test_none_context(self):
        """Test None context values."""
        util = SystemUtility(urn=None, api_name=None)
        assert util.urn is None
        assert util.api_name is None

    def test_multiple_instances_independent(self):
        """Test multiple instances are independent."""
        util1 = SystemUtility(urn="urn1")
        util2 = SystemUtility(urn="urn2")
        assert util1.urn != util2.urn
