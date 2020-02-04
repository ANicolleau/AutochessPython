from sqlalchemy import Integer, Column, String
from ..constants import DB_CONNECTION_STRING
from ..models import *

engine = create_engine(DB_CONNECTION_STRING, echo=True)


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

    @staticmethod
    def get_all():
        query = session.query(Type)
        print('query : %s' % query)
        return query.all()

    @staticmethod
    def drop_table_type():
        Base.metadata.drop_all(engine)
        print("TABLES TYPE DELETED")


Base.metadata.create_all(engine)
