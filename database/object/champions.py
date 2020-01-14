from sqlalchemy import Integer, Column, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql://root:root@localhost:3306', echo=True)
engine.execute("CREATE DATABASE autochess")
engine.execute("USE autochess")
Base = declarative_base()


class Champion(Base):
    __tablename__ = 'champions'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    health = Column(Integer)
    price = Column(Integer)
    description = Column(String(255))
    rarity = Column(Integer)
    level = Column(Integer)

    def __rep__(self):
        return "<Champion(name='%s', health='%s', price='%s', description='%s', rarity='%s', level='%s')>" % (
            self.name, self.health, self.price, self.description, self.rarity, self.level)


Base.metadata.create_all(engine)

# View et base de données
