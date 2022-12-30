
from datetime import datetime

class Suicide:
    def __int__(self, year, country, created_on, updated_on):
        self.year = year
        self.country = country
        self.created_on = created_on or datetime.now()
        self.updated_on = updated_on or datetime.now()