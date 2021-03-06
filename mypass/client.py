# Copyright (c) 2014 Sebastian Noack
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

import os
import socket
import pickle

from mypass import Error, ConnectionLost, SOCKET
from mypass.config import config, check_config_errors


class Client:
    DATABASE_DOES_NOT_EXIST = 1
    DATABASE_LOCKED = 2
    DATABASE_UNLOCKED = 3

    if hasattr(socket, 'AF_UNIX') and hasattr(os, 'fork') and not config['daemon']['disabled']:
        def __init__(self):
            check_config_errors()

            try:
                self._connect()
            except FileNotFoundError:
                self._read_database()

        def _connect(self):
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

            try:
                sock.connect(SOCKET)
            except:
                sock.close()
                raise

            self._socket = sock
            self.status = self.DATABASE_UNLOCKED

        def _set_database(self, db):
            from mypass.daemon import spawn_daemon
            spawn_daemon(db)
            self._connect()

        def call(self, command, *args):
            with self._socket.makefile('rwb', 0) as file:
                try:
                    pickle.dump((command, args), file)
                    output = pickle.load(file)
                except (BrokenPipeError, EOFError):
                    raise ConnectionLost

            if isinstance(output, Error):
                raise output

            return output
    else:
        def __init__(self):
            check_config_errors()
            self._read_database()

        def _set_database(self, db):
            self._db = db
            self.status = self.DATABASE_UNLOCKED

        def call(self, command, *args):
            return getattr(self._db, command.replace('-', '_'))(*args)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def _read_database(self):
        try:
            with open(config['database']['path'], 'rb') as file:
                self._ciphertext = file.read()
        except FileNotFoundError:
            self.status = self.DATABASE_DOES_NOT_EXIST
        else:
            self.status = self.DATABASE_LOCKED

    def create_database(self, passphrase):
        from mypass.storage import Database
        self._set_database(Database.create(passphrase))

    def unlock_database(self, passphrase):
        from mypass.storage import Database
        db = Database.decrypt(self._ciphertext, passphrase)
        del self._ciphertext
        self._set_database(db)

    def close(self):
        sock = getattr(self, '_socket', None)
        if sock:
            sock.close()
