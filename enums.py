from enum import Enum

class Platform(Enum):
  """Enum describing various platforms."""
  LINUX = "Linux"
  MACOS = "macOS"
  UNSUPPORTED = "Unsupported"

class RunMode(Enum):
  """Enum describing possible run modes."""
  PRODUCTION = "Production"
  EMULATOR = "Emulator"
  INCONSISTENT = "Inconsistent"