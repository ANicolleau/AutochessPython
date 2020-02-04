# table correspondante au personnage choisi au début
# buf et actif différent
# si pdv à 0 fin de partie

from sqlalchemy import Integer, Column, String
from ..constants import DB_CONNECTION_STRING
from ..models import *

engine = create_engine(DB_CONNECTION_STRING, echo=True)


class Heroes(Base):
    __tablename__ = "heroes"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    health = Column(Integer)
    money = Column(Integer)
    level = Column(Integer)

    def __rep__(self):
        return "<Board(name='%s', health='%s', money='%s', level='%s')>" % (
            self.name, self.health, self.money, self.level)

    @staticmethod
    def get_all():
        query = session.query(Heroes)
        print('query : %s' % query)
        return query.all()

    @staticmethod
    def drop_table_heroes():
        Base.metadata.drop_all(engine)
        print("TABLES HEROES DELETED")


Base.metadata.create_all(engine)
