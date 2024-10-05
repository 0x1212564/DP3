from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QGridLayout, QDialog
)
from PyQt5.QtCore import Qt
from database_wrapper import Database
from tkinter_wrapper import AttractieToevoegenDialoog, AttractieBewerkenDialoog, GuiBackEnd, AttractieVerwijderenDialoog


class VoorzieningenWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_window()
        self.setup_database()

        # Haal attracties op en vul de tabel
        self.load_and_fill_table()

        # Voeg knoppen toe voor bewerkingen
        self.add_buttons()

    def setup_window(self):
        """Set up the main window."""
        self.setWindowTitle("Attractie beheer")
        self.setGeometry(100, 100, 1200, 800)

        # Hoofdwidget en layout
        self.central_widget = QWidget(self)
        self.layout = QGridLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)

    def setup_database(self):
        """Set up database connection."""
        self.db = Database(host="localhost", gebruiker="user", wachtwoord="password", database="attractiepark_software")
        self.db.connect()

    def load_and_fill_table(self):
        """Load data from the database and populate the table."""
        self.attracties = self.attracties_ophalen()

        # Definieer de attributen van een attractie
        self.attributen_attractie = [
            {"naam": "naam", "type": "string", "verplicht": True},
            {"naam": "type", "type": "options", "opties": ["Achtbaan", "Water", "Draaien", "Familie", "Simulator"], "verplicht": True},
            {"naam": "overdekt", "type": "int", "verplicht": True},
            {"naam": "geschatte wachttijd", "type": "int", "verplicht": True},
            {"naam": "doorlooptijd", "type": "int", "verplicht": True},
            {"naam": "actief", "type": "boolean", "verplicht": True},
            {"naam": "min lengte", "type": "int"},
            {"naam": "max lengte", "type": "int"},
            {"naam": "min leeftijd", "type": "int"},
            {"naam": "max gewicht", "type": "int"},
            {"naam": "product", "type": "string", "verplicht": False},
        ]

        # Tabel instellen
        self.setup_table()
        self.vul_tabel()

    def setup_table(self):
        """Create and set up the QTableWidget."""
        self.attractie_tabel = QTableWidget(self)
        self.attractie_tabel.setColumnCount(len(self.attributen_attractie))
        self.attractie_tabel.setHorizontalHeaderLabels([attr["naam"] for attr in self.attributen_attractie])
        self.layout.addWidget(self.attractie_tabel, 0, 0, 1, 3)

    def add_buttons(self):
        """Add buttons for adding, editing, and deleting rows."""
        self.toevoegen_button = QPushButton("Toevoegen", self)
        self.toevoegen_button.clicked.connect(self.toevoegen_voorziening)
        self.layout.addWidget(self.toevoegen_button, 1, 0)

        self.verwijderen_button = QPushButton("Verwijderen", self)
        self.verwijderen_button.clicked.connect(self.verwijderen_voorziening)
        self.layout.addWidget(self.verwijderen_button, 1, 1)

        self.bewerken_button = QPushButton("Bewerken", self)
        self.bewerken_button.clicked.connect(self.bewerken_voorziening)
        self.layout.addWidget(self.bewerken_button, 1, 2)

    def attracties_ophalen(self):
        """Fetch attraction data from the database."""
        query = """
        SELECT naam, type, overdekt, geschatte_wachttijd, doorlooptijd, actief, 
               attractie_min_lengte, attractie_max_lengte, attractie_min_leeftijd, 
               attractie_max_gewicht, productaanbod 
        FROM voorziening
        """
        return self.db.execute_query(query)

    def vul_tabel(self):
        """Fill the table with data."""
        self.attractie_tabel.setRowCount(len(self.attracties))
        for rij, attractie in enumerate(self.attracties):
            for kolom, waarde in enumerate(attractie):
                self.attractie_tabel.setItem(rij, kolom, QTableWidgetItem(str(waarde)))

    def refresh_data(self):
        self.setup_window()
        self.setup_database()
        self.load_and_fill_table()
        self.add_buttons()

    def toevoegen_voorziening(self):
        """Handle adding a new attraction."""
        dialog = AttractieToevoegenDialoog(self)
        if dialog.exec_() == QDialog.Accepted:
            dialog.add_into_database()
        self.refresh_data()

    def bewerken_voorziening(self):
        """Handle editing an attraction."""
        dialog = AttractieBewerkenDialoog(self)
        if dialog.exec_() == QDialog.Accepted:
            print("Attractie bewerken:", dialog.get_IOdata())
        self.refresh_data()

    def verwijderen_voorziening(self):
        """Handle deleting an attraction."""
        dialog = AttractieVerwijderenDialoog(self)
        dialog.exec_()
        self.refresh_data()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = VoorzieningenWindow()
    window.show()
    sys.exit(app.exec_())
