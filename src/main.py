#!/usr/bin/env python
import argparse
from pathlib import Path

import git
from git.exc import InvalidGitRepositoryError
from rich.console import Console
from rich.table import Table

# Args
parser = argparse.ArgumentParser()
parser.add_argument("path", type=str)
args = parser.parse_args()

# Validate args
path = Path(args.path)

# Instantiations
console = Console()
happy_repos = Table("Happy Repos", style="#22C55E")
repos_missing_git_hooks = Table("Repos Missing Git Hooks", style="#00FFEA")
repos_missing_commits = Table("Repos Missing Commits", style="#FFD700")
repos_with_untracked_files = Table("Repos with Untracked Files", style="#FFA500")
repos_missing_upstream = Table("Repos Missing an Upstream", style="#FF6347")
not_repos = Table("Not a Git Repo", style="#DC143C")

# Categorize Projects
for project_path in sorted(path.iterdir()):
  happy_repo = True
  # Not a git Repo
  try:
    repo = git.Repo(project_path)
  except InvalidGitRepositoryError:
    not_repos.add_row(str(project_path))
    happy_repo = False
  # Missing Upstream
  if len(repo.remote().refs) == 0:
    repos_missing_upstream.add_row(str(project_path))
    happy_repo = False
  # Untracked Files
  if len(repo.untracked_files) > 0:
    repos_with_untracked_files.add_row(str(project_path))
    happy_repo = False
  # Missing Commits
  status = repo.git.status()
  if "nothing to commit" not in status:
    repos_missing_commits.add_row(str(project_path))
    happy_repo = False
  # Missing Git Hooks
  has_git_hooks = all(
    (Path(repo.git_dir) / "hooks" / hook).exists() for hook in ("pre-push", "pre-commit", "post-commit")
  )
  if not has_git_hooks:
    repos_missing_git_hooks.add_row(str(project_path))
    happy_repo = False
  # Happy_Repo
  if happy_repo:
    happy_repos.add_row(str(project_path))

# Output
if len(happy_repos.rows) > 0:
  console.print(happy_repos)
if len(repos_missing_git_hooks.rows) > 0:
  console.print(repos_missing_git_hooks)
if len(repos_missing_commits.rows) > 0:
  console.print(repos_missing_commits)
if len(repos_with_untracked_files.rows) > 0:
  console.print(repos_with_untracked_files)
if len(repos_missing_upstream.rows) > 0:
  console.print(repos_missing_upstream)
if len(not_repos.rows) > 0:
  console.print(not_repos)
