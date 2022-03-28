from math import ceil
import random
from typing import List

from abstracts import SeedableService
from constants import FIRESTORE_BATCH_SIZE, FIRESTORE_RUN_MODES
from enums import RunMode
from firebase_admin import firestore
from environment_manager import EnvironmentManager
from functions import MatchingHandler
from generator import Generator


class FirestoreService(SeedableService):
  def __init__(self, settings, environment_manager: EnvironmentManager):
    self.settings = settings
    self.environment_manager = environment_manager
    self.db = firestore.client()

  def is_active_in(cls, run_mode: RunMode) -> bool:
    return (run_mode in FIRESTORE_RUN_MODES)

  @classmethod
  def name(cls):
    return "Firestore"

  def can_seed(self):
    return True

  def can_unseed(self):
    return self.settings["seeding"]["firestore_should_unseed"]

  def _get_amount_of_matches_to_seed(self, number_of_profiles):
    return ceil(self.settings["seeding"]["percentage_of_users_to_match"] * float(number_of_profiles))

  def amount_to_seed(self, uids: List[str]) -> int:
    self.number_of_matches_to_create = self._get_amount_of_matches_to_seed(len(uids))
    return len(uids) + self.number_of_matches_to_create

  def _seed_users(self, uids: List[str], generator: Generator, progress_callback) -> List[str]:
    users_collection_ref = self.settings["seeding"]["firestore_users_collection_path"]
    user_data_ref = self.db.collection(users_collection_ref)
    split_size = min(FIRESTORE_BATCH_SIZE, len(uids))

    for split in [uids[i:i + split_size] for i in range(0, len(uids), split_size)]:
      batch = self.db.batch()

      for uid in split:
        data = generator.generate_user_data()
        batch.set(user_data_ref.document(uid), data)
        progress_callback()

      batch.commit()

    return uids

  def _pick_random_pairs(self, n: int, lst: List):
    result = []

    while(n > 0):
      result.append(random.sample(lst, 2))
      n -= 1

    return result


  def _seed_matches(self, uids: List[str], progress_callback) -> List[str]:
    self.number_of_matches_to_create = self.number_of_matches_to_create or self._get_amount_of_matches_to_seed(len(uids))
    matches = self._pick_random_pairs(self.number_of_matches_to_create, uids)

    matching_handler = MatchingHandler(self.environment_manager)

    for match in matches:
      uidOne = match[0]
      uidTwo = match[1]

      matching_handler.like_user(uidOne, uidTwo)
      matching_handler.like_user(uidTwo, uidOne)

      progress_callback()

    return uids


  def seed(self, uids: List[str], generator: Generator, progress_callback) -> List[str]:
    uids = self._seed_users(uids, generator, progress_callback)
    return self._seed_matches(uids, progress_callback)

  def unseed(self, progress_callback) -> List[str]:
    super().unseed(progress_callback)

    users_collection_ref = self.settings["seeding"]["firestore_users_collection_path"]
    docs = self.db.collection(users_collection_ref).limit(FIRESTORE_BATCH_SIZE).stream()
    deleted = 0

    for doc in docs:
      doc.reference.delete()
      deleted = deleted + 1
      progress_callback()

    if deleted >= FIRESTORE_BATCH_SIZE:
      return self.unseed(progress_callback)
