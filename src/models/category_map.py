from enum import Enum

from models.category_color import CategoryColor


class CategoryMap(str, Enum):
  HAPPY_REPO = CategoryColor.HAPPY.value
  MISSING_HOOKS = CategoryColor.INFO.value
  MISSING_COMMITS = CategoryColor.WARN.value
  UNTRACKED_FILES = CategoryColor.WARN.value
  UNPULLED_COMMITS = CategoryColor.ERROR.value
  UNPUSHED_COMMITS = CategoryColor.ERROR.value
  MISSING_UPSTREAM = CategoryColor.ERROR.value
  NOT_REPO = CategoryColor.CRITICAL.value
