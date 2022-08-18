from datetime import date
from typing import Optional

from structs import BatchEntry
from enums import ValidationStatus


class Batch:
    """
    Represents a batch of entries (file) as well as the validation status of that file.
    """

    def __init__(self, filename: str, file_hash: str, timestamp: date):
        self.filename = filename
        """The original filename that the data is from."""

        self.file_hash = file_hash
        """The hash of the original file."""

        self.timestamp = timestamp
        """The timestamp from the filename."""

        self.entries: dict[int, BatchEntry] = {}
        """The list of entries from the batch, keyed by the batch_id."""

        self.validation_status: ValidationStatus = ValidationStatus.VALID
        """The status of the batch during validation"""

        self.batch_validation_messages: dict[int, str] = {}
        """The list of validation messages per batch entry"""

        self.validation_messages: list[str] = []
        """The list of validation messages for the entire file"""

    @property
    def row_count(self):
        return len(self.entries)

    def set_validation_status(self, status: ValidationStatus):
        # Add the status if and only if it is more severe.
        if status > self.validation_status:
            self.validation_status = status

    def add_validation_message(self, validation_message: str):
        self.validation_messages.append(validation_message)

    def add_batch_validation_message(self, batch_id: int, validation_message: str):
        if batch_id not in self.batch_validation_messages:
            self.batch_validation_messages[batch_id] = validation_message

    def add_entry(self, entry: BatchEntry) -> Optional[str]:
        """
        Insert an entry into the current batch.
        :param entry: The batch entry
        :return: The error message if there is one, otherwise nothing.
        """

        if entry.batch_id in self.entries:
            self.set_validation_status(ValidationStatus.BATCH_ID_DUPLICATES)
            self.add_batch_validation_message(entry.batch_id, f"Found duplicate for batch id: {entry.batch_id}")
            return self.batch_validation_messages[entry.batch_id]
        else:
            self.entries[entry.batch_id] = entry
            return None

    def remove_entry(self, batch_id: int):
        """
        Remove an entry by its batch ID.
        :param batch_id: The batch ID to remove.
        """

        if batch_id in self.entries:
            del self.entries[batch_id]
