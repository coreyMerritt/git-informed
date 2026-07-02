from enum import Enum

from models.category_color import CategoryColor


class ArchiveMap(str, Enum):
  ARCHIVED = CategoryColor.INFO.value
  ACTIVE = CategoryColor.STD.value
