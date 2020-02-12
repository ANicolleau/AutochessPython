from sqlalchemy import Integer, Column, String
from ..constants import DB_CONNECTION_STRING
from ..models import *

engine = create_engine(DB_CONNECTION_STRING, echo=True)


class Board(Base):
    __tablename__ = "board"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    spot = Column(Integer)

    # bonus = Column(Integer)

    def __rep__(self):
        return "<Board(name='%s', spot='%s')>" % (
            self.name, self.spot)

    # return "<Board(name='%s', spot='%s', bonus='%s')>" % (
    #     self.name, self.spot, self.bonus)

    @staticmethod
    def get_all():
        query = session.query(Board)
        print('query : %s' % query)
        return query.all()

    @staticmethod
    def drop_table_board():
        session.commit()
        Base.metadata.drop_all(engine)
        print("TABLES BOARD DELETED")


Base.metadata.create_all(engine)

session.commit()
