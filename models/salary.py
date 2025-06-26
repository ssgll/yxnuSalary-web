from . import db
import json
from sqlalchemy.orm import reconstructor

class Salary(db.Model):
    __bind_key__ = "salary_db"
    __tablename__ = "DWD_JSGZXXB"

    id = db.Column(db.Integer,name="id", primary_key=True, autoincrement=False)
    year = db.Column(db.String(8),name='FFND',nullable=False)
    frequency = db.Column(db.Integer,name='FFCS',nullable=False)
    user_id = db.Column(db.String(16),name='ZYDM',nullable=False)
    time = db.Column(db.String(8),name='FFRQ',nullable=False)
    data = db.Column(db.Text,name='JSON')

    _parsed_data = None

    @reconstructor
    def __init_on_load(self):
        self.parse_data()

    
    def parse_data(self):
        self._parsed_data = json.loads(self.data)

    def __repr__(self):
        return f'<Salary {self.id} - {self.year}>'
    