from abc import ABC, abstractmethod


class BaseDataStorageEngine(ABC):
    """Base class for the data storage engine. (Set of methods responsible for storing and retrieving the data)"""

    @abstractmethod
    def load_dataset_indexes(self):
        """Loads indexes for the entire dataset."""

    @abstractmethod
    def load_data(self):
        """Fetches a single entry (i.e., a single timestamp file)."""

    def load_data_range(self):
        """Fetches entries within the specified range."""

    @abstractmethod
    def store_dataset(self):
        """
        Stores the entire dataset specified. This is called indirectly by the ingestion engine to refresh the data
        stored on the server.
        """
        pass
