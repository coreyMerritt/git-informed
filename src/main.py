#!/usr/bin/env python
import argparse
import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import git
from git.exc import InvalidGitRepositoryError
from rich.console import Console
from rich.table import Table

# Args
parser = argparse.ArgumentParser()
parser.add_argument("projects_path", type=str)
args = parser.parse_args()

# Convert Arg Types
projects_path = Path(args.projects_path)

# Global Instantiations
console = Console()
happy_repos = Table("Happy Repos", style="#22C55E")
repos_missing_git_hooks = Table("Repos Missing Git Hooks", style="#00FFEA")
repos_missing_commits = Table("Repos Missing Commits", style="#FFD700")
repos_with_untracked_files = Table("Repos with Untracked Files", style="#FFD700")
repos_with_unpulled_commits = Table("Repos that are Behind", style="#FFA500")
repos_with_unpushed_commits = Table("Repos with Unpushed Commits", style="#FFA500")
repos_missing_upstream = Table("Repos Missing an Upstream", style="#FF6347")
not_repos = Table("Not a Git Repo", style="#DC143C")

def main():
  if (projects_path / ".git").exists():
    repos_by_path = {projects_path: git.Repo(projects_path)}
  else:
    repos_by_path = __build_repos_by_path()
  with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
    executor.map(lambda r: r.remotes.origin.fetch(), repos_by_path.values())
  __categorize_projects(repos_by_path)
  __output_results()

def __build_repos_by_path() -> dict[Path, git.Repo]:
  repos: dict[Path, git.Repo] = {}
  for project_path in sorted(projects_path.iterdir()):
    try:
      repos[project_path] = git.Repo(project_path)
    except InvalidGitRepositoryError:
      not_repos.add_row(project_path.resolve().name)
  return repos

def __categorize_projects(repos_by_path: dict[Path, git.Repo]) -> None:
  for project_path, repo in repos_by_path.items():
    project_name = project_path.resolve().name
    happy_repo = True
    IS_MISSING_UPSTREAM = len(repo.remote().refs) == 0
    if IS_MISSING_UPSTREAM:
      repos_missing_upstream.add_row(project_name)
      happy_repo = False
    HAS_UNTRACKED_FILES = len(repo.untracked_files) > 0
    if HAS_UNTRACKED_FILES:
      repos_with_untracked_files.add_row(project_name)
      happy_repo = False
    status = repo.git.status()
    HAS_UNPULLED_COMMITS = "Your branch is behind " in status
    if HAS_UNPULLED_COMMITS:
      repos_with_unpulled_commits.add_row(project_name)
      happy_repo = False
    HAS_UNPUSHED_COMMITS = "Your branch is ahead of " in status
    if HAS_UNPUSHED_COMMITS:
      repos_with_unpushed_commits.add_row(project_name)
      happy_repo = False
    IS_MISSING_COMMITS = "nothing to commit" not in status
    if IS_MISSING_COMMITS:
      repos_missing_commits.add_row(project_name)
      happy_repo = False
    HAS_GIT_HOOKS = all((Path(repo.git_dir) / "hooks" / h).exists() for h in (
      "pre-commit",
      "post-commit",
      "pre-push"
    ))
    if not HAS_GIT_HOOKS:
      repos_missing_git_hooks.add_row(project_name)
      happy_repo = False
    if happy_repo:
      happy_repos.add_row(project_name)

def __output_results() -> None:
  if len(happy_repos.rows) > 0:
    console.print(happy_repos)
  if len(repos_missing_git_hooks.rows) > 0:
    console.print(repos_missing_git_hooks)
  if len(repos_missing_commits.rows) > 0:
    console.print(repos_missing_commits)
  if len(repos_with_untracked_files.rows) > 0:
    console.print(repos_with_untracked_files)
  if len(repos_with_unpulled_commits.rows) > 0:
    console.print(repos_with_unpulled_commits)
  if len(repos_with_unpushed_commits.rows) > 0:
    console.print(repos_with_unpushed_commits)
  if len(repos_missing_upstream.rows) > 0:
    console.print(repos_missing_upstream)
  if len(not_repos.rows) > 0:
    console.print(not_repos)


if __name__ == "__main__":
  main()
