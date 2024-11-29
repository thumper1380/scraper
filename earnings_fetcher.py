import json
from datetime import datetime
import requests
from typing import Dict, List
from models import EarningsRecord, DailyEarnings
from config import NASDAQ_API_URL, HEADERS
from utils import validate_response, safe_get_nested
from earnings_parser import parse_category_data

class NasdaqEarningsFetcher:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    def fetch_earnings(self, date: str) -> DailyEarnings:
        """Fetch earnings data for a specific date."""
        params = {"queryString": f"date={date}"}
        try:
            response = self.session.get(NASDAQ_API_URL, params=params)
            response.raise_for_status()
            data = response.json()
            
            if not validate_response(data):
                raise ValueError("Invalid API response structure")
                
            return self._parse_response(data, date)
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch data: {str(e)}")
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse JSON response: {str(e)}")

    def _parse_response(self, data: Dict, date: str) -> DailyEarnings:
        """Parse the API response and extract relevant data."""
        records = []
        
        categories = {
            "exceed": safe_get_nested(data, "data", "exceed"),
            "meet": safe_get_nested(data, "data", "meet"),
            "fail": safe_get_nested(data, "data", "fail")
        }

        for category, category_data in categories.items():
            category_records = parse_category_data(category_data, category)
            records.extend(category_records)

        return DailyEarnings(date=date, records=records)

    def save_to_json(self, earnings: DailyEarnings, filename: str = None):
        """Save earnings data to a JSON file."""
        if filename is None:
            filename = f"earnings_{earnings.date}.json"

        data = {
            "date": earnings.date,
            "records": [
                {
                    "symbol": record.symbol,
                    "company": record.company,
                    "fiscal_quarter": record.fiscal_quarter,
                    "eps": record.eps,
                    "consensus_eps": record.consensus_eps,
                    "est_percent": record.est_percent,
                    "surprise_percent": record.surprise_percent,
                    "url": record.url,
                    "category": record.category
                }
                for record in earnings.records
            ]
        }

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except IOError as e:
            raise Exception(f"Failed to save JSON file: {str(e)}")