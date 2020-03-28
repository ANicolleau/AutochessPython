from sqlalchemy import Integer, Column, Boolean
from ..constants import DB_CONNECTION_STRING
from ..models import *

engine = create_engine(DB_CONNECTION_STRING, echo=True)

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    ia = Column(Boolean)

    def __rep__(self):
        return "<User(ia='%s')>" % (
            self.ia)

    @staticmethod
    def get_all():
        query = session.query(User)
        print('query : %s' % query)
        return query.all()

    @staticmethod
    def drop_table():
        session.commit()
        Base.metadata.drop_all(engine)
        print("TABLES USER DELETED")


Base.metadata.create_all(engine)
