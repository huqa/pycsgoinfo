import sqlite3 as sql
import os

class SqliteResource(AbstractDataResource):
    
    DB_NAME = "pycsgoinfo.db"

    INIT_STRING = "BEGIN TRANSACTION;
                    CREATE TABLE IF NOT EXISTS match (id INTEGER PRIMARY KEY, map TEXT);
                    CREATE TABLE IF NOT EXISTS match_players_data (id INTEGER PRIMARY KEY, match_id INTEGER,
                        xuid TEXT, team_id INTEGER, kills NUMERIC, deaths NUMERIC, assists NUMERIC, headshots NUMERIC, 
                        mvps NUMERIC, weapon_fires NUMERIC, jumps NUMERIC, bombs_defused NUMERIC, 
                        bombs_planted NUMERIC, smokes NUMERIC, flashbangs NUMERIC, molotovs NUMERIC, 
                        grenades NUMERIC, decoys NUMERIC, name TEXT,
                        FOREIGN KEY(match_id) REFERENCES match(id));
                    CREATE TABLE IF NOT EXISTS players (id INTEGER PRIMARY KEY, xuid TEXT, kills NUMERIC, deaths NUMERIC, 
                        assists NUMERIC, headshots NUMERIC, mvps NUMERIC, weapon_fires NUMERIC, jumps NUMERIC, 
                        bombs_defused NUMERIC, bombs_planted NUMERIC, smokes NUMERIC, flashbangs NUMERIC, 
                        molotovs NUMERIC, grenades NUMERIC, decoys NUMERIC, name TEXT);
                    COMMIT;"

    def __init__(self):
        self.init_connection()
        db_exists = os.path.exists(self.DB_NAME)
        if not db_exists:
            c = self.conn.cursor()
            c.execute(self.INIT_STRING)
            self.conn.commit()
            c.close()

    def __del__(self):
        self.conn.close()

    def init_connection(self):
        try:
            self.conn = sql.connect(self.DB_NAME)
        except sql.Error, e:
            print("sqlite error: %s" % e.args[0])

    def addMatchData(self, match_data):
        try:
            c = self.conn.cursor()
            c.execute('''INSERT INTO match(map) VALUES(?)''', (match_data['map']))
            self.map_id = c.lastrowid
            c.close()
        except sql.Error, e:
            print("sqlite error: %s" % e.args[0])


    def addPlayerData(self, player_data):
        try:
            c = self.conn.cursor()
            for name in player_data:
                c.execute('''INSERT INTO match_players_data (match_id, xuid, team_id, kills, deaths, assists, headshots, mvps, weapon_fires, jumps, bombs_defused, bombs_planted,
                        smokes, flashbangs, molotovs, grenades, decoys, name) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (self.map_id, player_data[name]['xuid'],   player_data[name]['team_id'], 
                            player_data[name]['kills'], player_data[name]['deaths'],  player_data[name]['assists'],  player_data[name]['headshots'],  player_data[name]['round_mvp'],  
                            player_data[name]['weapon_fire'], player_data[name]['player_jump'],  player_data[name]['bomb_defused'],  player_data[name]['bomb_planted'],  player_data[name]['smokegrenade'], 
                            player_data[name]['flashbang'],  player_data[name]['firegrenade'],  player_data[name]['hegrenade'],  player_data[name]['decoy'], name))
            self.conn.commit()
            c.close()
        except sql.Error, e:
            print("sqlite error: %s" % e.args[0])
