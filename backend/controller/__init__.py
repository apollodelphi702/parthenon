from app import CoreApplication
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
        self.api: CoreAPI = CoreAPI(self)
        """The CoreAPI instance that should be used to pass actions between the engines."""

        self.app: CoreApplication = CoreApplication(name='Parthenon')
        """The application instance for configuration and logging"""

        # ...
        # Now load the active implementations specified in the constructor.
        # ...

        self.data_storage: BaseDataStorageEngine = data_storage
        """The active Data Storage Engine Implementation (DSEI) that should be used to store data."""
        data_storage.bind(self)
        if not data_storage.start():
            self.app.logger.error('Failed to start data storage engine')
            exit(1)

        self.ingestion: BaseIngestionEngine = ingestion
        """
        The active Ingestion Engine Implementation (IEI) that should be used to fetch data from the upstream data
        source.
        """
        ingestion.bind(self)
        if not ingestion.start():
            self.app.logger.error('Failed to start ingestion engine')
            exit(1)

    def shutdown(self):
        self.app.logger.info('Shutting down...')
        self.data_storage.stop()
        self.ingestion.stop()
        self.app.logger.info('Terminating...')
        exit(0)

