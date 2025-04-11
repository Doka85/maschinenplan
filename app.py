from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models import db, Machine, Task  # Hier sicherstellen, dass Machine importiert wird
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////app/belegung.db'  # Pfad zur DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    machine_id = db.Column(db.Integer, nullable=False)
    part_number = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    duration_hours = db.Column(db.Float, nullable=False)
    kw = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    priority = db.Column(db.Integer, default=0)
    archived = db.Column(db.Boolean, default=False)
    
 
# Berechnung der aktuellen Kalenderwoche
def get_current_week():
    return datetime.now().isocalendar()[1]
 
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
        machine_id = request.form.get('machine_id', type=int)  # Achten auf Integer-Typ
        part_number = request.form.get('part_number')  # Teilenummer
        description = request.form.get('description')
        duration = request.form.get('duration_hours')
        kw = request.form.get('kw')
        status = request.form.get('status')

        # Aufgabe speichern
        task = Task(
            machine_id=machine_id,
            part_number=part_number,  # Teilenummer hinzufügen
            description=description,
            duration_hours=duration,
            kw=kw,
            status=status
        )
        db.session.add(task)
        db.session.commit()

        # Zurück zur Admin-Seite
        return redirect(url_for('admin_view'))

    current_week = get_current_week()

    # Alle Aufgaben anzeigen
    tasks = Task.query.all()

    # Maschinen laden
    machines = Machine.query.all()

    return render_template('admin.html', tasks=tasks, current_week=current_week, machines=machines)



   
@app.route('/maschine/<int:machine_id>')
def maschine_view(machine_id):
    machine = Machine.query.get_or_404(machine_id)
    current_week = get_current_week()
    tasks = Task.query.filter(Task.machine_id == machine_id, 
                              Task.kw != current_week,  # Filtere nach Kalenderwoche
                              Task.status != 'Fertig').all()  # Filtere nach Status "nicht erledigt"
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

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if request.method == 'POST':
        task.machine_id = request.form['machine_id']
        task.part_number = request.form['part_number']
        task.description = request.form['description']
        task.duration_hours = request.form['duration_hours']
        task.kw = request.form['kw']
        task.status = request.form['status']
        db.session.commit()
        return redirect('/admin')  # Nach dem Bearbeiten zurück zum Admin-Bereich

    return render_template('edit_task.html', task=task)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
