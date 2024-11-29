import logging
from scheduler import EarningsScheduler

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
    scheduler = EarningsScheduler()
    
    # Run the scheduler indefinitely
    # Check every hour (3600 seconds)
    scheduler.run_forever(check_interval=3600)

if __name__ == "__main__":
    main()