from typing import List

from abstracts import SeedableService
from constants import FIRESTORE_USERS_COLLECTION_PATH, STORAGE_PROFILE_IMAGES_FOLDER, STORAGE_RUN_MODES
from enums import RunMode
from firebase_admin import firestore, storage
from generator import Generator


class StorageService(SeedableService):
  """A SeedableService which seeds and unseeds profile images to Firebase Storage."""

  def __init__(self, settings):
    self.settings = settings
    self.bucket = storage.bucket()

  def is_active_in(cls, run_mode: RunMode) -> bool:
    """Determines if the service is available in the current RunMode."""
    return (run_mode in STORAGE_RUN_MODES)

  @classmethod
  def name(cls):
    """Returns the humanized name of this service."""
    return "Storage"

  def can_seed(self):
    """Returns True if this class can seed."""
    return True

  def can_unseed(self):
    """Returns True if this class can unseed."""
    return self.settings["seeding"]["storage_should_unseed"]

  def amount_to_seed(self, uids: List[str]) -> int:
    """Amount of steps required when seeding."""
    return len(uids)

  def _save_url_to_user(self, uid, url):
    """Updates the 'profileImageUrl' field for a given user's Firestore document with a new url."""
    firestore.client().collection(FIRESTORE_USERS_COLLECTION_PATH).document(uid).set({
      "profileImageUrl": url
    }, merge=True)

  def seed(self, uids: List[str], _, generator: Generator, progress_callback) -> List[str]:
    """Seeds profile pictures to Firebase Storage."""
    for uid in uids:
      local_file_path = generator.pick_photo()
      blob = self.bucket.blob(STORAGE_PROFILE_IMAGES_FOLDER + "/" + uid + ".jpg")
      blob.content_type = "image/jpeg"

      with open(local_file_path, "rb") as file:
        blob.upload_from_file(file)
        
      blob.make_public()
      self._save_url_to_user(uid, blob.public_url)

      progress_callback()


  def unseed(self, progress_callback) -> List[str]:
    """Unseeds profile pictures from Firebase Storage."""
    blobs = self.bucket.list_blobs(prefix=STORAGE_PROFILE_IMAGES_FOLDER)

    for blob in blobs:
      blob.delete()
      progress_callback()
