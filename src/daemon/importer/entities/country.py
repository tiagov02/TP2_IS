import xml.etree.ElementTree as ET


class Country:
    def __init__(self, id, name, lat, lon):
        self.id = id
        self.name = name;
        self.lat = lat
        self.lon = lon

    def to_xml(self):
        el = ET.Element("Country")
        el.set("id", str(self.id))
        el.set("name", str(self.name))
        el.set("lat", str(self.lat))
        el.set("lon", str(self.lon))
        return el

    def get_id(self):
        return self.id

    def __str__(self):
        return f"name: {self.name}, id:{self.id}"


Country.counter = 0
