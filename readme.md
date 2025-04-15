# Maschinenplan Projekt

Willkommen zum **Maschinenplan-Projekt**! 🎉

Dieses Projekt bietet eine effiziente und benutzerfreundliche Verwaltung von Maschinen und deren Aufgaben in einer Werkstatt oder einem Produktionsumfeld. Die App ermöglicht es, Maschinen hinzuzufügen, Aufgaben zu verwalten, und eine detaillierte Stundenübersicht pro Maschine und Kalenderwoche zu erhalten.

## Features

- **Maschinenverwaltung**: Füge Maschinen hinzu, bearbeite oder lösche sie.
- **Aufgabenverwaltung**: Erstelle, bearbeite und lösche Aufgaben für Maschinen.
- **Sortierte Aufgabenanzeige**: Aufgaben werden nach Maschine, Jahr, Kalenderwoche und Priorität sortiert.
- **Stundenübersicht**: Detaillierte Ansicht über die Arbeitsstunden pro Maschine und Kalenderwoche.
- **Automatisches Laden**: Maschinenansicht wird alle 5 Minuten automatisch aktualisiert.
- **Benutzerfreundlich**: Einfacher Zugang zu allen Funktionen und eine übersichtliche Darstellung.

## Technologie

Dieses Projekt verwendet:

- **Flask**: Für das Backend und die Webserver-Logik.
- **SQLite**: Für die Datenbank, die alle Maschinen und Aufgaben speichert.
- **Jinja2**: Für die Templates, die die Seiten rendern.
- **HTML/CSS**: Für das Design der Benutzeroberfläche.
- **Docker**: Für die Containerisierung der Anwendung und die Verwaltung der Entwicklungsumgebung.

## Installation

### 1. Docker-Setup

Stelle sicher, dass Docker auf deinem System installiert ist. Falls nicht, folge den offiziellen Anweisungen zur Installation von Docker.

### 2. Klone das Repository

Klonen Sie das Projekt mit folgendem Befehl:

```
bashKopierengit clone https://github.com/Doka85/maschinenplan.git
```

### 3. Docker-Container starten

Navigiere in das Verzeichnis des geklonten Repositories und baue den Docker-Container:

```
bashKopierencd maschinenplan
docker-compose up --build
```

Dies startet sowohl die Anwendung als auch die Datenbank.

### 4. Zugriff auf die Anwendung

Sobald der Container läuft, kannst du die Anwendung unter `http://localhost:4711` in deinem Webbrowser öffnen.

## Verwendete Routen

### `/admin`

- **GET**: Zeigt die Verwaltungsseite an, auf der du Maschinen und Aufgaben hinzufügen kannst.
- **POST**: Verarbeitet die Erstellung neuer Maschinen oder Aufgaben.

### `/maschine/<int:machine_id>`

- **GET**: Zeigt die Aufgaben für eine bestimmte Maschine an.
- **POST**: Markiert eine Aufgabe als "Fertig".

### `/edit_task/<int:task_id>`

- **GET**: Zeigt die Bearbeitungsansicht einer bestimmten Aufgabe an.
- **POST**: Speichert die Änderungen an einer Aufgabe.

### `/delete/<int:task_id>`

- **POST**: Löscht eine Aufgabe.

## To-Do

- Verbesserung der Benutzeroberfläche.
- Automatische Benachrichtigungen für Maschinen und Aufgaben.
- Erweiterung der Filtermöglichkeiten für Aufgaben und Maschinen.

## Contributing

Wenn du zur Entwicklung des Projekts beitragen möchtest, folge diesen Schritten:

1. Forke das Repository.
2. Erstelle einen neuen Branch: `git checkout -b feature/neue-funktion`.
3. Nimm deine Änderungen vor und commite sie: `git commit -am 'Neue Funktion hinzugefügt'`.
4. Push den Branch auf GitHub: `git push origin feature/neue-funktion`.
5. Erstelle eine Pull-Anfrage.

## Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert.

