import uuid
from datetime import datetime

class Suicide:
    year = None
    id = None
    min_age = None
    max_age = None
    tax = None
    population_no = None
    suicides_no = None
    generation = None
    gdp_for_year = None
    hdi_for_year = None
    gdp_per_capita = None
    year = None
    id_country= None
    country = None
    created_on = None
    updated_on = None

    def __int__(self,id, year,min_age,max_age,tax,population_no,suicides_no,generation,gdp_for_year,hdi_for_year,gdp_per_capita,id_country,country = None, created_on=None, updated_on=None):
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
        self.country = country or self.find_country(self, id_country)
        self.created_on = created_on or datetime.now()
        self.updated_on = updated_on or datetime.now()

    def find_country(self,id_country):
        return "a"