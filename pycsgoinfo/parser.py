import subprocess
import os
#import sqlite3 as sql

class Parser(object):

    # path to data file dumped by demoinfogo
    dat_file = os.path.dirname(os.path.realpath(__file__)) + "/dat/demo.dat"
    # path to demoinfogo executable
    path_to_demoinfogo = os.path.dirname(os.path.realpath(__file__)) + "/lib/demoinfogo"

    # parsing keys
    match_start = "round_announce_match_start"
    player_info = "player info"
    player_spawn = "player_spawn"
    weapon_fire = "weapon_fire"
    player_jump = "player_jump"
    player_death = "player_death"
    round_mvp = "round_mvp"
    bomb_defused = "bomb_defused"
    bomb_planted = "bomb_planted"
    kills = "kills"
    assists = "assists"
    deaths = "deaths"
    team_id = "team_id"
    headshots = "headshots"
    xuid = "xuid"

    def __init__(self, demo_file):
        self.demo_file = demo_file
        self.command = str(self.path_to_demoinfogo) + ' -gameevents -nofootsteps -stringtables ' + str(self.demo_file)
        self._call_demoinfogo()
        self._parse_file()
        print(self.parsed_data)

    def _call_demoinfogo(self):
        ''' Calls demoinfogo with the demo file provided in the constructor '''
        with open(self.dat_file, "w+") as f:
            p = subprocess.Popen(self.command, shell=True, stdin=subprocess.PIPE, stdout = f)
            print("Dumping demo to data file. Please wait.")
            return_code = p.wait()
            print("Dumping process finished.")
            f.flush()
        

    def _parse_file(self):
        ''' Parses the data file dumped by demoinfogo.
            Adds the data to a dictionary '''
        self.parsed_data = {}
        warmup_skipped = False
        with open(self.dat_file, "r") as f:
            lines = f.readlines()
            # use indexes for handier parsing
            for i in range(0, len(lines)):
                line = lines[i]
                if warmup_skipped is True:
                    # find weapon fire events - TODO don't include grenades or knives
                    if line.find(self.weapon_fire) > -1:
                        user_id = self._get_user(lines[i+2])
                        if user_id not in self.parsed_data:
                            self._init_userdata(user_id)
                            
                        self.parsed_data[user_id][self.weapon_fire] += 1
                        # skip next five indexes
                        i = i + 5
                    # find player jump events
                    if line.find(self.player_jump) > -1:
                        user_id = self._get_user(lines[i+2])
                        if user_id not in self.parsed_data:
                            self._init_userdata(user_id)
                            
                        self.parsed_data[user_id][self.player_jump] += 1
                        i = i + 3
                    # find player death events
                    if line.find(self.player_death) > -1:
                        user_id = self._get_user(lines[i+2])
                        attacker = self._get_user(lines[i+3])
                        assister = self._get_user(lines[i+4])
                        if user_id not in self.parsed_data:
                            self._init_userdata(user_id)
                        if attacker not in self.parsed_data:
                            self._init_userdata(attacker)
                        if assister is not "0":
                            if assister not in self.parsed_data:
                                self._init_userdata(assister)
                            self.parsed_data[assister][self.assists] += 1
                        # get head shot
                        hs = int(lines[i+9].split()[1])
                        if hs == 1:
                            self.parsed_data[attacker][self.headshots] += 1
                        self.parsed_data[user_id][self.deaths] += 1
                        self.parsed_data[attacker][self.kills] += 1
                else:
                    if line.find(self.player_info) == 0:
                        is_fake = int(lines[i+9].split(":")[1].rstrip())
                        is_hltv = int(lines[i+10].split(":")[1].rstrip())
                        user_id = lines[i+4].split(":")[1].rstrip()
                        if user_id not in self.parsed_data and is_fake is 0 and is_hltv is 0:
                            self._init_userdata(user_id)
                        if is_fake is 0 and is_hltv is 0:
                            xuid = lines[i+3].split(":")[1].rstrip()
                            self.parsed_data[user_id][self.xuid] = xuid
                    if line.find(self.player_spawn) > -1:
                        user_id = self._get_user(lines[i+2])
                        if user_id not in self.parsed_data:
                            self._init_userdata(user_id)
                        teamnum = int(lines[i+3].split()[1])
                        self.parsed_data[user_id][self.team_id] = teamnum
                    if line.find(self.match_start) > -1:
                        warmup_skipped = True
                        i = i + 2

    def _get_user(self, line):
        ''' Finds a users name from the provided line '''
        user_id = line.split(" ")[2:-1]
        return ' '.join(user_id)

    def _init_userdata(self, user_id):
        ''' Initializes user data in the parse-dictionary '''
        if user_id not in self.parsed_data:
            self.parsed_data[user_id] = {
                    self.xuid: "",
                    self.weapon_fire: 0,
                    self.player_jump: 0,
                    self.kills: 0,
                    self.deaths: 0,
                    self.assists: 0,
                    self.team_id: 0,
                    self.headshots: 0
            }

