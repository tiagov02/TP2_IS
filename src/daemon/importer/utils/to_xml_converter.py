import csv
import xml.dom.minidom as md
import xml.etree.ElementTree as ET
#from entities.player import Player
import pandas as pd

class CSVtoXMLConverter:

    def __init__(self, path):
        self._reader = pd.read_csv(path)

    def to_xml(self):
        dataset = self._reader
        root = ET.Element('SUICIDES')
        for year, df_group in dataset.groupby('year'):
            i = 0
            years = ET.SubElement(root, 'YEAR', {'code': str(year)})
            for country, df_group_country in df_group.groupby('country'):
                countys = ET.SubElement(years, 'COUNTRY',{'name': str(country)})
                for item in df_group_country.iterrows():
                    aux = item[1].T
                    minAge = None
                    maxAge = None
                    if (aux['age'] == "75+ years"):
                        minAge = "75"
                        maxAge = "MAX"
                    else:
                        auxStr = str(aux['age']).split("-")
                        auxMax = str(auxStr[1]).split()
                        minAge = auxStr[0]
                        maxAge = auxMax[0]
                    suicides = ET.SubElement(countys, 'SUICIDE',
                                             {'sex': str(aux['sex']), 'minAge': str(minAge), 'maxAge': str(maxAge),
                                              'tax': str(aux['suicides/100k pop']),
                                              'population_no': str(aux['population']),
                                              'suicides_no': str(aux['suicides_no']),
                                              'generation': str(aux['generation']),
                                              'gdp_for_year': str(aux[' gdp_for_year ($) ']),
                                              'hdi_for_year': str(aux['HDI for year']),
                                              'gdp_per_capita': str(aux['gdp_per_capita ($)'])})

        return root

    def to_xml_str(self):
        xml_str = ET.tostring(self.to_xml(), encoding='utf8', method='xml').decode()
        dom = md.parseString(xml_str)
        return dom.toprettyxml()

