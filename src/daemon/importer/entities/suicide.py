import xml.etree.ElementTree as ET
from src.daemon.importer.entities.country import Country


class Suicide:

    def __init__(self, id, country : Country, year, sex, minage, maxage, tax, population_no, suicides_no,
                 generation, gdp_for_year, hdi_for_year, gdp_per_capita):
        self.id = id
        self.country = []
        self.year = year
        self.sex = sex
        self.minage = minage
        self.maxage = maxage
        self.tax = tax
        self.population_no = population_no
        self.suicides_no = suicides_no
        self.generation = generation
        self.gdp_for_year = gdp_for_year
        self.hdi_for_year = hdi_for_year
        self.gdp_per_capita = gdp_per_capita

    def __init__(self,country : Country, year, sex, minage, maxage, tax, population_no, suicides_no,
                 generation, gdp_for_year, hdi_for_year, gdp_per_capita):
        self.country = country
        self.year = year
        self.sex = sex
        self.minage = minage
        self.maxage = maxage
        self.tax = tax
        self.population_no = population_no
        self.suicides_no = suicides_no
        self.generation = generation
        self.gdp_for_year = gdp_for_year
        self.hdi_for_year = hdi_for_year
        self.gdp_per_capita = gdp_per_capita


    def to_xml(self):
        el = ET.Element("Suicides")
        el.set("year", str(self.year))
        el.set("sex", str(self.sex))
        el.set("minage", str(self.minage))
        el.set("maxage", str(self.maxage))
        el.set("tax", str(self.tax))
        el.set("population_no", str(self.population_no))
        el.set("suicides_no", str(self.suicides_no))
        el.set("generation", str(self.generation))
        el.set("gdp_for_year", str(self.gdp_for_year))
        el.set("hdi_for_year", str(self.hdi_for_year))
        el.set("gdp_per_capita", str(self.gdp_per_capita))

        suicides = ET.Element("Suicides")
        for country in self.country:
            suicides.append(country.to_xml())
        el.append(suicides)
        return el







