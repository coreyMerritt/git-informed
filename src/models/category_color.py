from enum import Enum


class CategoryColor(str, Enum):
  HAPPY = "#22C55E"
  INFO = "#00FFEA"
  WARN = "#FFD700"
  BIG_WARN = "#FFA500"
  ERROR = "#DC143C"
