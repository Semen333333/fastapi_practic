from sqlalchemy import create_engine, Column, Integer, String,Float
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://semencistckovgmail.com@localhost/practice"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
class Wallets(Base):
    __tablename__ = "wallets"
    id = Column(Integer,primary_key=True)
    wallet_name = Column(String)
    balance =Column(Float)
Base.metadata.create_all(bind=engine)