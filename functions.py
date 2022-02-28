import json
from decorators import sleepy_exit, safe_exit
from generator import Generator
import firebase_admin
from firebase_admin import credentials, firestore
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
        firebase_admin.initialize_app(cred)

        self.db = firestore.client()

    def save_users(self, data):
        USER_DATA_REF = self.db.collection("users")
        split_size = min(self.BATCH_SIZE, len(data))

        for split in [data[i:i + split_size] for i in range(0, len(data), split_size)]:
            batch = self.db.batch()

            for user_data in split:
                batch.set(USER_DATA_REF.document(), user_data)

            batch.commit()

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
    print("Generating users... ", end="", flush=True)
    data = generator.generate()
    print("OK")
    print("Saving users to Firestore... ", end="", flush=True)
    handler.save_users(data)
    print("OK")
    print("DONE")

@sleepy_exit
@safe_exit
def unseed_database():
    print("Unseeding users")
    handler.delete_all_users()
    print("DONE")


@safe_exit
def get_recommendations():
    url = "http://localhost:5001/seg-djangoals/us-central1/getRecHTTPs"
    payload = {}

    payload["userId"] = input("Type a user ID: ")

    response = requests.post(url, json=payload)
    json_response = json.loads(response.text)

    print(json_response)

    input("Press Enter to go back... ")