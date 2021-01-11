from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Text, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    'postgresql+psycopg2://postgres:docker@0.0.0.0:5400/postgres')

Session = sessionmaker(bind=engine)
Base = declarative_base()


class Apartments(Base):
    __tablename__ = 'appartments'
    id = Column(Integer, primary_key=True)
    Price = Column(Integer)
    District = Column(String(200))
    Rooms = Column(String(200))
    Floor = Column(String(200))
    Floors = Column(String(200))
    Area = Column(String(200))
    Type = Column(String(200))
    Cond = Column(String(200))
    Walls = Column(String(200))
    Desc = Column(Text)
    Name = Column(String(200))
