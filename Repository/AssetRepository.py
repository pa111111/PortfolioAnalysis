from Domain.Assets import Asset
from Repository.SessionContext import SessionContext
from Repository.db_uniswap import Asset as Asset_DB


def get_asset(symbol):
    with SessionContext() as session:
        asset_db = session.query(Asset_DB).filter_by(symbol=symbol).first()

    return Asset(id=asset_db.id, symbol=asset_db.symbol, name=asset_db.name)
