from datetime import time


class BatchEntry:
    """
    Represents an individual entry (row) within a batch (file).
    """

    def __init__(self,
                 batch_id: int,
                 timestamp: time,
                 reading1: str,
                 reading2: str,
                 reading3: str,
                 reading4: str,
                 reading5: str,
                 reading6: str,
                 reading7: str,
                 reading8: str,
                 reading9: str,
                 reading10: str):
        self.batch_id: int = batch_id
        """The ID of the entry within the batch."""

        self.timestamp: time = timestamp
        """The date and time of the entry"""

        # The readings from the source file, stored here as strings to preserve precision.
        # If desired, they could then be converted to floats trivially by the API.

        self.reading1: str = reading1
        self.reading2: str = reading2
        self.reading3: str = reading3
        self.reading4: str = reading4
        self.reading5: str = reading5
        self.reading6: str = reading6
        self.reading7: str = reading7
        self.reading8: str = reading8
        self.reading9: str = reading9
        self.reading10: str = reading10
