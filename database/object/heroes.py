# table correspondante au personnage choisi au début
# buf et actif différent
# si pdv à 0 fin de partie

from sqlalchemy import Integer, Column, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql://root:root@localhost:3306/autochess', echo=True)

Base = declarative_base()


# CREATE TABLE IF NOT EXISTS autochess.heroes(id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, name VARCHAR(255), health INT, money INT, level INT);

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


Base.metadata.create_all(engine)