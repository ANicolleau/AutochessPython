# CREATE TABLE IF NOT EXISTS autochess.type(id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, name VARCHAR(255), number INT, bonus_percent INT, modified_stats VARCHAR(255));

from sqlalchemy import Integer, Column, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
engine = create_engine('mysql://root:root@localhost:3306/autochess', echo=True)
Base = declarative_base()


class Type(Base):
    __tablename__ = "type"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    number = Column(Integer)
    bonus_percent = Column(Integer)
    modified_stats = Column(String(255))

    def __rep__(self):
        return "<Board(name='%s', number = '%s', bonus_percent='%s', modified_stats='%s')>" % (
            self.name, self.number, self.bonus_percent, self.modified_stats)

Base.metadata.create_all(engine)