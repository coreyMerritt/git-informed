#!/usr/bin/env python
import argparse
from pathlib import Path

from project import handle_project_status
from projects import handle_projects_status

# Args
parser = argparse.ArgumentParser()
parser.add_argument("projects_path", type=str)
args = parser.parse_args()

# Convert Arg Types
path = Path(args.projects_path)

def main():
  if (path / ".git").exists():
    handle_project_status(
      project_path=path
    )
  else:
    handle_projects_status(
      projects_path=path
    )

if __name__ == "__main__":
  main()
