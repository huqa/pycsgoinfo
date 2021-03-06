# -*- coding: utf-8 -*-
import subprocess
import os
from .sqlite_resource import SqliteResource

class Parser(object):

    # path to data file dumped by demoinfogo
    dat_file = os.path.dirname(os.path.realpath(__file__)) + "/dat/demo.dat"
    # path to demoinfogo executable
    path_to_demoinfogo = os.path.dirname(os.path.realpath(__file__)) + "/lib/demoinfogo"

    # parsing keys
    match_start = "round_announce_match_start"
    player_info = "player info"
    player_spawn = "player_spawn"
    player_team = "player_team"
    adding_player = "adding:player info:"
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
    name = "name"

    knife = "knife"

    # grenade weapons 
    smoke = "smokegrenade"
    flash = "flashbang"
    hegrenade = "hegrenade"
    molotov = "molotov"
    incgrenade = "incgrenade"
    decoy = "decoy"
    fire = "firegrenade"

    grenades = [
        smoke,
        flash,
        hegrenade,
        molotov,
        incgrenade,
        decoy
    ]

    def __init__(self, demo_file):
        self.demo_file = demo_file
        self.command = str(self.path_to_demoinfogo) + ' -gameevents -nofootsteps -stringtables ' + str(self.demo_file)
        self._call_demoinfogo()
        self._parse_playerdata()
        #print(self.match_data)
        data_res = SqliteResource()
        self.match_id = data_res.addMatchData(self.match_data)
        data_res.addPlayerData(self.player_data)
        #print(self.player_data)

    def get_match_id(self):
        return self.match_id

    def _call_demoinfogo(self):
        ''' Calls demoinfogo with the demo file provided in the constructor '''
        with open(self.dat_file, "w+") as f:
            p = subprocess.Popen(self.command, shell=True, stdin=subprocess.PIPE, stdout = f)
            print("Dumping demo to data file. Please wait.")
            return_code = p.wait()
            print("Dumping process finished.")
            f.flush()
        
    def _parse_playerdata(self):
        ''' Parses the data file dumped by demoinfogo.
            Adds the data to a dictionary '''
        self.player_data = {}
        # match data used basically for the map name
        # should think about adding rounds etc
        self.match_data = {}
        warmup_skipped = False
        with open(self.dat_file, "r") as f:
            lines = f.readlines()
            # use indexes for handier parsing
            for i in range(0, len(lines)):
                line = lines[i]
                if warmup_skipped is True:
                    # find weapon fire events - TODO don't include grenades or knives
                    if line.find(self.weapon_fire) > -1:
                        #user_id = self._get_user(lines[i+2])
                        #self._init_userdata(user_id)
                        weapon = self._get_weapon(lines[i+3])
                        if weapon in self.grenades:
                            if weapon == self.molotov or weapon == self.incgrenade:
                                #self.player_data[user_id][self.fire] += 1
                                self.increment_stats(lines[i+2], self.fire)
                            else:
                                #self.player_data[user_id][weapon] += 1
                                self.increment_stats(lines[i+2], weapon)
                        else:
                            #self.player_data[user_id][self.weapon_fire] += 1
                            self.increment_stats(lines[i+2], self.weapon_fire)
                        # skip next five indexes
                        i = i + 5
                    # find player jump events
                    if line.find(self.player_jump) > -1:
                        #user_id = self._get_user(lines[i+2])
                        #self._init_userdata(user_id)
                            
                        #self.player_data[user_id][self.player_jump] += 1
                        self.increment_stats(lines[i+2], self.player_jump)
                        i = i + 3
                    # find player death events
                    if line.find(self.player_death) > -1:
                        user_id = self._get_user(lines[i+2])
                        attacker = self._get_user(lines[i+3])
                        assister = self._get_assister(lines[i+4])
                        if assister is not "0":
                            #self.player_data[assister][self.assists] += 1
                            self.increment_stats(lines[i+4], self.assists)
                        # is death event a headshot
                        hs = int(lines[i+9].split()[1])
                        if hs == 1:
                            #self.player_data[attacker][self.headshots] += 1
                            self.increment_stats(lines[i+3], self.headshots)
                        #self.player_data[user_id][self.deaths] += 1
                        self.increment_stats(lines[i+2], self.deaths)
                        #self.player_data[attacker][self.kills] += 1
                        self.increment_stats(lines[i+3], self.kills)
                        i = i + 13
                    if line.find(self.round_mvp) > -1:
                        #user_id = self._get_user(lines[i+2])
                        #self._init_userdata(user_id)
                        #self.player_data[user_id][self.round_mvp] += 1
                        self.increment_stats(lines[i+2], self.round_mvp)
                    if line.find(self.bomb_planted) > -1:
                        #user_id = self._get_user(lines[i+2])
                        #self._init_userdata(user_id)
                        #self.player_data[user_id][self.bomb_planted] += 1
                        self.increment_stats(lines[i+2], self.bomb_planted)
                    if line.find(self.bomb_defused) > -1:
                        #user_id = self._get_user(lines[i+2])
                        #self._init_userdata(user_id)
                        self.player_data[user_id][self.bomb_defused] += 1
                        self.increment_stats(lines[i+2], self.bomb_defused)
                    if line.find(self.player_team) > -1:
                        is_bot = int(lines[i+8].split()[1])
                        if is_bot == 0:
                            user_id = lines[i+2].split()[1].rstrip()
                            if not self.is_int(user_id):
                                #user_id = self._get_user(lines[i+2])
                                teamnum = int(lines[i+3].split()[1])
                                #self.player_data[user_id][self.team_id] = teamnum
                                self.set_stat(lines[i+2], self.team_id, teamnum)
                else:
                    if line.find("0, maps/") > -1:
                        bsp = line.split()[1]
                        self.match_data['map'] = bsp
                    #if line.find(self.player_info) == 0:
                    #    is_fake = int(lines[i+9].split(":")[1].rstrip())
                    #    is_hltv = int(lines[i+10].split(":")[1].rstrip())
                    #    user_id = lines[i+4].split(":")[1].rstrip()
                    #    if user_id not in self.player_data and is_fake is 0 and is_hltv is 0:
                    #        self._init_userdata(user_id)
                    #    if is_fake is 0 and is_hltv is 0:
                    #        xuid = lines[i+3].split(":")[1].rstrip()
                    #        self.player_data[user_id][self.xuid] = xuid
                    if line.find(self.adding_player) > -1:
                        is_fake = int(lines[i+7].split(":")[1].rstrip())
                        if is_fake == 0:
                            user_id = int(lines[i+3].split(":")[1].rstrip())
                            self._init_userdata(user_id)
                            xuid = lines[i+1].split(":")[1].rstrip()
                            name = lines[i+2].split(":")[1].rstrip()
                            self.player_data[user_id][self.xuid] = xuid
                            self.player_data[user_id][self.name] = name
                    if line.find(self.match_start) > -1:
                        warmup_skipped = True
                        i = i + 2

    def _get_user(self, line):
        ''' Finds a users name from the provided line '''
        user_id = int(line.rstrip().strip(")").split("(")[1].split(":")[1])
        return user_id

    def _get_name(self, line):
        name = line.split(" ")[2:-1]
        return ' '.join(name)

    def _get_assister(self, line):
        ''' Find assister '''
        assister = line.rstrip().strip(" ").split(" ")[1]
        if assister == '0':
            return assister
        else:
            return int(line.rstrip().strip(" ").split(" ")[-1].strip("(").strip(")").split(":")[1])


    def _get_weapon(self, line):
        ''' Finds weapon from the provided line '''
        return line.split()[1]

    def _init_userdata(self, user_id):
        ''' Initializes user data in the parse-dictionary '''
        if user_id not in self.player_data:
            self.player_data[user_id] = {
                    self.xuid: "",
                    self.weapon_fire: 0,
                    self.player_jump: 0,
                    self.kills: 0,
                    self.deaths: 0,
                    self.assists: 0,
                    self.bomb_planted: 0,
                    self.bomb_defused: 0,
                    self.team_id: 0,
                    self.headshots: 0,
                    self.round_mvp: 0,
                    self.smoke: 0,
                    self.flash: 0,
                    self.hegrenade: 0,
                    self.fire: 0,
                    self.decoy: 0,
                    self.name: ""
            }

    def _find_user_id_by_name(self, name):
        for uid in self.player_data:
            if self.player_data[uid][self.name] == name:
                return uid
        return None


    def increment_stats(self, line, field):
        user_id = self._get_user(line)
        if user_id in self.player_data:
            self.player_data[user_id][field] += 1
        else:
            user_id = self._find_user_id_by_name(self._get_name(line))
            if user_id:
                self.player_data[user_id][field] += 1

    def set_stat(self, line, field, value):
        user_id = self._get_user(line)
        if user_id in self.player_data:
            self.player_data[user_id][field] = value
        else:
            user_id = self._find_user_id_by_name(self._get_name(line))
            if user_id:
                self.player_data[user_id][field] = value
        

    def is_int(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False
