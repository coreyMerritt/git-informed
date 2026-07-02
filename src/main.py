#!/usr/bin/env python
import argparse
import logging
import os
import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import git
from github import Github
from github.Auth import Token
from github.Repository import Repository
from rich.console import Console
from rich.table import Table
from rich.text import Text

from models.archive_map import ArchiveMap
from models.category_map import CategoryMap
from models.github_tag_map import GITHUB_TAG_MAP
from models.privacy_map import PrivacyMap
from models.project_type import ProjectType

# Args
parser = argparse.ArgumentParser()
parser.add_argument("projects_path", type=str)
args = parser.parse_args()

# Convert Arg Types
some_path = Path(args.projects_path)

# Global Instantiations
def __build_table(title: str, color: CategoryMap) -> Table:
  table = Table(
    title=title,
    style=color,
    width=75,
    title_style="bold white"
  )
  table.add_column("Repo Name", width=37)
  table.add_column("Project Type", width=16)
  table.add_column("Privacy", width=11)
  table.add_column("Activity", width=11)
  return table
console = Console()
happy_repos = __build_table(title="Happy Repos", color=CategoryMap.HAPPY_REPO)
repos_missing_git_hooks = __build_table(title="Repos missing Git Hooks", color=CategoryMap.MISSING_HOOKS)
repos_missing_commits = __build_table(title="Repos missing Commits", color=CategoryMap.MISSING_COMMITS)
repos_with_untracked_files = __build_table(title="Repos with Untracked Files", color=CategoryMap.UNTRACKED_FILES)
repos_with_unpulled_commits = __build_table(title="Repos that are Behind", color=CategoryMap.UNPULLED_COMMITS)
repos_with_unpushed_commits = __build_table(title="Repos with Unpushed Commits", color=CategoryMap.UNPUSHED_COMMITS)
repos_missing_upstream = __build_table(title="Repos missing an Upstream", color=CategoryMap.MISSING_UPSTREAM)
not_repos = Table(title="Not a Repo", style=CategoryMap.NOT_REPO, width=50)
all_tables = (
  happy_repos,
  repos_missing_git_hooks,
  repos_missing_commits,
  repos_with_untracked_files,
  repos_with_unpulled_commits,
  repos_with_unpushed_commits,
  repos_missing_upstream,
  not_repos
)

def main() -> None:
  repos: dict[Path, git.Repo] = {}
  IS_SINGLE_PROJECT = (some_path / ".git").exists()
  if IS_SINGLE_PROJECT:
    project_path = some_path
    repos[project_path] = git.Repo(project_path)
  else:
    projects_path = some_path
    for project_path in sorted(projects_path.iterdir()):
      try:
        repos[project_path] = git.Repo(project_path)
      except git.InvalidGitRepositoryError:
        not_repos.add_row(project_path.resolve().name)
  with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
    executor.map(
      lambda r: r.remotes.origin.fetch(),
      repos.values()
    )
    executor.map(
      __categorize_project,
      repos.keys(),
      repos.values()
    )
  with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
    executor.map(
      __sort_table,
      all_tables
    )
  __output_results()

def __categorize_project(project_path: Path, repo: git.Repo) -> None:
  project_name = project_path.resolve().name
  happy_repo = True
  IS_MISSING_UPSTREAM = len(repo.remote().refs) == 0
  if IS_MISSING_UPSTREAM:
    __add_row(project_name=project_name, repo=repo, table=repos_missing_upstream)
    happy_repo = False
  HAS_UNTRACKED_FILES = len(repo.untracked_files) > 0
  if HAS_UNTRACKED_FILES:
    __add_row(project_name=project_name, repo=repo, table=repos_with_untracked_files)
    happy_repo = False
  status = repo.git.status()
  HAS_UNPULLED_COMMITS = "Your branch is behind " in status
  if HAS_UNPULLED_COMMITS:
    __add_row(project_name=project_name, repo=repo, table=repos_with_unpulled_commits)
    happy_repo = False
  HAS_UNPUSHED_COMMITS = "Your branch is ahead of " in status
  if HAS_UNPUSHED_COMMITS:
    __add_row(project_name=project_name, repo=repo, table=repos_with_unpushed_commits)
    happy_repo = False
  IS_MISSING_COMMITS = "nothing to commit" not in status
  if IS_MISSING_COMMITS:
    __add_row(project_name=project_name, repo=repo, table=repos_missing_commits)
    happy_repo = False
  HAS_GIT_HOOKS = all((Path(repo.git_dir) / "hooks" / h).exists() for h in (
    "pre-commit",
    "post-commit",
    "pre-push"
  ))
  if not HAS_GIT_HOOKS:
    __add_row(project_name=project_name, repo=repo, table=repos_missing_git_hooks)
    happy_repo = False
  if happy_repo:
    __add_row(project_name=project_name, repo=repo, table=happy_repos)

