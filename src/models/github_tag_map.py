from models.project_type import ProjectType

GITHUB_TAG_MAP = {
  "configuration": ProjectType.CONFIGURATION,
  "installation": ProjectType.INSTALLATION,
  "deployment": ProjectType.DEPLOYMENT,
  "cli": ProjectType.CLI_TOOL,
  "scraper": ProjectType.SCRAPER,
  "job": ProjectType.JOB,
  "service": ProjectType.SERVICE,
  "library": ProjectType.LIBRARY,
  "frontend": ProjectType.FRONTEND,
  "backend": ProjectType.BACKEND,
  "platform": ProjectType.PLATFORM,
  "misc": ProjectType.MISC
}
