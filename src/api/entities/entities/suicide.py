import uuid
from datetime import datetime

class Suicide:
    def __int__(self,id, year,min_age,max_age,tax,population_no,suicides_no,generation,gdp_for_year,hdi_for_year,gdp_per_capita,id_country,country, created_on=None, updated_on=None):
        self.year = year
        self.id = id or uuid.uuid4()
        self.min_age = min_age
        self.max_age = max_age
        self.tax = tax
        self.population_no = population_no
        self.suicides_no = suicides_no
        self.generation = generation
        self.gdp_for_year = gdp_for_year
        self.hdi_for_year = hdi_for_year
        self.gdp_per_capita = gdp_per_capita
        self.year = year
        self.id_country = id_country
        self.country = country
        self.created_on = created_on or datetime.now()
        self.updated_on = updated_on or datetime.now()