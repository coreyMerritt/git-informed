from rich.table import Table

def _build_table(title: str, color: str) -> Table:
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

class Tables:
  happy_repos: Table = _build_table(
    title="Happy Repos",
    color="#22C55E"
  )
  repos_missing_commits: Table = _build_table(
    title="Repos missing Commits",
    color="#FFD700"
  )
  repos_missing_git_hooks: Table = _build_table(
    title="Repos missing Git Hooks",
    color="#00FFEA"
  )
  repos_missing_upstream: Table = _build_table(
    title="Repos missing an Upstream",
    color="#FFA500"
  )
  repos_with_unpulled_commits: Table = _build_table(
    title="Repos that are Behind",
    color="#FFA500"
  )
  repos_with_unpushed_commits: Table = _build_table(
    title="Repos with Unpushed Commits",
    color="#FFA500"
  )
  repos_with_untracked_files: Table = _build_table(
    title="Repos with Untracked Files",
    color="#FFD700"
  )
  not_repos: Table = Table(
    title="Not a Repo",
    style="#DC143C",
    width=75
  )

  def get_all_tables(self) -> list[Table]:
    return [
      self.happy_repos,
      self.repos_missing_commits,
      self.repos_missing_git_hooks,
      self.repos_missing_upstream,
      self.repos_with_unpulled_commits,
      self.repos_with_unpushed_commits,
      self.repos_with_untracked_files,
      self.not_repos
    ]
