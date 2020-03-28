from sqlalchemy import Integer, Column, String, PickleType
from sqlalchemy.orm import relationship
from ..constants import DB_CONNECTION_STRING
from ..models import *

engine = create_engine(DB_CONNECTION_STRING, echo=True)


class Party(Base):
    __tablename__ = "party"

    id = Column(Integer, primary_key=True)
    players = relationship('Heroes')  # Joueurs
    player_turn = Column(String(255))  # A qui de jouer
    state = Column(String(255))  # Etat de la partie
    collection_of_champions = Column(PickleType)

    def __rep__(self):
        return "<Party(players='%s', player_turn='%s', state='%s', collection_of_champions='%s')>" % (
            self.players, self.player_turn, self.state, self.collection_of_champions)

    @staticmethod
    def get_all():
        query = session.query(Party)
        print('query : %s' % query)
        return query.all()

    @staticmethod
    def drop_table():
        session.commit()
        Base.metadata.drop_all(engine)
        print("TABLE PARTY DELETED")


Base.metadata.create_all(engine)
