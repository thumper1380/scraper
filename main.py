from datetime import datetime,timedelta
import logging
from earnings_fetcher import NasdaqEarningsFetcher

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('earnings_fetcher.log'),
        logging.StreamHandler()
    ]
)

def main():
    logger = logging.getLogger(__name__)
    fetcher = NasdaqEarningsFetcher()
    today = datetime.now().strftime("%Y-%m-%d")
    
    yesterday = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d")

    try:
        logger.info(f"Starting earnings data fetch for {yesterday}")
        
        earnings = fetcher.fetch_earnings(yesterday)
        fetcher.save_to_json(earnings)
        
        logger.info(f"Successfully fetched and saved earnings data for {yesterday}")
        logger.info(f"Total records: {len(earnings.records)}")
        
        # Print summary of records by category
        categories = {}
        for record in earnings.records:
            categories[record.category] = categories.get(record.category, 0) + 1
        
        logger.info("Records by category:")
        for category, count in categories.items():
            logger.info(f"{category.capitalize()}: {count}")

    except Exception as e:
        logger.error(f"Error fetching earnings data: {str(e)}")
        raise

if __name__ == "__main__":
    main()