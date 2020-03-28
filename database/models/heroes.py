from sqlalchemy import Integer, Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from ..constants import DB_CONNECTION_STRING
from ..models import *

engine = create_engine(DB_CONNECTION_STRING, echo=True)


class Heroes(Base):
    __tablename__ = "heroes"

    id = Column(Integer, primary_key=True)
    party_id = Column(Integer, ForeignKey('party.id'))
    name = Column(String(255))
    health = Column(Integer)
    money = Column(Integer)
    level = Column(Integer)
    # champions = relationship('Champion')
    ia = Column(Boolean)
    child = relationship("Board", uselist=False, back_populates="parent")

    def __rep__(self):
        return "<Heroes(name='%s', health='%s', money='%s', level='%s', ia='%s')>" % (
            self.name, self.health, self.money, self.level, self.ia)

    @staticmethod
    def get_all():
        query = session.query(Heroes)
        print('query : %s' % query)
        return query.all()

    @staticmethod
    def drop_table():
        session.commit()
        Base.metadata.drop_all(engine)
        print("TABLES HEROES DELETED")


Base.metadata.create_all(engine)
