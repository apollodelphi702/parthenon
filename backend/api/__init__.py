from controller import CoreController


class CoreAPI:
    """Contains implementation methods that would be called by an 'API' frontend."""

    def __init__(self, controller: CoreController):
        self.controller = controller
        """The API controller that should be used to pass events to and source engine implementations from."""

    def synchronize(self):
        """Uses the ingestion engine to synchronize the source data from the upstream server and then validate it."""
        self.controller.app.logger.info("Synchronizing dataset...")
        self.controller.data_storage.store_dataset(
            self.controller.ingestion.fetch_data()
        )
        self.controller.app.logger.info("Finished synchronizing dataset...")

    def fetch_index(self):
        """Fetches the file index from the server."""
        pass

    def fetch_file(self):
        """Fetches a single file from the server."""
        pass

    def fetch_file_range(self):
        """Fetches a list of files within the specified date range."""
        pass
