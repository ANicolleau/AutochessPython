import os

DB_CONNECTION_STRING = "mysql://root:root@localhost:3306/autochess"
JSON_CHAMPIONS_PATH = "%s\\database\\sql_script\\champions.json" % os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))


class PartyState(object):
    IN_GAME = 'in_game'
    FINISHED = 'finished'
