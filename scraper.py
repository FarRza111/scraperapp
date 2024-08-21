import requests
import pycountry
import pandas as pd
from bs4 import BeautifulSoup
from typing import List, Dict, Union
import logging
from concurrent.futures import ThreadPoolExecutor

# logging
logging.basicConfig(level=logging.INFO)

class SwiftCodeScraper:

    
    def __init__(self, base_url: str, country_slugs: List[str]) -> None:
        self.base_url = base_url
        self.country_slugs = country_slugs
        self.swift_codes: Dict[str, List[Dict[str, str]]] = {}

    
    def fetch_country_page(self, slug: str) -> Union[str, None]:
        country_url = f"{self.base_url}{slug}"
        try:
            response = requests.get(country_url)
            response.raise_for_status()  # Raises HTTPError for bad responses [I can write like go if response == 200 then it is success otherwise, we must understand the responses from http protocol]
            return response.text
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching {country_url}: {e}")
            return None

    
    def parse_swift_codes(self, html_content: str) -> List[Dict[str, str]]:
        soup = BeautifulSoup(html_content, 'html.parser')
        swift_codes: List[Dict[str, str]] = []
        table = soup.find('table')
        if table:
            rows = table.find_all('tr')[1:]  # Skiping the header row off the body
            for row in rows:
                columns = row.find_all('td')
                if len(columns) > 4:
                    bank_name = columns[1].get_text(strip=True)
                    swift_code = columns[4].find('a').get_text(strip=True)
                    swift_codes.append({
                        'bank_name': bank_name,
                        'swift_code': swift_code
                    })
        return swift_codes
        

    def scrape(self) -> None:
        with ThreadPoolExecutor() as executor:
            results = executor.map(self.fetch_country_page, self.country_slugs)
            for slug, html_content in zip(self.country_slugs, results):
                if html_content:
                    swift_codes = self.parse_swift_codes(html_content)
                    self.swift_codes[slug] = swift_codes
                    

    def generate_swift_codes_df(self) -> pd.DataFrame:
        temp: Dict[str, List[str]] = {"Banke Name": [], "Swift Code": [], "country_name": []}
        for slug, codes in self.swift_codes.items():
            country_name = slug.strip('/').capitalize()
            for code in codes:
                temp["Banke Name"].append(code["bank_name"])
                temp["Swift Code"].append(code["swift_code"])
                temp["country_name"].append(country_name)
        return pd.DataFrame(temp)
        

def add_slash_to_country(countries: List[str]) -> List[str]:
    return [f"/{country}/" for country in countries]
    

# Example usage:
if __name__ == "__main__":
    list_of_countries: List[str] = [iso_country.name.lower() for iso_country in pycountry.countries]

    country_slugs: List[str] = [
        '/azerbaijan/', '/germany/', '/france/', '/georgia/', '/italy/', '/spain/', '/sweeden/',
        '/united-kingdom/', '/finland/', '/norway/', '/denmark/', '/netherlands/', '/sweden/',
        '/lithaunia/', '/latvia/', '/estonia/', '/romania/', '/switzerland/', '/austria/',
        '/belgium/', '/hungary/', '/turkey/', '/poland/', '/germany/', '/croatia/', '/slovakia/',
        '/iran/', '/armenia/'
    ]

    # country_slugs = add_slash_to_country(list_of_countries)  # Optional: generate slugs dynamically

    base_url: str = "https://www.theswiftcodes.com"
    scraper = SwiftCodeScraper(base_url, country_slugs)
    scraper.scrape()
    scraped_data: pd.DataFrame = scraper.generate_swift_codes_df()
    print(scraped_data)
    scraped_data.to_excel("swift_codes.xlsx", index=False)
