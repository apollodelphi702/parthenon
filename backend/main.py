#!/usr/bin/env python3
from controller import CoreController
from api.parthenon_encrypted_socket_api import ParthenonEncryptedSocketAPI
from data_storage.parthenon_dsei import ParthenonDSEI
from ingestion.ftp_csv import FTPIngestionEngine


def main():
    # Initialize the controller
    controller = CoreController(
        data_storage=ParthenonDSEI(),
        ingestion=FTPIngestionEngine(
            # TODO: load these from config
            hostname='127.0.0.1',
            port=21
        )
    )

    # Initialize the API frontend with the controller so we can start accepting requests
    api_frontend = ParthenonEncryptedSocketAPI(
        controller=controller
    )


if __name__ == '__main__':
    main()
