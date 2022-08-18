#!/usr/bin/env python3
from pyftpdlib import servers
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.authorizers import DummyAuthorizer


def main():
    authorizer = DummyAuthorizer()
    authorizer.add_anonymous('../test_csv_files', msg_login="You may need to use active mode.")

    handler = FTPHandler
    handler.authorizer = authorizer

    # Uncomment to specify passive port range:
    # handler.passive_ports = range(2121, 2142)

    # Can be changed to 21 but ports < 1024 require elevated permissions on *nix-like systems.
    address = ('127.0.0.1', 2121)
    server = servers.FTPServer(address, handler)
    server.serve_forever()


if __name__ == '__main__':
    main()
