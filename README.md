# mlbam_scraper
Scrape MLB Advanced Media Pitch F/X Data

Terrible description of how to use (will add more at a later date)...

```
brew install mysql
brew install rabbitmq
install python packages
create a mysql database called mlbam
run all of the scripts that being with 'create_' in the mlbam_scraper/mysql folder
  like this... mysql -uroot -p mlbam < create_<rest_of_file_name>.sql
Navigate to mlbam_scraper directory
Start a celery worker
  like this... celery -A GidScrapers worker --loglevel=info 
Submit the urls that library/GidScraper.py finds to the celery worker queue
Submit the paths of the data files to the celery worker queue to be writte to your mysql db
```

I also plan on making this a lot easier on the user in the future.
