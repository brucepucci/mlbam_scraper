# mlbam_scraper
Scrape MLB Advanced Media Pitch F/X Data

Terrible description of how to use (will add more at a later date)...

1) `brew install mysql (on a Mac)`

2) `brew install rabbitmq (on a Mac)`

3) install needed python packages

4) create a mysql database called mlbam

5) run all of the scripts that being with 'create_' in the mlbam_scraper/mysql folder
       `mysql -uroot -p mlbam < create_<rest_of_file_name>.sql`

6) Navigate to mlbam_scraper directory

7) Start a celery worker
       `celery -A GidScrapers worker --loglevel=info`

8) Submit the urls that `library/GidScraper.py` finds to the celery worker queue

9) Submit the paths of the data files to the celery worker queue to be writte to your mysql db
```

I plan on making this a lot easier on the user in the future.
