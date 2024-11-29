from dataclasses import dataclass
from typing import List, Optional

@dataclass
class EarningsRecord:
    symbol: str
    company: str
    fiscal_quarter: str
    eps: str
    consensus_eps: str
    est_percent: str
    surprise_percent: str
    url: str
    category: str  # 'exceed', 'meet', or 'fail'

@dataclass
class DailyEarnings:
    date: str
    records: List[EarningsRecord]