# -*- coding: utf-8 -*-

import sqlite3 as sql
import os
from .data_resource import AbstractDataResource

class SqliteResource(AbstractDataResource):
    
    DB_NAME = "pycsgoinfo.db"

    INIT_MATCH_TABLE = """CREATE TABLE IF NOT EXISTS match (id INTEGER PRIMARY KEY, map TEXT);"""
    INIT_MATCH_PLAYERS_TABLE = """CREATE TABLE IF NOT EXISTS match_players_data (id INTEGER PRIMARY KEY, match_id INTEGER,
                        xuid TEXT, team_id INTEGER, kills NUMERIC, deaths NUMERIC, assists NUMERIC, headshots NUMERIC, 
                        mvps NUMERIC, weapon_fires NUMERIC, jumps NUMERIC, bombs_defused NUMERIC, 
                        bombs_planted NUMERIC, smokes NUMERIC, flashbangs NUMERIC, molotovs NUMERIC, 
                        grenades NUMERIC, decoys NUMERIC, name TEXT,
                        FOREIGN KEY(match_id) REFERENCES match(id));"""
    INIT_PLAYERS_TABLE = """CREATE TABLE IF NOT EXISTS players (id INTEGER PRIMARY KEY, xuid TEXT, kills NUMERIC, deaths NUMERIC, 
                        assists NUMERIC, headshots NUMERIC, mvps NUMERIC, weapon_fires NUMERIC, jumps NUMERIC, 
                        bombs_defused NUMERIC, bombs_planted NUMERIC, smokes NUMERIC, flashbangs NUMERIC, 
                        molotovs NUMERIC, grenades NUMERIC, decoys NUMERIC, name TEXT);"""

    def __init__(self):
        self.init_connection()
        self.match_id = 0
        c = self.conn.cursor()
        c.execute(self.INIT_MATCH_TABLE)
        c.execute(self.INIT_MATCH_PLAYERS_TABLE)
        c.execute(self.INIT_PLAYERS_TABLE)
        self.conn.commit()
        c.close()

    def __del__(self):
        self.conn.close()

    def init_connection(self):
        try:
            self.conn = sql.connect(self.DB_NAME)
            self.conn.text_factory = str
        except sql.Error, e:
            print("sqlite error: %s" % e.args[0])

    def addMatchData(self, match_data):
        try:
            c = self.conn.cursor()
            c.execute("""INSERT INTO match(map) VALUES(?)""", (match_data['map'],))
            self.match_id = c.lastrowid
            c.close()
            return self.match_id
        except sql.Error, e:
            print("sqlite error in addMatchData: %s" % e.args[0])


    def addPlayerData(self, player_data):
        try:
            c = self.conn.cursor()
            for pid in player_data:
                c.execute("""INSERT INTO match_players_data (match_id, xuid, team_id, kills, deaths, assists, headshots, mvps, weapon_fires, jumps, bombs_defused, bombs_planted,
                        smokes, flashbangs, molotovs, grenades, decoys, name) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (self.match_id, player_data[pid]['xuid'], player_data[pid]['team_id'], 
                            player_data[pid]['kills'], player_data[pid]['deaths'],  player_data[pid]['assists'],  player_data[pid]['headshots'],  player_data[pid]['round_mvp'],  
                            player_data[pid]['weapon_fire'], player_data[pid]['player_jump'],  player_data[pid]['bomb_defused'],  player_data[pid]['bomb_planted'],  player_data[pid]['smokegrenade'], 
                            player_data[pid]['flashbang'],  player_data[pid]['firegrenade'],  player_data[pid]['hegrenade'],  player_data[pid]['decoy'], player_data[pid]['name']))
            self.conn.commit()
            c.close()
        except sql.Error, e:
            print("sqlite error in addPlayerData: %s" % e.args[0])
