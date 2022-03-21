from abc import ABC, abstractmethod
from typing import List

from enums import RunMode
from generator import Generator


class Service(ABC):
  @abstractmethod
  def is_active_in(cls, run_mode: RunMode) -> bool:
    pass

  @classmethod
  @abstractmethod
  def name(cls):
    pass

  @classmethod
  def twenty_char_name(cls):
    name = cls.name()
    return " " * (20 - len(name)) + name


class Seedable(ABC):
  @abstractmethod
  def seed(self, uids: List[str], generator: Generator, progress_callback) -> List[str]:
    pass

  @abstractmethod
  def unseed(self, progress_callback) -> List[str]:
    pass


class SeedableService(Service, Seedable):
  pass
