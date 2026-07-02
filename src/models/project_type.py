from enum import Enum
from typing import TypedDict


class GithubTagMap(TypedDict):
  configuration: str
  installation: str
  deployment: str
  cli: str
  scraper: str
  job: str
  service: str
  library: str
  frontend: str
  backend: str
  platform: str
  misc: str

class ProjectType(str, Enum):
  CONFIGURATION = "Configuration"
  INSTALLATION = "Installation"
  DEPLOYMENT = "Deployment"
  CLI_TOOL = "CLI Tool"
  SCRAPER = "Data Scraper"
  JOB = "Job"
  SERVICE = "Service"
  LIBRARY = "Library"
  FRONTEND = "Frontend"
  BACKEND = "Backend"
  PLATFORM = "Platform"
  MISC = "Misc"
  UNDEFINED = "Undefined"
