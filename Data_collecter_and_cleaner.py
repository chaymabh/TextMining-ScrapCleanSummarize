import pandas as pd
from bs4 import BeautifulSoup as soup
import requests
import csv

class WebScraper:
    def __init__(self, url):
        self.url = url
        self.event_names = []
        self.event_links = []
        self.event_dates = []

    def scrape_data(self):
        try:
            # Send a Request to the URL and return an HTML file
            req = requests.get(self.url)

            if req.status_code == 200:
                # BeautifulSoup to parse the HTML page
                html_parsed = soup(req.text, "html.parser")

                # Get the events table
                events = html_parsed.find('div', class_='box tarek')
                content = events.find_all('a')

                for ahref in content:
                    text = ahref.text.strip()
                    href = ahref.get('href').strip()

                    if text and href:
                        self.event_names.append(text)
                        self.event_links.append(href)

                # Get event dates
                events_dates = events.find_all('time')
                for d in events_dates:
                    date = d.get('data-start').strip()
                    if date:
                        self.event_dates.append(date)

                return True
            else:
                print(f"Error: Unable to retrieve data from {self.url}")
                return False

        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def clean_data(self):
        # Remove duplicates
        self.event_names, self.event_links, self.event_dates = zip(*set(zip(self.event_names, self.event_links, self.event_dates)))

        # Convert date strings to datetime objects
        self.event_dates = [pd.to_datetime(date, format='%Y-%m-%d', errors='coerce') for date in self.event_dates]

    def store_data_csv(self, filename):
        if not self.event_names or not self.event_links or not self.event_dates:
            print("No data to store.")
            return

        try:
            data = {
                'EventName': self.event_names,
                'EventUrl': self.event_links,
                'EventDate': self.event_dates
            }
            df = pd.DataFrame(data)
            df.to_csv(filename, index=False, encoding='utf-8')
            print(f"Data saved to {filename}")
        except Exception as e:
            print(f"Error saving data to CSV: {e}")

def main():
    url = "http://www.istic.rnu.tn/fr/presentation/presentation.html"
    scraper = WebScraper(url)

    if scraper.scrape_data():
        scraper.clean_data()
        scraper.store_data_csv('events_cleaned.csv')

if __name__ == '__main__':
    main()
