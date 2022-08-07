from data_storage import BaseDataStorageEngine
from ingestion import BaseIngestionEngine


class CoreController:

    def __init__(
            self,
            data_storage: BaseDataStorageEngine,
            ingestion: BaseIngestionEngine
    ):
        # Import API when needed.
        # (This helps prevent cyclic dependency issue too).
        from api import CoreAPI

        # Initialize CoreAPI with this controller.
        # The controller serves as the state management for the application, whereas CoreAPI serves as a
        # 'messenger bus'.
        self.api = CoreAPI(self)
        """The CoreAPI instance that should be used to pass actions between the engines."""

        # ...
        # Now load the active implementations specified in the constructor.
        # ...

        self.data_storage = data_storage
        """The active Data Storage Engine Implementation (DSEI) that should be used to store data."""

        self.ingestion = ingestion
        """
        The active Ingestion Engine Implementation (IEI) that should be used to fetch data from the upstream data
        source.
        """
