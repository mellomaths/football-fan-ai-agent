import schedule
import time

from dotenv import load_dotenv

from main import load_database
from src.infrastructure.custom_logger import create_logger

load_dotenv()

LOGGER = create_logger(__name__, add_file_handler=False)


def main():
    """Main function to run the scheduled jobs."""
    log = LOGGER.getChild("main")
    log.info("Scheduling job_load_database to run every Monday at 10:30 AM")
    schedule.every().monday.at("10:30").do(load_database)
    log.info("Scheduler started. Waiting for jobs to run...")
    log.debug("Scheduled jobs: " + str(schedule.get_jobs()))
    while True:
        schedule.run_pending()
        log.info("Scheduler is running. Pressing Ctrl+C to stop.")
        time.sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        LOGGER.info("Scheduler stopped by user.")
    except Exception as e:
        LOGGER.error(f"An error occurred: {e}")
        raise
    finally:
        LOGGER.info("Scheduler has been terminated.")
        # Any cleanup code can go here if needed
        # For example, closing database connections or releasing resources
        LOGGER.info("Exiting the scheduler.")
        exit(0)  # Ensure the script exits cleanly
