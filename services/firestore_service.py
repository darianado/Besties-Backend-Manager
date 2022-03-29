from math import ceil
import random
from typing import List

from abstracts import SeedableService
from constants import FIRESTORE_BATCH_SIZE, FIRESTORE_MATCH_COLLECTION_PATH, FIRESTORE_MATCH_MESSAGES_COLLECTION_PATH, FIRESTORE_RUN_MODES, FIRESTORE_USER_RECOMMENDATIONS_DOCUMENT_PATH, FIRESTORE_USERS_COLLECTION_PATH, FIRESTORE_USERS_DERIVED_COLLECTION_PATH
from enums import RunMode
from firebase_admin import firestore
from environment_manager import EnvironmentManager
from functions import MatchingHandler
from generator import Generator
from utils import pick_random_from, pick_random_pairs


class FirestoreService(SeedableService):
  """A SeedableService which seeds and unseeds Firebase Firestore user profiles, matches, and messages."""

  def __init__(self, settings, environment_manager: EnvironmentManager):
    self.settings = settings
    self.environment_manager = environment_manager
    self.db = firestore.client()

  def is_active_in(cls, run_mode: RunMode) -> bool:
    """Determines if the service is available in the current RunMode."""
    return (run_mode in FIRESTORE_RUN_MODES)

  @classmethod
  def name(cls):
    """Returns the humanized name of this service."""
    return "Firestore"

  def can_seed(self):
    """Returns True if this class can seed."""
    return True

  def can_unseed(self):
    """Returns True if this class can unseed."""
    return self.settings["seeding"]["firestore_should_unseed"]

  def _get_amount_of_matches_to_seed(self, number_of_profiles):
    """Returns amount of matches to be seeded, given the settings."""
    return ceil(self.settings["seeding"]["percentage_of_users_to_match"] * float(number_of_profiles))

  def amount_to_seed(self, uids: List[str]) -> int:
    """Amount of steps required when seeding."""
    self.number_of_matches_to_create = self._get_amount_of_matches_to_seed(len(uids))
    self.number_of_matches_to_seed_messages_for = self.number_of_matches_to_create

    return len(uids) + self.number_of_matches_to_create + self.number_of_matches_to_seed_messages_for

  def _seed_users(self, uids: List[str], generator: Generator, progress_callback) -> List[str]:
    """Seeds user profiles to Firestore."""
    user_data_ref = self.db.collection(FIRESTORE_USERS_COLLECTION_PATH)
    split_size = min(FIRESTORE_BATCH_SIZE, len(uids))

    for split in [uids[i:i + split_size] for i in range(0, len(uids), split_size)]:
      batch = self.db.batch()

      for uid in split:
        data = generator.generate_user_data()
        batch.set(user_data_ref.document(uid), data)
        progress_callback()

      batch.commit()

    return uids

  def _seed_matches(self, uids: List[str], progress_callback) -> List[str]:
    """Seeds matches between users to Firestore."""
    self.number_of_matches_to_create = self.number_of_matches_to_create or self._get_amount_of_matches_to_seed(len(uids))
    matches = pick_random_pairs(self.number_of_matches_to_create, uids)

    matching_handler = MatchingHandler(self.environment_manager)

    for match in matches:
      uidOne = match[0]
      uidTwo = match[1]

      matching_handler.like_user(uidOne, uidTwo)
      matching_handler.like_user(uidTwo, uidOne)

      progress_callback()

    return uids

  def _seed_messages_for_match(self, generator: Generator, match_doc):
    """Seeds messages for a given match document from Firestore.
    Seeding is random, and some matches may not have any messages seeded."""
    match_data = match_doc.to_dict()
    should_generate_messages = random.getrandbits(1)

    if should_generate_messages:
      number_of_messages = random.randint(0, 10)

      messages = []

      for _ in range(number_of_messages):
        sender_id = pick_random_from(match_data['uids'])
        messages.append(generator.generate_message(sender_id))

      batch = self.db.batch()
      for message in messages:
        batch.set(match_doc.reference.collection(FIRESTORE_MATCH_MESSAGES_COLLECTION_PATH).document(), message)

      batch.commit()

  def _seed_messages(self, generator: Generator, progress_callback):
    """Seeds potential messages for all matches."""
    match_docs = self.db.collection(FIRESTORE_MATCH_COLLECTION_PATH).stream()

    for doc in match_docs:
      self._seed_messages_for_match(generator, doc)
      progress_callback()


  def seed(self, uids: List[str], _, generator: Generator, progress_callback) -> List[str]:
    """Seeds user profiles, matches, and messages to Firestore."""
    uids = self._seed_users(uids, generator, progress_callback)
    uids = self._seed_matches(uids, progress_callback)
    return self._seed_messages(generator, progress_callback)

  def _unseed_recommendations(self, doc, progress_callback):

    doc.reference.collection(FIRESTORE_USERS_DERIVED_COLLECTION_PATH).document(FIRESTORE_USER_RECOMMENDATIONS_DOCUMENT_PATH).delete()
    progress_callback()

  def _unseed_users(self, progress_callback):
    """Unseeds all user documents from Firestore.
    Also deletes nested data."""
    docs = self.db.collection(FIRESTORE_USERS_COLLECTION_PATH).limit(FIRESTORE_BATCH_SIZE).stream()
    deleted = 0

    for doc in docs:
      self._unseed_recommendations(doc, progress_callback)
      doc.reference.delete()
      deleted = deleted + 1
      progress_callback()

    if deleted >= FIRESTORE_BATCH_SIZE:
      return self.unseed(progress_callback)

  def _unseed_messages(self, doc, progress_callback):
    """Unseeds all messages nested under the provided match Firestore document."""
    docs = self.db.collection(FIRESTORE_MATCH_MESSAGES_COLLECTION_PATH).limit(FIRESTORE_BATCH_SIZE).stream()
    deleted = 0

    for doc in docs:
      doc.reference.delete()
      deleted = deleted + 1
      progress_callback()

    if deleted >= FIRESTORE_BATCH_SIZE:
      return self.unseed(progress_callback)

  def _unseed_matches(self, progress_callback):
    """Unseeds all matches from Firestore.
    Also deletes nested data."""
    docs = self.db.collection(FIRESTORE_MATCH_COLLECTION_PATH).limit(FIRESTORE_BATCH_SIZE).stream()
    deleted = 0

    for doc in docs:
      self._unseed_messages(doc, progress_callback)
      doc.reference.delete()
      deleted = deleted + 1
      progress_callback()

    if deleted >= FIRESTORE_BATCH_SIZE:
      return self.unseed(progress_callback)

  def unseed(self, progress_callback) -> List[str]:
    """Unseed user profiles, matches, and messages from Firestore."""
    super().unseed(progress_callback)
    self._unseed_users(progress_callback)
    self._unseed_matches(progress_callback)
