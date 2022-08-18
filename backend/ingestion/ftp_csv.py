import csv
from hashlib import sha256
from typing import Optional

from validation import StaticValidation
from . import BaseIngestionEngine
from structs import Batch
from enums import ValidationStatus
from ftplib import FTP_TLS, FTP


class FTPIngestionEngine(BaseIngestionEngine):
    """An ingestion engine that fetches CSV data from an FTP server."""

    def __init__(self, hostname: str, port: int, directory: str, secure: bool):
        super().__init__()

        self.hostname = hostname
        """The hostname of the FTP server to fetch the data from."""

        self.port = port
        """The port that should be used to communicate with the FTP server."""

        self.directory = directory
        """The directory containing the CSV files"""

        self.secure = secure
        """Whether secure FTP (over TLS) should be used"""

        self.client = None
        if self.secure:
            self.client = FTP_TLS()
        else:
            self.client = FTP()

    def start(self) -> bool:
        self.controller.app.logger.info(
            'Starting FTP Ingestion engine (testing connection). Remote server: {}:{}',
            self.hostname, self.port
        )

        # Attempt to connect to the FTP server to test the connection.
        try:
            self.client.connect(host=self.hostname, port=self.port)
        except ConnectionRefusedError:
            self.controller.app.logger.error('Failed to communicate with the FTP server (connection refused).')
            return False

        # Now, close the connection with QUIT - we open it as needed to fetch data.
        # If we close the connection with close, the FTP client is rendered unusable for subsequent connections.
        self.client.quit()
        return True

    def fetch_data(self) -> Optional[list[Batch]]:
        self.controller.app.logger.info('Fetching data from server...')

        try:
            # Connect to the server
            self.client.connect(host=self.hostname, port=self.port)

            # Log in (anonymously)
            self.client.login()

            if self.secure:
                self.client.prot_p()

            # Open the directory and list the files
            self.client.cwd(self.directory)
            files = self.client.nlst()

            # Filter files where they end in '.csv'
            files = list(filter(lambda file_to_test: file_to_test.endswith('.csv'), files))
            self.controller.app.logger.info('Located {} CSV file(s) – Validating...', len(files))

            batches = []

            for filename in files:
                file, digest = self.fetch_file(filename)
                batch = self.decode_file(file=file, filename=filename, digest=digest)
                if batch:
                    batches.append(batch)

            self.controller.app.logger.info('Processing data from {} valid CSV file(s) - Synchronizing...', len(batches))

            # Close the connection
            self.client.quit()

            # Return the fetched data.
            return batches

        except ConnectionRefusedError:
            self.controller.app.logger.error('Failed to fetch data from server.')
            return None

    def stop(self):
        self.client.close()
        self.controller.app.logger.info('Closed connection to FTP server')

    def fetch_file(self, filename) -> (list[str], str):
        """
        Fetches the contents of the specified filename from the FTP server
        :returns: A list of strings - where each string is a line in the file.
        """

        lines = []
        hasher = sha256()

        self.controller.app.logger.info('Fetching file: {}', filename)
        self.client.retrlines(
            f'RETR {filename}',
            lambda line: (
                hasher.update(line.encode('utf-8')),
                lines.append(line))
        )

        return lines, hasher.hexdigest()

    def decode_file(self, filename: str, file: list[str], digest: str) -> Optional[Batch]:
        """
        Decode the data from a CSV file into an application structure
        """
        reader = csv.reader(file)
        # TODO: read timestamp from filename
        batch: Batch = Batch(filename, digest, None)

        headers = None
        row_index = 0

        for row in reader:
            row_index += 1

            # Process headers.
            if headers is None:
                if StaticValidation.validate_headers(self.controller, batch, filename, row):
                    headers = row
                    continue
                else:
                    self.controller.app.logger.info("Finished processing (error): {}", filename)
                    return None

            # Process values
            if not StaticValidation.validate_row(self.controller, batch, filename, row, row_index):
                if int(batch.validation_status) >= ValidationStatus.critical:
                    self.controller.app.logger.info("Finished processing (error): {}", filename)
                    return None

        self.controller.app.logger.info('Finished processing (success): {}; found {} row(s)', filename, batch.row_count)
        return batch
