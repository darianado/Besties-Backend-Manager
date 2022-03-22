from enum import Enum

class Platform(Enum):
  LINUX = "Linux"
  WINDOWS = "Windows"
  MACOS = "macOS"
  UNSUPPORTED = "Unsupported"

class RunMode(Enum):
  PRODUCTION = "Production"
  EMULATOR = "Emulator"
  INCONSISTENT = "Inconsistent"