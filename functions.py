import time
import json, os, uuid
from decorators import sleepy_exit, safe_exit
from generator import Generator
import firebase_admin
from firebase_admin import credentials, firestore, storage
import requests

class FirebaseHandler():
    BATCH_SIZE = 500
    CREDENTIALS_FILENAME = 'serviceAccountKey.json'

    def get_credentials(self, cert):
      try:
        return credentials.Certificate(cert)
      except:
        raise 

    def __init__(self):
        cred = self.get_credentials(self.CREDENTIALS_FILENAME)
        firebase_admin.initialize_app(cred, {
          'storageBucket': 'seg-djangoals.appspot.com',
        })

        self.db = firestore.client()
        self.bucket = storage.bucket()

    def save_images(self, data):
      for user_data in data:
        local_paths = user_data.pop("images")

        for local_path in local_paths:
          blob_base_path = "user_avatars/" + user_data["uid"] + "/"
          blob = self.bucket.blob(blob_base_path + uuid.uuid4().hex + ".jpg")
          blob.content_type = "image/jpeg"
          
          with open(local_path, 'rb') as file:
            blob.upload_from_file(file)

    def save_users(self, data):
      USER_DATA_REF = self.db.collection("users")
      split_size = min(self.BATCH_SIZE, len(data))

      for split in [data[i:i + split_size] for i in range(0, len(data), split_size)]:
        batch = self.db.batch()

        for user_data in split:
          uid = user_data.pop('uid')
          user_data.pop('images', None)
          batch.set(USER_DATA_REF.document(uid), user_data)

        batch.commit()

    def delete_all_user_avatars(self):
      blobs = self.bucket.list_blobs(prefix="user_avatars")
      for blob in blobs:
        blob.delete()

    def delete_all_users(self):
      USER_DATA_REF = self.db.collection("users")

      docs = USER_DATA_REF.limit(self.BATCH_SIZE).stream()

      deleted = 0

      for doc in docs:
        doc.reference.delete()
        deleted = deleted + 1
        print(".", end="", flush=True)

      if deleted >= self.BATCH_SIZE:
        return self.delete_all_users()
      else:
        print("")


handler = FirebaseHandler()

@sleepy_exit
@safe_exit
def seed_database():
    print("Seeding users")
    generator = Generator("seed_settings.json")
    settings = json.load(open("main_settings.json"))

    print("Generating users... ", end="", flush=True)
    data = generator.generate()
    print("OK")
    if(not os.environ.get('FIRESTORE_EMULATOR_HOST')):
      print("Saving images to Storage... ", end="", flush=True)
      handler.save_images(data)
      print("OK")
    print("Saving users to Firestore... ", end="", flush=True)
    handler.save_users(data)
    print("OK")
    print("DONE")

@sleepy_exit
@safe_exit
def unseed_database():
    print("Unseeding users")
    if(not os.environ.get('FIRESTORE_EMULATOR_HOST')):
      print("Deleting all user avatars... ", end="", flush=True)
      handler.delete_all_user_avatars()
      print("OK")
    print("Deleting all user data... ", end="", flush=True)
    handler.delete_all_users()
    print("OK")
    print("DONE")


@safe_exit
def get_recommendations():
    data = json.load(open("rec_settings.json"))

    if(not os.environ.get('FIRESTORE_EMULATOR_HOST')):
      rec_url = data["production_url"]
    else:
      rec_url = data["local_url"]

    payload = {
        "userId": input("Type a user ID: "),
        "recs": data["recs"]
    }

    response = requests.post(rec_url, json=payload)
    json_response = json.loads(response.text)

    print(json_response)

    input("Press Enter to go back... ")