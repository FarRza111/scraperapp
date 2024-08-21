import pycountry
from typing import List
from itertools import islice


def add_slash_to_country(countries: List[str]) -> List[str]:
  return [f"/{country}/" for country in countries]


def chunks(iterable, size):
    iterator = iter(iterable)
    for first in iterator:
        yield [first] + list(islice(iterator, size - 1))


def read_files(path):
  data_frame= [pd.read_excel(file) for file in os.listdir(mypath) if re.search(".xlsx", file) ]
  return pd.concat(data_frame)




if __name__ == "__main__":
  
  mypath = os.getcwd()
  # data = read_files(mypath)
  # data.to_excel("swift_codes_bic.xlsx")
  
  list_of_countries: List[str] = [iso_country.name.lower() for iso_country in  pycountry.countries]
  test = add_slash_to_country(list_of_countries)

  chunked_list1 = list(map(str, list(chunks(test, 30))[:9]))

  for chunk in chunked_list1:
      print(chunk)

  
