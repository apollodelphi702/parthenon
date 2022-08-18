from abc import ABC, abstractmethod
from typing import Optional, TYPE_CHECKING

from structs import Batch

if TYPE_CHECKING:
    from controller import CoreController


class BaseIngestionEngine(ABC):
    """Base class for an ingestion engine. (Set of methods capable of importing data from a remote server)"""

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
    def fetch_data(self) -> Optional[list[Batch]]:
        """
        Connects to the server and fetches the raw data.
        The data is then passed through the Core Validation library which validates the entries and returns
        structured data along with a list of validation results.
        :return:
        """
        pass
