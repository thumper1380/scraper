from datetime import datetime, timedelta
from typing import Optional

def get_valid_date(max_retries: int = 3) -> Optional[str]:
    """
    Get a valid date for fetching earnings data.
    Tries current date first, then goes back day by day up to max_retries.
    """
    current_date = datetime.now()
    
    for i in range(max_retries):
        check_date = current_date - timedelta(days=i)
        date_str = check_date.strftime("%Y-%m-%d")
        yield date_str