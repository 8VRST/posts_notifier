Posts Notifier goal is: quickly and automatically receive posts from the different websites instead of searching them manually.
Firstly the scripts were meant to scrap a posts about housing but you can try to use the project for the other categories from the websites.


**Deployment:**<br />
Everything is working and tested on Windows 10 machine with Python 3.8 and PostgreSQL 13.2 and Ubuntu 18.04 with Python 3.7 and PostgreSQL 10.22
1. Create virtual environment
2. Install in virtual environment requirements.txt
3. Rename creds_example.json in database directory to creds.json and change the values according to your database
4. Rename creds_example.json in telegram directory to creds.json and change the values according to your telegram bot. admin_id - your telegram id
5. Run setup_database.py file to apply migrations
6. Configure links and spam words for vk.com pages in scrapper/config.json similar to the links in the configuration file (just configure filters on the websites to get a links according to your parameters) or leave "" instead of a link to not scrap from a website you don't want to
7. Run run_bot.py and run_scrapper.py scripts


**Known problems:**<br />
1. On irr.by the scrapper can't get a first three posts