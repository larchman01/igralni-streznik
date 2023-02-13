# -*- coding: utf-8 -*-
import logging
import random
from typing import Dict, List
from uuid import uuid4

import gevent
from flask_restx import Api, fields

from sledilnik.classes.Field import Field
from sledilnik.classes.ObjectTracker import ObjectTracker
from src.classes.StateLiveData import StateLiveData
from src.classes.Team import Team
from src.classes.Timer import Timer
from src.servers.Server import Server
from src.servers.StateServer import StateServer


class GameServer(Server):
    """Game state for particular game

    Pulls information from a state server and computers a game state.

    Attributes:
        id (UUID): Game id
        key (string): Key for write permissions
    """

    def __init__(self, state_server: StateServer, game_config: Dict, teams: List[int]):
        Server.__init__(self)

        self.logger = logging.getLogger('servers.GameServer')
        self.config = game_config

        self.state_server: StateServer = state_server
        self.id: str = str(uuid4())[:4]
        self.key: str = "very_secret_key"

        self.game_on: bool = False
        self.game_paused: bool = False

        self.game_time: int = game_config['game_time']
        self.timer = Timer()

        self.teams: Dict[int, Team] = {}
        self.set_teams(teams)

    def _run(self):
        self.logger.info("Started a new game server with id: %s" % self.id)
        while True:
            # Wait for state server to update state
            self.state_server.updated.wait()
            self.state_data: StateLiveData = self.state_server.state

            # print(self.id, self.gameData.gameOn)
            if self.game_on and not self.game_paused:
                self.update_game_state()

                # stop the game when no time left
                if self.timer.get() <= 0:
                    self.game_on = False
                    break

            self.updated.set()
            gevent.sleep(0.01)
            self.updated.clear()

    def update_game_state(self):
        """
        Needs to me implemented by extending class
        """
        for team in self.teams:
            team.score = random.randint(-100, 100)

    def set_teams(self, teams: List[int]):
        colors = ['blue', 'red']
        self.teams = {team: self.init_team(team, color) for team, color in zip(teams, colors)}

    def init_team(self, robot_id: int, color: str):
        if robot_id in self.config['robots']:
            return Team(robot_id, color, self.config['robots'][robot_id])
        else:
            logging.error("Team with specified id does not exist in config!")
            raise Exception("Team with specified id does not exist in config!")

    def alter_score(self, team_1_score: int, team_2_score: int):
        self.teams[team_1_score].score_bias = team_1_score
        self.teams[team_2_score].score_bias = team_2_score

    def start_game(self):
        if not self.game_on:
            for team in self.teams.values():
                team.score = 0

            self.timer.start()
            self.game_on = True
            self.game_paused = False

    def pause_game(self):
        if self.game_on and not self.game_paused:
            self.timer.pause()
            self.game_paused = True

    def resume_game(self):
        if self.game_on and self.game_paused:
            self.timer.resume()
            self.game_paused = False

    def stop_game(self):
        self.game_on = False

    def set_game_time(self, game_time: int):
        self.game_time = game_time

    def to_json(self):
        return {
            'id': self.id,
            'game_on': self.game_on,
            'game_paused': self.game_paused,
            'time_left': self.game_time - self.timer.get(),
            'teams': {str(t.robot_id): t.to_json() for t in self.teams.values()},
            'robots': {str(r.id): r.to_json() for r in self.state_data.robots.values()},
            'objects': {
                str(ot): {
                    str(o.id): o.to_json() for o in self.state_data.objects[ot].values()
                } for ot in self.state_data.objects
            },
            'fields': {f_name: f.to_json() for f_name, f in self.state_data.fields.items()}
        }

    @classmethod
    def to_model(cls, api: Api, game_config: Dict):
        return api.model('GameServer', {
            'id': fields.String,
            'game_on': fields.Boolean,
            'game_paused': fields.Boolean,
            'time_left': fields.Float,
            'teams': fields.Nested(api.model(
                'Teams',
                {str(t): fields.Nested(Team.to_model(api)) for t in game_config['robots']})
            ),
            'robots': fields.Nested(api.model(
                'Robots',
                {str(r): fields.Nested(ObjectTracker.to_model(api), required=False) for r in game_config['robots']})
            ),
            'objects': fields.Nested(
                api.model(
                    'Objects',
                    {str(ot): fields.Nested(
                        api.model(
                            'ObjectType',
                            {
                                str(o): fields.Nested(ObjectTracker.to_model(api), required=False)
                                for o in game_config['objects'][ot]
                            }
                        )
                    ) for ot in game_config['objects']}
                )
            ),
            'fields': fields.Nested(api.model(
                'Fields',
                {f: fields.Nested(Field.to_model(api), required=False) for f in game_config['fields_names']})
            )
        })