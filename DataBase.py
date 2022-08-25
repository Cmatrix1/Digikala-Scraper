from sqlalchemy import Column, Integer, String, ForeignKey, Table ,MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text


engine = create_engine('sqlite:///digikala.db', echo=True)
Base = declarative_base()
session = sessionmaker(bind=engine)()



class Products(Base):
    __tablename__ = 'Products'
    id = Column(Integer, primary_key=True)
    link = Column(String)
    photo = Column(String)
    name = Column(String)
    price = Column(Integer)

Base.metadata.create_all(engine)