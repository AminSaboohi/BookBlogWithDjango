# Django Goodreads Scraper 
## Overview
This project is a web application built with Django, utilizing the requests and Beautiful Soup 4 (bs4) libraries for web scraping. It allows users to sign up, log in, and enter a specific Goodreads URL. The application then scrapes book information from the first five pages of the provided URL and displays it in a table format to the user. 
## Features
- User authentication (sign up and login).
- Input form for entering a Goodreads URL.
- Web scraping functionality to gather book information from the first five pages of the entered Goodreads URL.
- Display of scraped book information in a structured table format. 
## Requirements
All required libraries are listed in the requirements.txt file. Install them using the following command: 

```
pip install -r requirements.txt
```

## Configuration 
Before running the application, you must configure your local settings. Copy sample_setting.py to local_setting.py and follow the instructions within to set up your database connection and other necessary settings. 
## Setting Up the Database
Run the following commands to set up your database: 
```
python manage.py makemigrations
```
```
python manage.py migrate
```

## Running the Application 
To start the server, run: 
```
python manage.py runserver
```

Navigate to http://127.0.0.1:8000/ in your web browser to view the application. Users can sign up or log in from the homepage. Once logged in, users can enter a Goodreads URL as below to scrape and view books information.
```
'https://www.goodreads.com/search?page=*&q=book'
```
## Contributing
Contributions to this project are welcome. Please feel free to fork the repository, make your changes, and submit a pull request.
