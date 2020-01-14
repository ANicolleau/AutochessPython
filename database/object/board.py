from sqlalchemy import Integer, Column, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
engine = create_engine('mysql://root:root@localhost:3306/autochess', echo=True)
Base = declarative_base()


# CREATE TABLE IF NOT EXISTS
# autochess.board(id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, name VARCHAR(255), spot INT, bonus INT);
class Board(Base):
    __tablename__ = "board"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    spot = Column(Integer)
    bonus = Column(Integer)

    def __rep__(self):
        return "<Board(name='%s', spot='%s', bonus='%s')>" % (
            self.name, self.spot, self.bonus)


Base.metadata.create_all(engine)
