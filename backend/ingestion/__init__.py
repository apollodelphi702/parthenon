from abc import ABC, abstractmethod


class BaseIngestionEngine(ABC):
    """Base class for an ingestion engine. (Set of methods capable of importing data from a remote server)"""

    @abstractmethod
    def fetch_data(self):
        """
        Connects to the server and fetches the raw data.
        The data is then passed through the Core Validation library which validates the entries and returns
        structured data along with a list of validation results.
        :return:
        """
        pass
