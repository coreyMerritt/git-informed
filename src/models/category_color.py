from enum import Enum


class CategoryColor(str, Enum):
  STD = "#FFFFFF"
  HAPPY = "#22C55E"
  INFO = "#00FFEA"
  WARN = "#FFD700"
  ERROR = "#FFA500"
  CRITICAL = "#DC143C"
