#!/usr/bin/env python3
from controller import CoreController
from api.parthenon_encrypted_socket_api import ParthenonEncryptedSocketAPI
from data_storage.parthenon_dsei import ParthenonDSEI
from ingestion.ftp_csv import FTPIngestionEngine
from structs import Batch


def handle_shutdown():
    if controller:
        controller.shutdown()

    if api_frontend:
        api_frontend.stop()


if __name__ == '__main__':
    controller = None
    api_frontend = None

    try:
        # Initialize the controller
        controller = CoreController(
            data_storage=ParthenonDSEI(
                path='./_data/'
            ),
            ingestion=FTPIngestionEngine(
                # TODO: load these from config
                hostname='127.0.0.1',
                port=2121,
                directory='/',
                secure=False
            )
        )

        # Initialize the API frontend with the controller so we can start accepting requests
        api_frontend = ParthenonEncryptedSocketAPI(
            controller=controller
        )
        api_frontend.start()

        # TODO: host server
        batches: list[Batch] = controller.data_storage.load_data()
        handle_shutdown()

    except KeyboardInterrupt:
        handle_shutdown()
