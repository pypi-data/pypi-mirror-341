from collections import defaultdict
from datetime import date
from unittest.mock import MagicMock, patch

import pytest
from git import Actor, Commit, InvalidGitRepositoryError, Repo

from src.cli import (
  analyze,
  fetch_commits_from,
  find_original_commit_from,
  is_pull_request,
  is_revert,
  update_revert_counter,
  validate_repo_and_branch,
)


@pytest.fixture
def mock_repo():
  return MagicMock(spec=Repo)


@pytest.fixture
def mock_commit():
  commit = MagicMock(spec=Commit)
  commit.author = MagicMock(spec=Actor)

  return commit


@patch("src.cli.Repo")
def test_validate_repo_and_branch_valid(MockRepo, mock_repo):
  MockRepo.return_value = mock_repo

  mock_repo.branches = [MagicMock(name="main"), MagicMock(name="develop")]
  mock_repo.branches[0].name = "main"
  mock_repo.branches[1].name = "develop"

  repo, branch = validate_repo_and_branch("valid/path/to/repo", "develop")

  assert repo == mock_repo
  assert branch == "develop"


@patch("src.cli.Repo")
def test_validate_repo_and_branch_invalid_repo(MockRepo):
  MockRepo.side_effect = InvalidGitRepositoryError

  with pytest.raises(InvalidGitRepositoryError):
    validate_repo_and_branch("invalid/path/to/repo", None)


@patch("src.cli.Repo")
def test_validate_repo_and_branch_branch_not_found(MockRepo, mock_repo):
  MockRepo.return_value = mock_repo

  mock_repo.branches = [MagicMock(name="main")]
  mock_repo.branches[0].name = "main"

  mock_repo.heads = MagicMock()
  mock_repo.heads.__iter__.return_value = [MagicMock(name="main")]

  repo, branch = validate_repo_and_branch(mock_repo, "nonexistent_branch")

  assert repo == mock_repo
  assert branch == "main"


def test_fetch_commits_from(mock_repo):
  mock_repo.iter_commits.return_value = [MagicMock(spec=Commit), MagicMock(spec=Commit)]
  commits = fetch_commits_from(mock_repo, "main")

  assert len(commits) == len(mock_repo.iter_commits.return_value)
  mock_repo.iter_commits.assert_called_with("main")


def test_analyze_with_no_commits(mock_repo):
  mock_repo.iter_commits.return_value = []
  stats = analyze([], mock_repo)

  assert stats == defaultdict(
    lambda: {
      "names": set(),
      "commits": 0,
      "lines_added": 0,
      "lines_deleted": 0,
      "files_changed": set(),
      "pull_requests": 0,
      "reverts": 0,
      "first_commit": None,
      "last_commit": None,
    }
  )


def test_analyze_with_commits(mock_repo, mock_commit):
  mock_commit.author.name = "Test Author"
  mock_commit.author.email = "test@example.com"

  mock_commit.stats.total = {"insertions": 10, "deletions": 5}
  mock_commit.stats.files = {"file1.txt": None, "file2.txt": None}

  mock_commit.committed_datetime.date.return_value = date(2024, 5, 1)
  mock_commit.message = "Test commit message"

  mock_repo.iter_commits.return_value = [mock_commit]
  stats = analyze([mock_commit], mock_repo)

  assert stats["test@example.com"]["names"] == {"Test Author"}
  assert stats["test@example.com"]["commits"] == 1

  assert stats["test@example.com"]["lines_added"] == 10
  assert stats["test@example.com"]["lines_deleted"] == 5
  assert len(stats["test@example.com"]["files_changed"]) == 2

  assert stats["test@example.com"]["first_commit"] == date(2024, 5, 1)
  assert stats["test@example.com"]["last_commit"] == date(2024, 5, 1)


def test_is_pull_request(mock_commit):
  valid_messages = [
    "Merge pull request #123 from example/branch",
    "Merged in master from example/branch (pull request #123)",
    "See merge request #123",
  ]

  for message in valid_messages:
    mock_commit.message = message
    assert is_pull_request(mock_commit) is True

  invalid_messages = ["Some commit message", "Is this a commit too"]

  for message in invalid_messages:
    mock_commit.message = message
    assert is_pull_request(mock_commit) is False


def test_is_revert(mock_commit):
  valid_messages = [
    'Revert "Merged SomeFeature (pull request #42)"\n\nThis reverts commit abcdef1234567890.',
    "Revert: Fix some bug\n\nThis reverts commit 0123456789abcdef.",
  ]

  for message in valid_messages:
    mock_commit.message = message
    assert is_revert(mock_commit) is True

  invalid_messages = ["Some commit message", "Fix some bug", "Normal commit message"]

  for message in invalid_messages:
    mock_commit.message = message
    assert is_revert(mock_commit) is False


def test_find_original_commit_from(mock_repo, mock_commit):
  original_commit_hash = "abcdef1234567890"
  mock_commit.message = f'Revert "Merged SomeFeature (pull request #42)"\n\nThis reverts commit {original_commit_hash}.'

  mock_repo.commit.return_value = MagicMock(spec=Commit)
  original_commit = find_original_commit_from(mock_repo, mock_commit)

  assert original_commit is not None
  mock_repo.commit.assert_called_with(original_commit_hash.strip())

  mock_commit.message = "Normal commit message"
  original_commit = find_original_commit_from(mock_repo, mock_commit)

  assert original_commit is None


def test_update_revert_counter(mock_repo, mock_commit):
  mock_commit.message = 'Revert "Merged SomeFeature (pull request #42)"\n\nThis reverts commit abcdef1234567890.'
  mock_commit.author = MagicMock(spec=Actor)
  mock_commit.committed_datetime.date.return_value = date(2024, 5, 1)

  original_commit = MagicMock(spec=Commit)
  original_commit.author = MagicMock(spec=Actor)
  original_commit.author.email = "original@example.com"
  original_commit.message = "Original commit message"

  mock_repo.commit.return_value = original_commit

  stats = defaultdict(
    lambda: {
      "names": set(),
      "commits": 0,
      "lines_added": 0,
      "lines_deleted": 0,
      "files_changed": set(),
      "pull_requests": 0,
      "reverts": 0,
      "first_commit": None,
      "last_commit": None,
    }
  )

  update_revert_counter(stats, mock_commit, mock_repo)
  assert stats[original_commit.author.email]["reverts"] == 1
