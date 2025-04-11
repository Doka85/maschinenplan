from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Machine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    machine_id = db.Column(db.Integer, db.ForeignKey('machine.id'), nullable=False)
    part_number = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    duration_hours = db.Column(db.Float, nullable=False)
    kw = db.Column(db.Integer, nullable=False)  # Kalenderwoche
    status = db.Column(db.String, default='warteschlange')
    priority = db.Column(db.Integer, default=0)
    archived = db.Column(db.Boolean, default=False)

    machine = db.relationship('Machine', backref=db.backref('tasks', lazy=True))