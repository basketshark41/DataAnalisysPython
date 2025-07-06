from app import db

class PartecipazioneLavoro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    anno = db.Column(db.Integer, nullable=False)
    regione = db.Column(db.String(50), nullable=False)
    valore = db.Column(db.Float, nullable=False)
    
class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type1 = db.Column(db.String(50))
    type2 = db.Column(db.String(50))
    total = db.Column(db.Integer)
    hp = db.Column(db.Integer)
    attack = db.Column(db.Integer)
    defense = db.Column(db.Integer)
    speed = db.Column(db.Integer)
    generation = db.Column(db.Integer)
    legendary = db.Column(db.Boolean, default=False)
    
class DatiPesca(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    anno = db.Column(db.Integer, nullable=False)
    regione = db.Column(db.String(100), nullable=False)
    occupazione = db.Column(db.Float, nullable=False)
    importanza_economica = db.Column(db.Float, nullable=False)
    produttivita = db.Column(db.Float, nullable=False)
