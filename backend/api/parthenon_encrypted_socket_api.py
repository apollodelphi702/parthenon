from controller import CoreController


class ParthenonEncryptedSocketAPI:
    """Communicates with the server over encrypted sockets."""

    def __init__(self, controller: CoreController):
        self.controller = controller
