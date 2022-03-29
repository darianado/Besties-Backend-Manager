import uuid
from typing import List

from alive_progress import alive_bar

from abstracts import SeedableService
from constants import CIRCLES_BAR, CIRCLES_BAR_SPINNER
from generator import Generator
from utils import load_settings


class SeedingHandler:
  """Class that handles seeding and unseeding from various services, 
  as well as showing progress bars in the console."""

  def __init__(self):
    self.reload_settings()

  def _generate_uids(self, amount):
    """Generates and returns a number of random UUID v4 strings."""
    return [uuid.uuid4().hex for _ in range(amount)]

  def reload_settings(self):
    """Reloads the settings file to get newest changes."""
    self.settings = load_settings()

  def seed(self, services: List[SeedableService]):
    """Seeds all available services that can be seeded."""
    self.reload_settings()

    generator = Generator(self.settings)
    number_of_random_users_to_seed = self.settings["seeding"]["number_of_random_users_to_seed"]
    required_accounts = self.settings["seeding"]["required_accounts"]
    uids = self._generate_uids(number_of_random_users_to_seed + len(required_accounts))

    print(f"Seeding {len(uids)} users.")
    print("")

    for service in services:
      total = service.amount_to_seed(uids)
      with alive_bar(total, title=service.twenty_char_name() + ":", bar=CIRCLES_BAR) as bar:
        service.seed(uids, required_accounts, generator, bar)

    print("")
    print("Successfully seeded to all services.")

  def unseed(self, services: List[SeedableService]):
    """Unseeds all available services that can be unseeded."""
    print("Unseeding users.")
    print("")

    for service in services:
      with alive_bar(title=service.twenty_char_name() + ":", bar=CIRCLES_BAR, unknown=CIRCLES_BAR_SPINNER) as bar:
        service.unseed(bar)

    print("")
    print("Successfully unseeded all services.")
