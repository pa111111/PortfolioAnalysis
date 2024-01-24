from datetime import datetime
from Domain.Assets import Asset
from Repository.SessionContext import SessionContext
from Repository.db_uniswap import Asset as Asset_DB, AssetDailyUsdPrice, AssetDailyWethPrice
import pandas as pd
from sqlalchemy import and_


def get_asset(symbol):
    with SessionContext() as session:
        asset_db = session.query(Asset_DB).filter_by(symbol=symbol).first()

    return Asset(id=asset_db.id, symbol=asset_db.symbol, name=asset_db.name)


def get_asset_daily_prices(asset: Asset, numeraire, start_date: datetime, end_date: datetime):
    df_prices = pd.DataFrame(columns=['symbol', 'numeraire', 'price', 'ts'])
    if numeraire not in ['USDT', 'WETH']:
        raise ValueError('Unknown purchase period')
    price_model = AssetDailyUsdPrice if numeraire == 'USDT' else AssetDailyWethPrice
    with SessionContext() as session:
        prices_db = session.query(price_model).filter_by(asset_id=asset.id).filter(and_(price_model.ts >= start_date, price_model.ts <= end_date)).all()
    for price in prices_db:
        df_prices = pd.concat([df_prices, pd.DataFrame([[asset.symbol, numeraire, price.price, price.ts]], columns=df_prices.columns)])
    return df_prices


