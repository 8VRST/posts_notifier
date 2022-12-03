Posts Notifier goal is: quick and automatically receive posts from the different websites instead of searching them manually.
Firstly it was meant to scrap a posts about housing but you can try to use the scrapper for the other categories from the websites.


**Deployment:**<br />
Everything is worked and tested on Windows 10 machine with Python 3.8.0 and PostgreSQL 13.2
1. Create virtual environment
2. Install in virtual environment requirements.txt
3. Rename creds_example.json in database directory to creds.json and change the values according to your database
4. Rename creds_example.json in telegram directory to creds.json and change the values according to your telegram bot. admin_id - your telegram id
5. Run setup_database.py file to apply migrations
6. Run run_bot.py and run_scrapper.py scripts.


**Known problems:**<br />
1. On irr.by the scrapper can't get the first three posts