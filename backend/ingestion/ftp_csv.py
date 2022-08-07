from . import BaseIngestionEngine


class FTPIngestionEngine(BaseIngestionEngine):
    """An ingestion engine that fetches CSV data from an FTP server."""

    def __init__(self, hostname: str, port: int):
        self.hostname = hostname
        """The hostname of the FTP server to fetch the data from."""

        self.port = port
        """The port that should be used to communicate with the FTP server."""

    def fetch_data(self):
        pass
