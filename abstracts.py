from abc import ABC, abstractmethod
from typing import List

from enums import RunMode
from generator import Generator


class Service(ABC):
  """Abstract class that any Service must conform to.
  A Service is anything that can perform an action when called upon."""

  @abstractmethod
  def is_active_in(cls, run_mode: RunMode) -> bool:
    """Implementations of this method are expected to return True 
    if the Service can perform any action under the given RunMode."""
    pass

  @classmethod
  @abstractmethod
  def name(cls):
    """Implementations of this method are expected to return a string
    containing the class's humanized name."""
    pass

  @classmethod
  def twenty_char_name(cls):
    """Returns a padded string containing the humanized name of the class.
    Only overload this method if the default implementation is insufficient."""
    name = cls.name()
    return " " * (20 - len(name)) + name


class Seedable(ABC):
  """Abstract class that any Seedable class must conform to."""

  @abstractmethod
  def seed(self, uids: List[str], required_accounts, generator: Generator, progress_callback) -> List[str]:
    """Implementations of this function are expected to seed the environment.
    Details may vary, and it is up the the individual class to determine what constitutes seeding."""
    pass

  @abstractmethod
  def unseed(self, progress_callback) -> List[str]:
    """Implementations of this function are expected to unseed the environment.
    Details may vary, and it is up the the individual class to determine what constitutes unseeding."""
    pass

  def can_seed(self):
    """Implementations of this class are expected to return True 
    if the 'seed' function can be called in the given environment."""
    return True

  def can_unseed(self):
    """Implementations of this class are expected to return True 
    if the 'unseed' function can be called in the given environment."""
    return True

  @abstractmethod
  def amount_to_seed(self, uids: List[str]) -> int:
    """Implementations of this class are expected to return a number 
    corresponding to the number of atomic "steps" seeding that class involves."""
    pass


class SeedableService(Service, Seedable):
  """A Service that is seedable."""
  pass
