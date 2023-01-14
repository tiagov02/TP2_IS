import uuid
from datetime import datetime

class Country:
    def __init__(self,name,geom,id=None, created_on=None,updated_on= None):
        self.id = id or uuid.uuid4(),
        self.name = name
        self.geom = geom or None
        self.created_on = created_on or datetime.now()
        self.updated_on = updated_on or datetime.now()