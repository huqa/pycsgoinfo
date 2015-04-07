# -*- coding: utf-8 -*-

class AbstractDataResource(object):
    """ Abstract class for data resources """

    def addMatchData(self, match_data):
        raise NotImplementedError("Implement the addMatchData method")

    def addPlayerData(self, player_data):
        raise NotImplementedError("Implement the addPlayerData method")
