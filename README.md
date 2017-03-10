# mlbam_scraper
Scrape MLB Advanced Media Pitch F/X Data

### Terrible description of how to use (will add more at a later date)...

1) `brew install mysql (on a Mac)`

2) `brew install rabbitmq (on a Mac)`

3) install needed python packages

4) Navigate to mlbam_scraper directory

5) Start a celery worker
       `celery -A GidScrapers worker --loglevel=info`

6) Submit the urls that `library/GidScraper.py` finds to the celery worker queue

7) Submit the paths of the data files to the celery worker queue to be writte to your mysql db
```

I plan on making this a lot easier on the user in the future.
