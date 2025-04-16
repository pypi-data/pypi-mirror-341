#!/usr/bin/env python3

from argparse import ArgumentParser
from collections import defaultdict
from os import getcwd
from re import DOTALL, IGNORECASE, compile

from git import InvalidGitRepositoryError, Repo
from rich.align import Align as align
from rich.console import Console
from rich.progress import Progress
from rich.table import Table

console = Console()


def initialize_table(title, caption=None):
  table = Table(
    title=title,
    title_style="bold cyan",
    caption=caption,
    caption_style="italic magenta",
    show_header=True,
    header_style="bold white",
    border_style="bright_blue",
    title_justify="center",
    caption_justify="center",
  )

  table.add_column("Author", justify="left", style="green", no_wrap=False)
  table.add_column("Email", justify="left", style="blue", no_wrap=False)
  table.add_column("Commits", justify="right", style="yellow")

  table.add_column("Lines Added", justify="right", style="green")
  table.add_column("Lines Deleted", justify="right", style="red")
  table.add_column("Files Changed", justify="right", style="yellow")

  table.add_column("Pull Requests", justify="right", style="green")
  table.add_column("Reverts", justify="right", style="red")

  table.add_column("First Commit", justify="right", style="magenta")
  table.add_column("Last Commit", justify="right", style="magenta")

  return table


def display(stats):
  table = initialize_table("Git Repository User Stats", "made with <3, by @mcking-07")

  for email, data in sorted(stats.items(), key=lambda x: x[0]):
    names = ", ".join(data["names"])

    names = names if len(names) <= 40 else names[:37] + "..."
    email = email if len(email) <= 30 else email[:27] + "..."

    commits = str(data["commits"])

    lines_added = str(data["lines_added"])
    lines_deleted = str(data["lines_deleted"])
    files_changed = str(len(data["files_changed"]))

    pull_requests = str(data["pull_requests"])
    reverts = str(data["reverts"])

    first_commit = data["first_commit"].strftime("%Y-%m-%d")
    last_commit = data["last_commit"].strftime("%Y-%m-%d")

    table.add_row(names, email, commits, lines_added, lines_deleted, files_changed, pull_requests, reverts, first_commit, last_commit)

  console.print(align.center(table))


def fetch_commits_from(repo, branch):
  console.print(f"[bold cyan]fetching commits from branch: {branch}[/bold cyan]")
  return list(repo.iter_commits(branch))


pr_patterns = [
  compile(r"merge pull request #\d+", IGNORECASE),
  compile(r"merged in .* \(pull request #\d+\)", IGNORECASE),
  compile(r"see (merge|pull) request #\d+", IGNORECASE),
]
revert_pattern = compile(r"revert.*?this reverts commit ([a-f0-9]{7,40})", IGNORECASE | DOTALL)


def is_pull_request(commit):
  return any(pattern.search(commit.message) for pattern in pr_patterns)


def is_revert(commit):
  return revert_pattern.search(commit.message) is not None


def find_original_commit_from(repo, commit):
  match = revert_pattern.search(commit.message)

  return repo.commit(match.group(1).strip()) if match else None


def update_revert_counter(stats, commit, repo):
  if not is_revert(commit):
    return

  original_commit = find_original_commit_from(repo, commit)

  if not original_commit or is_revert(original_commit):
    return

  author_email = original_commit.author.email
  stats[author_email]["reverts"] += 1


def analyze(commits, repo):
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

  with Progress() as progress:
    task = progress.add_task("[cyan]calculating git stats...\n", total=len(commits))

    for commit in commits:
      try:
        commit_author, commit_stats = commit.author, commit.stats
        author_name, author_email = commit_author.name, commit_author.email

        stats[author_email]["names"].add(author_name)
        stats[author_email]["commits"] += 1

        stats[author_email]["lines_added"] += commit_stats.total["insertions"]
        stats[author_email]["lines_deleted"] += commit_stats.total["deletions"]
        stats[author_email]["files_changed"].update(commit_stats.files.keys())

        commit_date = commit.committed_datetime.date()
        stats[author_email]["first_commit"] = min(stats[author_email]["first_commit"] or commit_date, commit_date)
        stats[author_email]["last_commit"] = max(stats[author_email]["last_commit"] or commit_date, commit_date)

        stats[author_email]["pull_requests"] += 1 if is_pull_request(commit) else 0
        update_revert_counter(stats, commit, repo)

        progress.update(task, advance=1)
      except Exception as error:
        raise ValueError(f"error occurred while processing commit: {error}") from error

    return stats


def analyze_and_display_stats_from(repo, branch):
  commits = fetch_commits_from(repo, branch)

  if not commits:
    raise ValueError(f"no commits found in the branch {branch} of the repository {repo.working_tree_dir}")

  stats = analyze(commits, repo)

  if not stats:
    raise ValueError(f"no data found for the branch {branch} of the repository {repo.working_tree_dir}")

  return display(stats)


def validate_repo_and_branch(repo_path, branch_name):
  try:
    repo = Repo(repo_path, search_parent_directories=True)
  except InvalidGitRepositoryError as error:
    raise InvalidGitRepositoryError(f"'{repo_path}' is not a valid git repository") from error

  branches = [branch.name for branch in repo.branches]
  branch = branch_name if branch_name in branches else next((branch for branch in branches if branch in ["main", "master"]), None)

  if branch is None:
    error_message = (
      f"branch '{branch_name}' not found in the repository '{repo_path}'"
      if branch_name
      else f"default branch ('main' or 'master') not found in the repository '{repo_path}'"
    )
    raise ValueError(error_message)

  if branch_name and branch_name not in branches:
    console.print(f"[bold yellow]warning: branch '{branch_name}' not found, defaulting to '{branch}' instead[/bold yellow]")

  return repo, branch


def main():
  parser = ArgumentParser(description="fetch git stats xD")
  parser.add_argument("repo_path", nargs="?", default=getcwd(), help="path to the git repository")
  parser.add_argument("branch", nargs="?", default=None, help="branch to fetch commits from")
  args = parser.parse_args()

  try:
    repo, branch = validate_repo_and_branch(args.repo_path, args.branch)

    return analyze_and_display_stats_from(repo, branch)
  except (InvalidGitRepositoryError, ValueError) as error:
    console.print(f"[bold red]error: {error}[/bold red]")
  except Exception as error:
    console.print(f"[bold red]an unexpected error occurred: {error}[/bold red]")


if __name__ == "__main__":
  main()
