# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
#
# from . import *
#
#
# class Database(object):
#     def __init__(self):
#         # self.create_db()
#         # self.champion_table = None
#         # self.board_table = Board()
#         # self.heroes_table = Heroes()
#         # self.type_table = Type()
#         # self.user_table = User()
#
#     def create_db(self):
#         engine = create_engine('mysql://root:root@localhost:3306', echo=True)
#         # engine.execute("CREATE DATABASE autochess")
#         # engine.execute("USE autochess")
#         engine2 = create_engine('mysql://root:root@localhost:3306/autochess', echo=True)
#         # Base = declarative_base()
#         # Base.metadata.create_all(engine2)
#         # self.champion_table = Champion()
