#!/usr/bin/env python
from pathlib import Path

import git
from rich.console import Console
from rich.table import Table

from models.category_map import CategoryMap


def handle_project_status(project_path: Path) -> None:
  console = Console()
  project_name = project_path.resolve().name
  repo = git.Repo(project_path)
  repo_table = Table(project_name)
  repo.remotes.origin.fetch()
  __categorize_project(
    repo=repo,
    repo_table=repo_table
  )
  console.print(repo_table)

def __categorize_project(repo: git.Repo, repo_table: Table) -> None:
  happy_repo = True
  IS_MISSING_UPSTREAM = len(repo.remote().refs) == 0
  if IS_MISSING_UPSTREAM:
    repo_table.add_row("Missing Upstream", style=CategoryMap.MISSING_UPSTREAM)
    happy_repo = False
  HAS_UNTRACKED_FILES = len(repo.untracked_files) > 0
  if HAS_UNTRACKED_FILES:
    repo_table.add_row("Untracked Files", style=CategoryMap.UNTRACKED_FILES)
    happy_repo = False
  status = repo.git.status()
  HAS_UNPULLED_COMMITS = "Your branch is behind " in status
  if HAS_UNPULLED_COMMITS:
    repo_table.add_row("Unpulled Commits", style=CategoryMap.UNPULLED_COMMITS)
    happy_repo = False
  HAS_UNPUSHED_COMMITS = "Your branch is ahead of " in status
  if HAS_UNPUSHED_COMMITS:
    repo_table.add_row("Unpushed Commits", style=CategoryMap.UNPUSHED_COMMITS)
    happy_repo = False
  IS_MISSING_COMMITS = "nothing to commit" not in status
  if IS_MISSING_COMMITS:
    repo_table.add_row("Missing Commits", style=CategoryMap.MISSING_COMMITS)
    happy_repo = False
  HAS_GIT_HOOKS = all((Path(repo.git_dir) / "hooks" / h).exists() for h in (
    "pre-commit",
    "post-commit",
    "pre-push"
  ))
  if not HAS_GIT_HOOKS:
    repo_table.add_row("Doesn't have Git Hooks", style=CategoryMap.MISSING_HOOKS)
    happy_repo = False
  if happy_repo:
    repo_table.add_row("Happy Repo", style=CategoryMap.HAPPY_REPO)
