import decimal
from dataclasses import dataclass
from datetime import datetime
from Domain.Assets import Asset



@dataclass
class PortfolioElement:
    asset: Asset
    period_start: datetime
    period_end: datetime
    volume: decimal

    def to_dict(self):
        return {
            'symbol': self.asset.symbol,
            'period_start': self.period_start,
            'period_end': self.period_end,
            'volume': self.volume
        }


@dataclass
class Portfolio:
    name: str
    numeraire: str
    purchase_period: str

    def to_dict(self):
        return {
            'name': self.name,
            'numeraire': self.numeraire,
            'purchase_period': self.purchase_period
        }



