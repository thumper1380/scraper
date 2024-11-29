from typing import Dict, List, Optional
from models import EarningsRecord
from utils import safe_get_nested

def parse_earnings_row(row: Dict, category: str) -> Optional[EarningsRecord]:
    """Parse a single earnings row into an EarningsRecord."""
    try:
        return EarningsRecord(
            symbol=row["symbol"],
            company=row["company"],
            fiscal_quarter=row["fiscalQuarterReported"],
            eps=row["eps"],
            consensus_eps=row["consensusEPSForecast"],
            est_percent=row["estPercent"],
            surprise_percent=row["surprisePercent"],
            url=row["url"],
            category=category
        )
    except (KeyError, TypeError):
        return None

def parse_category_data(category_data: Dict, category: str) -> List[EarningsRecord]:
    """Parse earnings data for a specific category."""
    records = []
    if not category_data:
        return records

    rows = safe_get_nested(category_data, 'table', 'rows')
    if not rows:
        return records

    for row in rows:
        record = parse_earnings_row(row, category)
        if record:
            records.append(record)

    return records