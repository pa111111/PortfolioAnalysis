import decimal
from dataclasses import dataclass, field
from datetime import datetime
from pyarrow import timestamp
from Domain.Assets import Asset
from typing import List
import pandas as pd


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
    _portfolio_elements: List[PortfolioElement] = field(default_factory=list)

    def add_portfolio_element(self, element: PortfolioElement):
        self._portfolio_elements.append(element)

    def get_portfolio_elements(self):
        return self._portfolio_elements

    def to_dict(self):
        return {
            'name': self.name,
            'numeraire': self.numeraire,
            'purchase_period': self.purchase_period
        }



