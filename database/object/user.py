from sqlalchemy import Integer, Column, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql://root:root@localhost:3306/autochess', echo=True)
Base = declarative_base()


# CREATE TABLE IF NOT EXISTS autochess.user(id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, bool_ia boolean);


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    ia = Column(Boolean)

    def __rep__(self):
        return "<Board(ia='%s')>" % (
            self.ia)


Base.metadata.create_all(engine)
