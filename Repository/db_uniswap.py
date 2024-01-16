# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Asset(Base):
    __tablename__ = 'asset'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    symbol = Column(String(50))
    load_prices = Column(Boolean)


class PurchasePeriod(Base):
    __tablename__ = 'purchase_period'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))


class Portfolio(Base):
    __tablename__ = 'portfolio'

    id = Column(Integer, primary_key=True)
    purchase_period_id = Column(ForeignKey('purchase_period.id'))
    name = Column(String(250))
    numeraire = Column(String(50))

    purchase_period = relationship('PurchasePeriod')


class AssetInPortfolio(Base):
    __tablename__ = 'asset_in_portfolio'

    id = Column(Integer, primary_key=True)
    period_start = Column(DateTime)
    period_end = Column(DateTime)
    volume = Column(Numeric)
    asset_id = Column(ForeignKey('asset.id'))
    portfolio_id = Column(ForeignKey('portfolio.id'))

    asset = relationship('Asset')
    portfolio = relationship('Portfolio')
