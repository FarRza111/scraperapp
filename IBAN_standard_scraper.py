import re 
import pycountry
import urllib.request
import pandas as pd
from typing import List
from bs4 import BeautifulSoup


country_urls = [
'https://bank.codes/iban/structure/aruba', 'https://bank.codes/iban/structure/afghanistan', 'https://bank.codes/iban/structure/angola', 'https://bank.codes/iban/structure/anguilla', 
'https://bank.codes/iban/structure/albania', 'https://bank.codes/iban/structure/andorra', 'https://bank.codes/iban/structure/united-arab-emirates', 'https://bank.codes/iban/structure/argentina', 'https://bank.codes/iban/structure/armenia', 'https://bank.codes/iban/structure/american-samoa', 'https://bank.codes/iban/structure/antarctica', 'https://bank.codes/iban/structure/french-southern-territories', 'https://bank.codes/iban/structure/antigua-and-barbuda', 'https://bank.codes/iban/structure/australia', 'https://bank.codes/iban/structure/austria', 'https://bank.codes/iban/structure/azerbaijan', 'https://bank.codes/iban/structure/burundi', 'https://bank.codes/iban/structure/belgium', 'https://bank.codes/iban/structure/benin', 'https://bank.codes/iban/structure/bonaire,-sint-eustatius-and-saba', 'https://bank.codes/iban/structure/burkina-faso', 'https://bank.codes/iban/structure/bangladesh', 'https://bank.codes/iban/structure/bulgaria', 'https://bank.codes/iban/structure/bahrain', 'https://bank.codes/iban/structure/bahamas', 'https://bank.codes/iban/structure/bosnia-and-herzegovina', 'https://bank.codes/iban/structure/saint-barthélemy', 'https://bank.codes/iban/structure/belarus', 'https://bank.codes/iban/structure/belize', 'https://bank.codes/iban/structure/bermuda', 'https://bank.codes/iban/structure/bolivia,-plurinational-state-of', 'https://bank.codes/iban/structure/brazil', 'https://bank.codes/iban/structure/barbados', 'https://bank.codes/iban/structure/brunei-darussalam', 'https://bank.codes/iban/structure/bhutan', 'https://bank.codes/iban/structure/bouvet-island', 'https://bank.codes/iban/structure/botswana', 'https://bank.codes/iban/structure/central-african-republic', 'https://bank.codes/iban/structure/canada', 'https://bank.codes/iban/structure/cocos-(keeling)-islands', 'https://bank.codes/iban/structure/switzerland', 'https://bank.codes/iban/structure/chile', 'https://bank.codes/iban/structure/china',  'https://bank.codes/iban/structure/cameroon', 
'https://bank.codes/iban/structure/congo', 'https://bank.codes/iban/structure/cook-islands', 'https://bank.codes/iban/structure/colombia', 'https://bank.codes/iban/structure/comoros', 'https://bank.codes/iban/structure/cabo-verde', 'https://bank.codes/iban/structure/costa-rica', 'https://bank.codes/iban/structure/cuba', 'https://bank.codes/iban/structure/curaçao', 'https://bank.codes/iban/structure/christmas-island', 'https://bank.codes/iban/structure/cayman-islands', 'https://bank.codes/iban/structure/cyprus', 'https://bank.codes/iban/structure/czechia', 'https://bank.codes/iban/structure/germany', 'https://bank.codes/iban/structure/djibouti', 'https://bank.codes/iban/structure/dominica', 'https://bank.codes/iban/structure/denmark', 'https://bank.codes/iban/structure/dominican-republic', 'https://bank.codes/iban/structure/algeria', 'https://bank.codes/iban/structure/ecuador', 'https://bank.codes/iban/structure/egypt', 'https://bank.codes/iban/structure/eritrea', 'https://bank.codes/iban/structure/western-sahara', 'https://bank.codes/iban/structure/spain', 'https://bank.codes/iban/structure/estonia', 'https://bank.codes/iban/structure/ethiopia', 'https://bank.codes/iban/structure/finland', 'https://bank.codes/iban/structure/fiji', 'https://bank.codes/iban/structure/falkland-islands-(malvinas)', 'https://bank.codes/iban/structure/france', 'https://bank.codes/iban/structure/faroe-islands', 'https://bank.codes/iban/structure/micronesia,-federated-states-of', 'https://bank.codes/iban/structure/gabon', 'https://bank.codes/iban/structure/united-kingdom', 'https://bank.codes/iban/structure/georgia', 'https://bank.codes/iban/structure/guernsey', 'https://bank.codes/iban/structure/ghana', 'https://bank.codes/iban/structure/gibraltar', 'https://bank.codes/iban/structure/guinea', 'https://bank.codes/iban/structure/guadeloupe', 'https://bank.codes/iban/structure/gambia', 'https://bank.codes/iban/structure/guinea-bissau', 'https://bank.codes/iban/structure/equatorial-guinea', 'https://bank.codes/iban/structure/greece', 'https://bank.codes/iban/structure/grenada', 'https://bank.codes/iban/structure/greenland', 'https://bank.codes/iban/structure/guatemala', 'https://bank.codes/iban/structure/french-guiana', 'https://bank.codes/iban/structure/guam', 'https://bank.codes/iban/structure/guyana', 'https://bank.codes/iban/structure/hong-kong', 'https://bank.codes/iban/structure/heard-island-and-mcdonald-islands', 'https://bank.codes/iban/structure/honduras', 'https://bank.codes/iban/structure/croatia', 'https://bank.codes/iban/structure/haiti', 'https://bank.codes/iban/structure/hungary', 'https://bank.codes/iban/structure/indonesia', 'https://bank.codes/iban/structure/isle-of-man', 'https://bank.codes/iban/structure/india', 'https://bank.codes/iban/structure/british-indian-ocean-territory', 'https://bank.codes/iban/structure/ireland', 'https://bank.codes/iban/structure/iran,-islamic-republic-of', 'https://bank.codes/iban/structure/iraq', 'https://bank.codes/iban/structure/iceland', 'https://bank.codes/iban/structure/israel', 'https://bank.codes/iban/structure/italy', 'https://bank.codes/iban/structure/jamaica', 'https://bank.codes/iban/structure/jersey', 'https://bank.codes/iban/structure/jordan', 'https://bank.codes/iban/structure/japan', 'https://bank.codes/iban/structure/kazakhstan', 'https://bank.codes/iban/structure/kenya', 'https://bank.codes/iban/structure/kyrgyzstan', 'https://bank.codes/iban/structure/cambodia', 'https://bank.codes/iban/structure/kiribati', 'https://bank.codes/iban/structure/saint-kitts-and-nevis', 'https://bank.codes/iban/structure/korea,-republic-of', 'https://bank.codes/iban/structure/kuwait', "https://bank.codes/iban/structure/lao-people's-democratic-republic", 'https://bank.codes/iban/structure/lebanon', 'https://bank.codes/iban/structure/liberia', 'https://bank.codes/iban/structure/libya', 'https://bank.codes/iban/structure/saint-lucia', 'https://bank.codes/iban/structure/liechtenstein', 'https://bank.codes/iban/structure/sri-lanka', 'https://bank.codes/iban/structure/lesotho', 'https://bank.codes/iban/structure/lithuania', 'https://bank.codes/iban/structure/luxembourg', 'https://bank.codes/iban/structure/latvia', 'https://bank.codes/iban/structure/macao', 'https://bank.codes/iban/structure/saint-martin-(french-part)', 'https://bank.codes/iban/structure/morocco', 'https://bank.codes/iban/structure/monaco', 'https://bank.codes/iban/structure/moldova,-republic-of', 'https://bank.codes/iban/structure/madagascar', 'https://bank.codes/iban/structure/maldives', 'https://bank.codes/iban/structure/mexico', 'https://bank.codes/iban/structure/marshall-islands', 'https://bank.codes/iban/structure/north-macedonia', 'https://bank.codes/iban/structure/mali', 'https://bank.codes/iban/structure/malta', 'https://bank.codes/iban/structure/myanmar', 'https://bank.codes/iban/structure/montenegro', 'https://bank.codes/iban/structure/mongolia', 'https://bank.codes/iban/structure/northern-mariana-islands', 'https://bank.codes/iban/structure/mozambique', 'https://bank.codes/iban/structure/mauritania', 'https://bank.codes/iban/structure/montserrat', 'https://bank.codes/iban/structure/martinique', 'https://bank.codes/iban/structure/mauritius', 'https://bank.codes/iban/structure/malawi', 'https://bank.codes/iban/structure/malaysia', 'https://bank.codes/iban/structure/mayotte', 'https://bank.codes/iban/structure/namibia', 'https://bank.codes/iban/structure/new-caledonia', 'https://bank.codes/iban/structure/niger', 'https://bank.codes/iban/structure/norfolk-island', 'https://bank.codes/iban/structure/nigeria', 'https://bank.codes/iban/structure/nicaragua', 'https://bank.codes/iban/structure/niue', 'https://bank.codes/iban/structure/netherlands', 'https://bank.codes/iban/structure/norway', 'https://bank.codes/iban/structure/nepal', 'https://bank.codes/iban/structure/nauru',
'https://bank.codes/iban/structure/new-zealand', 'https://bank.codes/iban/structure/oman', 'https://bank.codes/iban/structure/pakistan', 'https://bank.codes/iban/structure/panama', 'https://bank.codes/iban/structure/pitcairn', 'https://bank.codes/iban/structure/peru', 'https://bank.codes/iban/structure/philippines', 'https://bank.codes/iban/structure/palau', 'https://bank.codes/iban/structure/papua-new-guinea', 'https://bank.codes/iban/structure/poland', 'https://bank.codes/iban/structure/puerto-rico', "https://bank.codes/iban/structure/korea,-democratic-people's-republic-of", 'https://bank.codes/iban/structure/portugal', 'https://bank.codes/iban/structure/paraguay', 'https://bank.codes/iban/structure/palestine,-state-of', 'https://bank.codes/iban/structure/french-polynesia', 'https://bank.codes/iban/structure/qatar', 'https://bank.codes/iban/structure/réunion', 'https://bank.codes/iban/structure/romania', 'https://bank.codes/iban/structure/russian-federation', 'https://bank.codes/iban/structure/rwanda', 'https://bank.codes/iban/structure/saudi-arabia', 'https://bank.codes/iban/structure/sudan', 'https://bank.codes/iban/structure/senegal', 'https://bank.codes/iban/structure/singapore', 'https://bank.codes/iban/structure/south-georgia-and-the-south-sandwich-islands', 
'https://bank.codes/iban/structure/saint-helena,-ascension-and-tristan-da-cunha', 'https://bank.codes/iban/structure/svalbard-and-jan-mayen', 'https://bank.codes/iban/structure/solomon-islands', 'https://bank.codes/iban/structure/sierra-leone', 'https://bank.codes/iban/structure/el-salvador', 'https://bank.codes/iban/structure/san-marino', 'https://bank.codes/iban/structure/somalia', 'https://bank.codes/iban/structure/saint-pierre-and-miquelon', 'https://bank.codes/iban/structure/serbia', 'https://bank.codes/iban/structure/south-sudan', 'https://bank.codes/iban/structure/sao-tome-and-principe', 'https://bank.codes/iban/structure/suriname', 'https://bank.codes/iban/structure/slovakia', 'https://bank.codes/iban/structure/slovenia', 'https://bank.codes/iban/structure/sweden', 'https://bank.codes/iban/structure/eswatini', 'https://bank.codes/iban/structure/sint-maarten-(dutch-part)', 'https://bank.codes/iban/structure/seychelles', 'https://bank.codes/iban/structure/syrian-arab-republic', 'https://bank.codes/iban/structure/turks-and-caicos-islands', 'https://bank.codes/iban/structure/chad', 'https://bank.codes/iban/structure/togo', 'https://bank.codes/iban/structure/thailand', 'https://bank.codes/iban/structure/tajikistan', 'https://bank.codes/iban/structure/tokelau', 'https://bank.codes/iban/structure/turkmenistan', 'https://bank.codes/iban/structure/timor-leste', 'https://bank.codes/iban/structure/tonga', 'https://bank.codes/iban/structure/trinidad-and-tobago', 'https://bank.codes/iban/structure/tunisia', 'https://bank.codes/iban/structure/türkiye', 'https://bank.codes/iban/structure/tuvalu', 'https://bank.codes/iban/structure/taiwan,-province-of-china', 'https://bank.codes/iban/structure/tanzania,-united-republic-of', 'https://bank.codes/iban/structure/uganda', 'https://bank.codes/iban/structure/ukraine', 'https://bank.codes/iban/structure/united-states-minor-outlying-islands', 'https://bank.codes/iban/structure/uruguay', 'https://bank.codes/iban/structure/united-states', 'https://bank.codes/iban/structure/uzbekistan', 'https://bank.codes/iban/structure/holy-see-(vatican-city-state)', 'https://bank.codes/iban/structure/saint-vincent-and-the-grenadines', 'https://bank.codes/iban/structure/venezuela,-bolivarian-republic-of', 'https://bank.codes/iban/structure/virgin-islands,-british', 'https://bank.codes/iban/structure/virgin-islands,-u.s.', 'https://bank.codes/iban/structure/viet-nam', 'https://bank.codes/iban/structure/vanuatu', 'https://bank.codes/iban/structure/wallis-and-futuna', 'https://bank.codes/iban/structure/samoa', 'https://bank.codes/iban/structure/yemen', 'https://bank.codes/iban/structure/south-africa', 'https://bank.codes/iban/structure/zambia', 'https://bank.codes/iban/structure/zimbabwe']
    

