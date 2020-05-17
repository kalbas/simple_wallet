from sqlalchemy import Column, ForeignKey, Integer, BigInteger, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func


Base = declarative_base()


class Wallet(Base):
    __tablename__ = 'wallets'

    id = Column(Integer, primary_key=True)
    balance = Column(BigInteger)


class Refill(Base):
    __tablename__ = 'refills'

    id = Column(Integer, primary_key=True)
    wallet_id = Column(Integer, ForeignKey('wallets.id'))
    amount = Column(BigInteger)
    datetime = Column(DateTime, server_default=func.now())


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    wallet_id = Column(Integer, ForeignKey('wallets.id'))
    amount = Column(BigInteger)
    datetime = Column(DateTime, server_default=func.now())
    ip = Column(String)
