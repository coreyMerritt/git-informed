from enum import Enum

from models.category_color import CategoryColor


class CategoryMap(str, Enum):
  HAPPY_REPO = CategoryColor.HAPPY.value
  MISSING_HOOKS = CategoryColor.INFO.value
  MISSING_COMMITS = CategoryColor.WARN.value
  UNTRACKED_FILES = CategoryColor.WARN.value
  UNPULLED_COMMITS = CategoryColor.BIG_WARN.value
  UNPUSHED_COMMITS = CategoryColor.BIG_WARN.value
  MISSING_UPSTREAM = CategoryColor.BIG_WARN.value
  NOT_REPO = CategoryColor.ERROR.value
