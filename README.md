# job_tracker
Tool to track jobs you've applied to

# Two trackers included
  - Automatic
    - indeed_job_scraper.py
    - Run file with system args [username] [password]
    - Automatically logs in to indeed and web scrapes the applied page for info on jobs you have applied to
    - If recaptcha shows up, manually complete it and type in any character into the terminal to continue the web scraping
    - Saves data as a csv file
  - Manual
    - job_tracker.py
    - Manually enter key information about jobs you've applied to, for now this allows you to enter more info than the auto scraper can scrape
    - Reference above for recaptcha process
    - Saves data as a json file
