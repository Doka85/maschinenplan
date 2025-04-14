from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # Flask-Migrate importieren
from models import db, Machine, Task  # Hier sicherstellen, dass Machine importiert wird
from datetime import datetime, timedelta

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////app/belegung.db'  # Pfad zur DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

migrate = Migrate(app, db)  # Flask-Migrate initialisieren

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
    prio = db.Column(db.Integer)  # Neue Spalte für Priorität
    status = db.Column(db.String(50))

    # Beziehung zur Maschine
    machine = db.relationship('Machine', backref=db.backref('tasks', lazy=True))

    def __init__(self, machine_id, part_number, description, duration_hours, kw, year, prio, status):
        self.machine_id = machine_id
        self.part_number = part_number
        self.description = description
        self.duration_hours = duration_hours
        self.kw = kw
        self.year = year  # Jahr speichern
        self.prio = prio  # Priorität speichern
        self.status = status

    def __repr__(self):
        return f'<Task {self.description} - Machine {self.machine_id}>'
    
 
# Berechnung der aktuellen Kalenderwoche
def get_year_and_week(week_number, current_year):
    # Um die Kalenderwoche für das neue Jahr zu berechnen, wird der 1. Januar des aktuellen Jahres
    # genommen und die entsprechenden Tage zur Berechnung der Kalenderwoche hinzugefügt
    first_day_of_year = datetime(current_year, 1, 1)
    delta_days = timedelta(weeks=week_number - 1)
    new_date = first_day_of_year + delta_days
    return new_date.year, new_date.isocalendar()[1]  # Gibt das Jahr und die Kalenderwoche zurück

    
    # Bestimme das Jahr und die Woche
    return target_date.year, target_date.isocalendar()[1]
    
def get_current_week():
    today = datetime.today()
    return today.isocalendar()[1]

 
@app.route('/')
def index():
    current_week = get_current_week()
    machines = Machine.query.all()
    return render_template('index.html', machines=machines, current_week=current_week)

from flask import render_template
from sqlalchemy import func

@app.route('/admin', methods=['GET', 'POST'])
def admin_view():
    if request.method == 'POST':
        # Formularfelder abfragen
        machine_id = request.form.get('machine_id', type=int)
        part_number = request.form.get('part_number')
        description = request.form.get('description')
        duration = request.form.get('duration_hours')
        kw = request.form.get('kw')
        year = request.form.get('year', type=int) or datetime.now().year  # Standardwert für das Jahr
        prio = request.form.get('prio', type=int)
        status = request.form.get('status')

        # Aufgabe speichern
        task = Task(
            machine_id=machine_id,
            part_number=part_number,
            description=description,
            duration_hours=duration,
            kw=kw,
            year=year,
            status=status,
            prio=prio
        )
        db.session.add(task)
        db.session.commit()

        return redirect(url_for('admin_view'))

    current_week = get_current_week()

    # Alle Aufgaben anzeigen
    tasks = Task.query.all()

    # Maschinen laden
    machines = Machine.query.all()

    # Aktuelles Jahr übergeben
    current_year = datetime.now().year

    # Berechnung der Wochen und Jahre, die tatsächlich in der DB existieren
    unique_weeks_years = db.session.query(Task.year, Task.kw).distinct().all()
    weeks_years = sorted(unique_weeks_years, key=lambda x: (x[0], x[1]))  # nach Jahr und Woche sortieren

    # Berechnung der summierten Stunden pro Maschine und Kalenderwoche (einschließlich Jahr)
    hours_per_machine_kw = {}
    for machine in machines:
        for year, week in weeks_years:  # Iteriere nur über existierende Wochen/Jahre
            total_duration = db.session.query(db.func.sum(Task.duration_hours)).filter(
                Task.machine_id == machine.id,
                Task.kw == week,
                Task.year == year
            ).scalar() or 0  # Falls keine Aufgabe für diese Woche existiert, setze 0 Stunden
            hours_per_machine_kw[(machine.id, year, week)] = total_duration

    return render_template('admin.html', tasks=tasks, current_week=current_week, current_year=current_year, machines=machines, hours_per_machine_kw=hours_per_machine_kw, weeks_years=weeks_years)

   
@app.route('/maschine/<int:machine_id>', methods=['GET', 'POST'])
def maschine_view(machine_id):
    machine = Machine.query.get_or_404(machine_id)

    # Alle Aufgaben für die Maschine holen, die nicht den Status 'Fertig' haben, sortiert nach Jahr, KW und Priorität
    tasks = Task.query.filter(Task.machine_id == machine_id, Task.status != 'Fertig').order_by(Task.year, Task.kw, Task.prio).all()

    # Wenn der Fertig-Button gedrückt wurde, setzen wir den Status auf 'Fertig'
    if request.method == 'POST':
        task_id = request.form.get('task_id')  # Aufgabe auswählen
        task = Task.query.get(task_id)
        if task:
            task.status = 'Fertig'
            db.session.commit()
            return redirect(url_for('maschine_view', machine_id=machine_id))  # Zurück zur Maschinenansicht

    current_week = get_current_week()

    return render_template('maschine_view.html', machine=machine, tasks=tasks, current_week=current_week)


    
@app.route('/update_task_status/<int:task_id>', methods=['POST'])
def update_task_status(task_id):
    # Hole die Aufgabe aus der DB
    task = Task.query.get_or_404(task_id)

    # Setze den Status auf 'Fertig'
    task.status = 'Fertig'

    # Speichere die Änderung in der Datenbank
    db.session.commit()

    # Leite zurück zum Maschinenview
    return redirect(url_for('maschine_view', machine_id=task.machine_id))

@app.route('/delete/<int:task_id>', methods=['GET'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect('/admin')  # Nach dem Löschen zurück zum Admin-Bereich

@app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    
    # Maschinen laden
    machines = Machine.query.all()

    if request.method == 'POST':
        # Formularfelder abfragen
        task.machine_id = request.form.get('machine_id', type=int)
        task.part_number = request.form.get('part_number')
        task.description = request.form.get('description')
        task.duration_hours = request.form.get('duration_hours', type=int)
        task.kw = request.form.get('kw', type=int)
        task.year = request.form.get('year', type=int) or datetime.now().year  # Standardwert für Jahr
        task.prio = request.form.get('prio', type=int)
        task.status = request.form.get('status')

        db.session.commit()

        # Zurück zur Admin-Seite
        return redirect(url_for('admin_view'))

    return render_template('edit_task.html', task=task, machines=machines)




if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Hier wird sicher gestellt, dass die Tabellen erstellt werden
    app.run(host="0.0.0.0", port=5000)