def __add_row(project_name: str, repo: git.Repo, table: Table) -> None:
  gh_repo = __build_github_repo(repo)
  project_type = __get_project_type(gh_repo)
  if gh_repo.private:
    privacy_string = f"[{PrivacyMap.PRIVATE.value}]Private[/{PrivacyMap.PRIVATE.value}]"
  else:
    privacy_string = f"[{PrivacyMap.PUBLIC.value}]Public[/{PrivacyMap.PUBLIC.value}]"
  if gh_repo.archived:
    archive_string = f"[{ArchiveMap.ARCHIVED.value}]Archived[/{ArchiveMap.ARCHIVED.value}]"
  else:
    archive_string = f"[{ArchiveMap.ACTIVE.value}]Active[/{ArchiveMap.ACTIVE.value}]"
  table.add_row(
    project_name,
    project_type,
    privacy_string,
    archive_string
  )

def __build_github_repo(repo: git.Repo) -> Repository:
  owner = __get_repo_owner(repo)
  name = __get_repo_name(repo)
  gh = Github(auth=Token(os.environ["GITHUB_PAT"]))
  return gh.get_repo(f"{owner}/{name}")

def __get_repo_owner(repo: git.Repo) -> str:
  url = repo.remotes.origin.url
  if url.endswith(".git"):
    url = url[:-4]
  match = re.search(r"[:/]([^/:]+)/([^/]+)$", url)
  assert match, f"Could not parse owner/repo from: {url}"
  return match.group(1)

def __get_repo_name(repo: git.Repo) -> str:
  url = repo.remotes.origin.url
  if url.endswith(".git"):
    url = url[:-4]
  match = re.search(r"[:/]([^/:]+)/([^/]+)$", url)
  assert match, f"Could not parse owner/repo from: {url}"
  return match.group(2)

def __get_project_type(gh_repo: Repository) -> ProjectType:
  for tag in gh_repo.get_topics():
    try:
      return GITHUB_TAG_MAP[tag]
    except KeyError:
      pass
  return ProjectType.UNDEFINED

def __sort_table(table: Table) -> None:
  if not table.columns:
    return
  rows = list(zip(*(column._cells for column in table.columns)))  # pylint: disable=protected-access
  def sort_key(row: tuple) -> tuple:
    return tuple(Text.from_markup(str(cell)).plain.lower() for cell in row)
  rows.sort(key=sort_key)
  sorted_columns = list(zip(*rows))
  for column, sorted_cells in zip(table.columns, sorted_columns):
    column._cells = list(sorted_cells)  # pylint: disable=protected-access

def __output_results() -> None:
  print()
  if len(happy_repos.rows) > 0:
    console.print(happy_repos)
    print()
  if len(repos_missing_git_hooks.rows) > 0:
    console.print(repos_missing_git_hooks)
    print()
  if len(repos_missing_commits.rows) > 0:
    console.print(repos_missing_commits)
    print()
  if len(repos_with_untracked_files.rows) > 0:
    console.print(repos_with_untracked_files)
    print()
  if len(repos_with_unpulled_commits.rows) > 0:
    console.print(repos_with_unpulled_commits)
    print()
  if len(repos_with_unpushed_commits.rows) > 0:
    console.print(repos_with_unpushed_commits)
    print()
  if len(repos_missing_upstream.rows) > 0:
    console.print(repos_missing_upstream)
    print()
  if len(not_repos.rows) > 0:
    console.print(not_repos)
    print()


if __name__ == "__main__":
  logging.getLogger("github").setLevel(logging.CRITICAL)
  main()
