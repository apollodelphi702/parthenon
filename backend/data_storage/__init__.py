from abc import ABC, abstractmethod
from typing import Optional, TYPE_CHECKING

from structs import Batch

if TYPE_CHECKING:
    from controller import CoreController


class BaseDataStorageEngine(ABC):
    """Base class for the data storage engine. (Set of methods responsible for storing and retrieving the data)"""

    def __init__(self):
        self.controller: Optional['CoreController'] = None

    def bind(self, controller: 'CoreController'):
        self.controller = controller

    @abstractmethod
    def start(self) -> bool:
        """
        Can be used by the service implementation to set up services.
        Remote services can be connected to here if they're long connections (i.e., if the connection stays
        open for the entire duration the backend application is running).
        """
        pass

    @abstractmethod
    def stop(self):
        """
        Can be used by the service implementation to tear down the services.
        """
        pass

    @abstractmethod
    def load_dataset_indexes(self):
        """Loads indexes for the entire dataset."""
        pass

    @abstractmethod
    def load_data(self):
        """Fetches a single entry (i.e., a single timestamp file)."""
        pass

    @abstractmethod
    def load_data_range(self):
        """Fetches entries within the specified range."""
        pass

    @abstractmethod
    def store_dataset(self, batches: list[Batch]):
        """
        Stores the entire dataset specified. This is called indirectly by the ingestion engine to refresh the data
        stored on the server.
        """
        pass
