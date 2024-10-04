from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QGridLayout, QDialog
)
from PyQt5.QtCore import Qt
from database_wrapper import Database
from tkinter_wrapper import AttractieToevoegenDialoog, AttractieBewerkenDialoog, GuiBackEnd


class VoorzieningenWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Attractie beheer")
        self.setGeometry(100, 100, 1200, 800)

        # Maak een hoofdwidget en layout
        self.central_widget = QWidget(self)
        self.layout = QGridLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)

        # Connect met de database
        self.db = Database(host="localhost", gebruiker="user", wachtwoord="password", database="attractiepark_software")
        self.db.connect()

        # Haal attracties op
        self.attracties = self.attracties_ophalen()

        # Definieer de attributen van een attractie
        self.attributen_attractie = [
            {"naam": "naam", "type": "string", "verplicht": True},
            {"naam": "type", "type": "options", "opties": ["Achtbaan", "Water", "Draaien", "Familie", "Simulator"], "verplicht": True},
            {"naam": "overdekt", "type": "int", "verplicht": True},
            {"naam": "geschatte_wachttijd", "type": "int", "verplicht": True},
            {"naam": "doorlooptijd", "type": "int", "verplicht": True},
            {"naam": "actief", "type": "boolean", "verplicht": False},
            {"naam": "attractie_min_lengte", "type": "int"},
            {"naam": "attractie_max_lengte", "type": "int"},
            {"naam": "attractie_min_leeftijd", "type": "int"},
            {"naam": "attractie_max_gewicht", "type": "int"},
        ]

        # Voeg tabel toe voor attracties
        self.attractie_tabel = QTableWidget(self)
        self.attractie_tabel.setRowCount(len(self.attracties))
        self.attractie_tabel.setColumnCount(len(self.attributen_attractie))
        self.attractie_tabel.setHorizontalHeaderLabels([attr["naam"] for attr in self.attributen_attractie])
        self.layout.addWidget(self.attractie_tabel, 0, 0, 1, 3)

        # Vul de tabel met gegevens
        self.vul_tabel()

        # Knoppen voor toevoegen, bewerken, verwijderen
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
        query = """
        SELECT naam, type, overdekt, geschatte_wachttijd, doorlooptijd, actief, 
               attractie_min_lengte, attractie_max_lengte, attractie_min_leeftijd, 
               attractie_max_gewicht, productaanbod 
        FROM voorziening
        """
        results = self.db.execute_query(query)
        return results

    def vul_tabel(self):
        for rij, attractie in enumerate(self.attracties):
            for kolom, waarde in enumerate(attractie):
                self.attractie_tabel.setItem(rij, kolom, QTableWidgetItem(str(waarde)))

    def toevoegen_voorziening(self):
        dialog = AttractieToevoegenDialoog(self)
        if dialog.exec_() == QDialog.Accepted:
            dialog.add_into_database()


    def bewerken_voorziening(self):
        dialog = AttractieBewerkenDialoog(self)
        if dialog.exec_():
            print("Attractie bewerken:", dialog.get_IOdata())


    def verwijderen_voorziening(self):
        print("Functie voor voorziening verwijderen")


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = VoorzieningenWindow()
    window.show()
    sys.exit(app.exec_())
