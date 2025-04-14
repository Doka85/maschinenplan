from flask_sqlalchemy import SQLAlchemy

# Initialisiere das SQLAlchemy-Objekt
db = SQLAlchemy()

class Machine(db.Model):
    __tablename__ = 'machine'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'<Machine {self.name}>'

class Task(db.Model):
    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True)
    machine_id = db.Column(db.Integer, db.ForeignKey('machine.id'), nullable=False)
    part_number = db.Column(db.String(50))
    description = db.Column(db.String(200))
    duration_hours = db.Column(db.Integer)
    kw = db.Column(db.Integer)
    year = db.Column(db.Integer)  # Spalte für das Jahr
    status = db.Column(db.String(50))
    prio = db.Column(db.Integer)  # Spalte für die Priorität (1, 2, 3)

    # Beziehung zur Maschine
    machine = db.relationship('Machine', backref=db.backref('tasks', lazy=True))

    def __init__(self, machine_id, part_number, description, duration_hours, kw, year, status, prio):
        self.machine_id = machine_id
        self.part_number = part_number
        self.description = description
        self.duration_hours = duration_hours
        self.kw = kw
        self.year = year  # Jahr speichern
        self.status = status
        self.prio = prio  # Priorität speichern

    def __repr__(self):
        return f'<Task {self.description} - Machine {self.machine_id} - Priority {self.prio}>'
