from enum import Enum

from models.category_color import CategoryColor


class PrivacyMap(str, Enum):
  PRIVATE = CategoryColor.STD.value
  PUBLIC = CategoryColor.WARN.value
