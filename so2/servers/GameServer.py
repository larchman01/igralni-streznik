# -*- coding: utf-8 -*-

from uuid import uuid1

import gevent

from so2.servers.Server import Server


class GameServer(Server):
    """Game state for particular game

    Pulls information from a state server and computers a game state.

    Attributes:
        id (UUID): Game id
        key (string): Key for write permissions
    """

    def __init__(self, state_server):
        Server.__init__(self)
        self.state_server = state_server
        self.id = uuid1()
        self.key = "very_secret_key"

    def _run(self):
        while True:
            # Wait for state server to update state
            self.state_server.updated.wait()
            # Update game from state

            self.game = self.state_server.value

            gevent.sleep(0.01)
