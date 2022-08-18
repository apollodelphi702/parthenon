import base64
import os.path

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes

from structs import Batch
from . import BaseDataStorageEngine

import pickle
from getpass import getpass

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class ParthenonDSEI(BaseDataStorageEngine):
    storage_key = None
    """The storage key for the files"""

    salt = None
    """The salt used for key-derivation"""

    fernet: Fernet = None

    def __init__(self, path: str):
        super().__init__()
        self.path = path

    def start(self) -> bool:
        if not os.path.isdir(self.path):
            self.controller.app.logger.error("Data Storage Engine directory does not exist: {}", self.path)
            return False

        # If the sentinel exists, use it to read parameters.
        sentinel = None
        if os.path.isfile(os.path.join(self.path, 'sentinel.pno')):
            with open(os.path.join(self.path, 'sentinel.pno'), 'rb') as sentinel:
                sentinels = sentinel.read().split(b'\0')
                self.salt = sentinels[0]
                sentinel = sentinels[1]

        # Otherwise delete all the files in the data directory and enter set up.
        else:
            for file in os.listdir(self.path):
                os.remove(os.path.join(self.path, file))

        if self.salt is None:
            self.salt = os.urandom(64)

        key_derive = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=600000
        )

        if sentinel is None:
            new_storage_key = getpass("Enter (new) storage key: ").encode('UTF-8')
            while getpass("Confirm (new) storage key: ").encode('UTF-8') != new_storage_key:
                print("The confirmation security key must match the new security key!")
                new_storage_key = getpass("Enter (new) storage key: ").encode('UTF-8')

            self.storage_key = base64.urlsafe_b64encode(
                key_derive.derive(new_storage_key)
            )

        if not self.storage_key:
            self.storage_key = base64.urlsafe_b64encode(key_derive.derive(getpass("Enter storage key: ").encode('UTF-8')))
        self.fernet = Fernet(self.storage_key)

        if sentinel is not None:
            try:
                if self.fernet.decrypt(sentinel) != b'sentinel':
                    raise InvalidToken
            except InvalidToken:
                self.controller.app.logger.error(
                    "Invalid storage key. If you're setting up the application, delete {} if it exists. "
                    "Otherwise, please restart the application and enter the correct storage key.",
                    os.path.join(self.path, 'sentinel.pno')
                )
                return False

        return True

    def stop(self):
        pass

    def load_dataset_indexes(self):
        pass

    def has_existing_data(self):
        return os.path.isfile(os.path.join(self.path, 'dataset.pno'))

    def load_data(self) -> list[Batch]:
        # If we don't have any data, trigger a synchronize, otherwise
        # use the cached data.
        if not self.has_existing_data():
            self.controller.api.synchronize()

        self.controller.app.logger.info("Loading dataset...")

        with open(os.path.join(self.path, 'dataset.pno'), 'rb') as file:
            file_data = self.fernet.decrypt(file.read())
            batches = pickle.loads(file_data)

            self.controller.app.logger.info("Finished loading dataset.")
            return batches

    def load_data_range(self):
        pass

    def store_dataset(self, batches: list[Batch]):
        self.controller.app.logger.info("Storing dataset...")
        raw_file_data = pickle.dumps(batches)
        file_data = self.fernet.encrypt(raw_file_data)

        with(open(os.path.join(self.path, 'sentinel.pno'), 'wb')) as file:
            file.write(self.salt)
            file.write(b'\0')
            file.write(self.fernet.encrypt(b'sentinel'))

        self.controller.app.logger.info("Writing dataset to file...")
        with open(os.path.join(self.path, 'dataset.pno'), 'wb') as file:
            file.write(file_data)
        self.controller.app.logger.info("Finished storing dataset.")
