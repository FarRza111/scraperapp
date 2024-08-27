import os
import logging
import pandas as pd
from typing import List, Optional
from pydantic import BaseModel, Field, validator, ValidationError

# Set up logging
logging.basicConfig(format="%(levelname)s:%(name)s:(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
BASE_DIR = os.getcwd()
FOLDER = "data_folder"
FILE = "account_info_details.xlsx"
RELEVANT_DIRECTORY = os.path.join(BASE_DIR, FOLDER)

# Pydantic model for validation
class Swift(BaseModel):
    Country: str = Field(..., min_length=1, max_length=2)
    iban_checksum: int = Field(..., alias='IBAN Checksum')

    @validator('Country')
    def validate_country(cls, v):
        if len(v) < 2:
            raise ValueError("Country code should be exactly 2 characters.")
        return v

    @validator('iban_checksum')
    def validate_swiftchecksum(cls, v):
        if not isinstance(v, int) or v > 100:
            raise TypeError("IBAN Checksum should be an integer and less than or equal to 10.")
        return v

# Main function
def main():
    if os.path.exists(RELEVANT_DIRECTORY):
        mlist = os.listdir(RELEVANT_DIRECTORY)
        data = pd.read_excel(os.path.join(RELEVANT_DIRECTORY, FILE))
        print(data)
    else:
        os.mkdir(RELEVANT_DIRECTORY)

    df = data.to_dict(orient='records')
    try:
        for val in df:
            Swift(**val)
    except ValidationError as e:
        print(e)
        logger.error(f'Validation error: {e}')

# Entry point of the script
if __name__ == "__main__":
    main()
