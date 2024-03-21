"""this function provide an url information"""
import logging
import json
import requests
import re
from bs4 import BeautifulSoup


def build_logger():
    # Set up basic configuration for logging
    logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s', )
    logger_ = logging.getLogger()
    logger_.setLevel(logging.DEBUG)
    return logger_


class URLData:
    def __init__(self, url):
        self.response = None
        self.logger = build_logger()
        self.data = dict()
        self.data['url'] = url
        self.meno_dict = dict()
        self.data['timeout'] = 100000
        self.user_meno()

    def user_meno(self):
        self.meno_dict['status'] = lambda: print(self.data['status_code'])
        self.meno_dict['headers'] = lambda: print(self.data['headers'])
        self.meno_dict['text'] = lambda: print(self.data['page_content'])

    def parse_data(self):
        try:
            self.fetch_data()
        except Exception as err:
            self.logger.error(f"An error occur {err}")
            print(f"An error occur {err}")
        book_rows = list()
        for i in range(5):
            url_split = self.data['url'].split('*')
            url = str(i + 1).join(url_split)
            print(i)
            response = requests.get(url)
            content = BeautifulSoup(response.text, 'html.parser')
            html_table = content.findAll('tr')
            for html_row in html_table:
                book_row = dict()
                book_row['name'] = html_row.find('a',
                                                 class_="bookTitle").span.text
                book_row['auther'] = html_row.find('a',
                                                   class_="authorName").span.text
                h_rating_year_edition = html_row.find('span',
                                                      class_="greyText smallText uitext").text
                rating_year_edition = h_rating_year_edition.split('—')
                book_row['rating_avg'] = \
                    rating_year_edition[0].split()[0]
                book_row['total_ratings'] = \
                    rating_year_edition[1].split()[0]
                book_row['year'] = rating_year_edition[2].split()[1]
                book_row['editions'] = rating_year_edition[3].split()[
                    0]
                if book_row not in book_rows:
                    book_rows.append(book_row)
                else:
                    print('@' * 60)
        return book_rows

    def fetch_data(self):
        try:
            regex = re.compile(
                r'^(?:http|ftp)s?://'  # http:// or https://
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+'
                r'(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
                r'localhost|'  # localhost...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
                r'(?::\d+)?'  # optional port
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)
            if re.match(regex, self.data['url']) is not None:
                raise "Invalid URL!"
            self.response = requests.get(self.data['url'],
                                    timeout=self.data['timeout'],
                                    )
            self.response.raise_for_status()
            # Raises HTTPError for bad responses
            if self.response.status_code == 200:
                self.data['status_code'] = self.response.status_code
                self.data['headers'] = dict(self.response.headers)
                self.data['page_content'] = self.response.text
                # Saving first 200 chars for brevity
                self.logger.info(f"Data fetched successfully for "
                                 f"URL: {self.data['url']}"
                                 )
        except requests.exceptions.HTTPError as http_err:
            self.logger.error(f"HTTP error occurred for "
                              f"URL {self.data['url']}: {http_err}"
                              )
            print(f"HTTP error: {http_err}")
        except requests.exceptions.ConnectionError as conn_err:
            self.logger.error(f"Connection error occurred for "
                              f"URL {self.data['url']}: {conn_err}"
                              )
            print(f"Connection error: {conn_err}")
        except requests.exceptions.Timeout as timeout_err:
            self.logger.error(f"Timeout error occurred for "
                              f"URL {self.data['url']}: {timeout_err}"
                              )
            print(f"Timeout error: {timeout_err}")
        except requests.exceptions.RequestException as req_err:
            self.logger.error(f"General error fetching data for "
                              f"URL {self.data['url']}: {req_err}"
                              )
            print(f"General error fetching data for "
                  f"URL {self.data['url']}: {req_err}"
                  )
        except Exception as err:
            self.logger.error(f"An error occur {err}")
            print(f"An error occur {err}")

    def make_json_file_name(self):
        file_name = self.data['url'].replace('https://', '').replace('/', '_')
        self.data['json_file'] = f"{file_name}.json"

    def save_data(self):
        file_name = self.data['url'].replace('https://', '').replace('/', '_')
        filename = f"{file_name}.json"
        try:
            with open(filename, "w") as outfile:
                json.dump(self.data, outfile)
                self.logger.info(
                    f"Data saved to file for URL: {self.data['url']}")
        except IOError as io_err:
            self.logger.error(
                f"Error saving data to file for "
                f"URL {self.data['url']}: {io_err}"
            )
            print(f"Error saving data: {io_err}")
        except Exception as err:
            self.logger.error(f"An error occur {err}")
            print(f"An error occur {err}")
