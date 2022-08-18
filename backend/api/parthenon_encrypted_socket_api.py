from controller import CoreController


class ParthenonEncryptedSocketAPI:
    """Communicates with the server over encrypted sockets."""

    def __init__(self, controller: CoreController):
        self.controller = controller

    def start(self):
        """Start listening for requests and set up API."""

    def stop(self):
        """Stop listening for requests and tear down API."""
