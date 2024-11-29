import time
import logging
from datetime import datetime, timedelta
from earnings_fetcher import NasdaqEarningsFetcher
from date_utils import get_valid_date

logger = logging.getLogger(__name__)

class EarningsScheduler:
    def __init__(self):
        self.fetcher = NasdaqEarningsFetcher()
        self.last_run_date = None

    def should_run(self) -> bool:
        """Check if we should run the fetcher based on last run date."""
        if self.last_run_date is None:
            return True
            
        current_date = datetime.now().date()
        return current_date > self.last_run_date

    def run_once(self) -> bool:
        """
        Run one iteration of the earnings fetcher.
        Returns True if successful, False otherwise.
        """
        try:
            for date_str in get_valid_date():
                try:
                    logger.info(f"Attempting to fetch earnings data for {date_str}")
                    earnings = self.fetcher.fetch_earnings(date_str)
                    
                    if earnings and earnings.records:
                        self.fetcher.save_to_json(earnings)
                        self.last_run_date = datetime.now().date()
                        
                        logger.info(f"Successfully fetched and saved earnings data for {date_str}")
                        logger.info(f"Total records: {len(earnings.records)}")
                        
                        # Print summary of records by category
                        categories = {}
                        for record in earnings.records:
                            categories[record.category] = categories.get(record.category, 0) + 1
                        
                        logger.info("Records by category:")
                        for category, count in categories.items():
                            logger.info(f"{category.capitalize()}: {count}")
                            
                        return True
                    
                    logger.warning(f"No earnings data found for {date_str}")
                
                except Exception as e:
                    logger.error(f"Error fetching data for {date_str}: {str(e)}")
                    continue
            
            logger.error("Failed to fetch earnings data after trying multiple dates")
            return False
            
        except Exception as e:
            logger.error(f"Unexpected error in run_once: {str(e)}")
            return False

    def run_forever(self, check_interval: int = 3600):
        """
        Run the earnings fetcher indefinitely.
        check_interval: Time between checks in seconds (default: 1 hour)
        """
        logger.info("Starting automated earnings fetcher")
        
        while True:
            try:
                if self.should_run():
                    self.run_once()
                
                logger.debug(f"Sleeping for {check_interval} seconds")
                time.sleep(check_interval)
                
            except KeyboardInterrupt:
                logger.info("Received shutdown signal, stopping scheduler")
                break
            except Exception as e:
                logger.error(f"Error in scheduler loop: {str(e)}")
                time.sleep(60)  # Wait a minute before retrying on error