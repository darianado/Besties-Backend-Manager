from typing import List

from abstracts import SeedableService
from constants import AUTH_RUN_MODES
from enums import RunMode
from firebase_admin import auth
from generator import Generator


class AuthService(SeedableService):
  """A SeedableService which seeds and unseeds Firebase Authentication user profiles."""

  def __init__(self, settings):
    self.settings = settings

  def is_active_in(cls, run_mode: RunMode) -> bool:
    """Determines if the service is available in the current RunMode."""
    return (run_mode in AUTH_RUN_MODES)

  @classmethod
  def name(cls):
    """Returns the humanized name of this service."""
    return "Authentication"

  def can_seed(self):
    """Returns True if this class can seed."""
    return True

  def can_unseed(self):
    """Returns True if this class can unseed."""
    return self.settings["seeding"]["auth_should_unseed"]

  def amount_to_seed(self, uids: List[str]) -> int:
    """Amount of steps required when seeding."""
    return len(uids)

  def seed(self, uids: List[str], required_accounts, generator: Generator, progress_callback):
    """Seeds randomized and required accounts to Firebase Authentication."""
    super().seed(uids, generator, required_accounts, progress_callback)

    number_of_required_accounts = len(required_accounts)
    required_accounts_uids = uids[:number_of_required_accounts]
    random_accounts_uids = uids[number_of_required_accounts:]

    for required_account in required_accounts:
      uid = required_accounts_uids.pop()
      email = required_account["email"]
      password = required_account["password"]

      auth.create_user(
        uid=uid,
        email=email,
        email_verified=self.settings["seeding"]["context"]["email_verified"],
        password=password)

      progress_callback()

    for uid in random_accounts_uids:
      auth.create_user(
        uid=uid,
        email=generator.pick_unique_email(),
        email_verified=self.settings["seeding"]["context"]["email_verified"],
        password=self.settings["seeding"]["context"]["password"])

      progress_callback()

  def unseed(self, progress_callback):
    """Unseeds all Firebase Authentication users."""
    super().unseed(progress_callback)

    for user in auth.list_users().iterate_all():
      auth.delete_user(user.uid)
      progress_callback()