import re
import pycountry
import urllib.request
import pandas as pd
from typing import List, Dict
from bs4 import BeautifulSoup

country_urls = [

    'https://bank.codes/iban/structure/estonia', 'https://bank.codes/iban/structure/azerbaijan',
]

# Function to get the soup object
def get_soup(url: str, headers: Dict[str, str]) -> BeautifulSoup:
    try:
        request = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(request) as response:
            html_content = response.read()
        return BeautifulSoup(html_content, 'html.parser')
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"404 Error for URL: {url}")
            return None
        else:
            raise
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

# Function to process the soup object and extract data
def process_soup(soup: BeautifulSoup, country_name: str) -> List[Dict[str, str]]:
    
    data = []
    if not soup:
        return data

    tables = soup.find_all('table')
    for table in tables:
        rows = table.find_all('tr')
        country_data = {'Country': country_name}
        for row in rows:
            cols = row.find_all('td')
            if not cols:
                continue
            label = cols[0].text.strip()  # The label (e.g., "IBAN Checksum")
            value = cols[2].text.strip()  # The value (e.g., "14")
            country_data[label] = value  # Add to the country data dictionary
        data.append(country_data)  

    spans = soup.find_all('span')
    extracted_values = [span.get_text() for span in spans]
    filtered_list = list(filter(None, extracted_values))

    return data


# Define the request headers
headers = {'User-Agent': 'Mozilla/5.0'}
all_data = []

for url in country_urls:
    country_name = url.split('/')[-2].capitalize()
    soup = get_soup(url, headers)
    country_data = process_soup(soup, country_name)
    all_data.extend(country_data)

df = pd.DataFrame(all_data)

# Save the DataFrame to an Excel file
df.to_excel('account__s.xlsx', index=False)



