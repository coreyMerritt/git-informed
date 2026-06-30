#!/usr/bin/env python
import argparse
from concurrent.futures import ThreadPoolExecutor
import os
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
repos_with_untracked_files = Table("Repos with Untracked Files", style="#FFD700")
repos_with_unpushed_commits = Table("Repos with Unpushed Commits", style="#FFA500")
repos_missing_upstream = Table("Repos Missing an Upstream", style="#FF6347")
not_repos = Table("Not a Git Repo", style="#DC143C")

# Build repo objects first, skipping non-repos
repos_by_path: dict[Path, git.Repo] = {}
for project_path in sorted(path.iterdir()):
  try:
    repos_by_path[project_path] = git.Repo(project_path)
  except InvalidGitRepositoryError:
    not_repos.add_row(str(project_path))

# Fetch all repos concurrently
with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
  executor.map(lambda r: r.remotes.origin.fetch(), repos_by_path.values())

# Categorize Projects
for project_path, repo in repos_by_path.items():
  happy_repo = True
  # Missing Upstream
  if len(repo.remote().refs) == 0:
    repos_missing_upstream.add_row(str(project_path))
    happy_repo = False
  # Untracked Files
  if len(repo.untracked_files) > 0:
    repos_with_untracked_files.add_row(str(project_path))
    happy_repo = False
  status = repo.git.status()
  # Unpushed Commits
  if "Your branch is ahead of " in status:
    repos_with_unpushed_commits.add_row(str(project_path))
    happy_repo = False
  # Missing Commits
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
  # Happy Repo
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
if len(repos_with_unpushed_commits.rows) > 0:
  console.print(repos_with_unpushed_commits)
if len(repos_missing_upstream.rows) > 0:
  console.print(repos_missing_upstream)
if len(not_repos.rows) > 0:
  console.print(not_repos)
