from typing import List

from abstracts import SeedableService
from constants import FIRESTORE_BATCH_SIZE, FIRESTORE_RUN_MODES
from enums import RunMode
from firebase_admin import firestore
from generator import Generator


class FirestoreService(SeedableService):
  def __init__(self, settings):
    self.settings = settings
    self.db = firestore.client()

  def is_active_in(cls, run_mode: RunMode) -> bool:
    return (run_mode in FIRESTORE_RUN_MODES)

  @classmethod
  def name(cls):
    return "Firestore"

  def seed(self, uids: List[str], generator: Generator, progress_callback) -> List[str]:
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
