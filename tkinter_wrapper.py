from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLineEdit, QLabel, QDialog,
    QVBoxLayout, QGridLayout, QComboBox, QMessageBox, QWidget
)
import traceback
from database_wrapper import Database


class GuiBackEnd(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Voorzieningen Bewerken en Verwijderen")

        # Maak een hoofdwidget en layout
        self.central_widget = QWidget()
        self.layout = QGridLayout(self.central_widget)

        self.setCentralWidget(self.central_widget)

        # Voorbeeld van een knop voor toevoegen
        self.toevoegen_button = QPushButton("Toevoegen", self)
        self.toevoegen_button.clicked.connect(self.toevoegen_voorziening)

        # Voorbeeld van een knop voor verwijderen
        self.verwijderen_button = QPushButton("Verwijderen", self)
        self.verwijderen_button.clicked.connect(self.verwijder_voorziening)

        # Voorbeeld van een knop voor bewerken
        self.bewerken_button = QPushButton("Bewerken", self)
        self.bewerken_button.clicked.connect(self.bewerk_voorziening)

        # Voeg knoppen toe aan de layout
        self.layout.addWidget(self.toevoegen_button, 0, 0)
        self.layout.addWidget(self.verwijderen_button, 0, 1)
        self.layout.addWidget(self.bewerken_button, 0, 2)


# Toevoeging van een dialoogvenster voor het toevoegen van attracties
class AttractieToevoegenDialoog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Attractie Toevoegen")

        self.layout = QGridLayout(self)
        # ID invoerveld
       # self.id_label = QLabel("id:")
       # self.id_entry = QLineEdit(self)
       # self.layout.addWidget(self.id_label, 0, 0)
       # self.layout.addWidget(self.id_entry, 0, 1)
        # Naam invoerveld
        self.naam_label = QLabel("naam:")
        self.naam_entry = QLineEdit(self)
        self.layout.addWidget(self.naam_label, 1, 0)
        self.layout.addWidget(self.naam_entry, 1, 1)

        # Type invoerveld
        self.type_label = QLabel("type:")
        self.type_entry = QComboBox(self)
        self.type_entry.addItems(["achtbaan", "water", "draaien", "familie", "simulator"])
        self.layout.addWidget(self.type_label, 2, 0)
        self.layout.addWidget(self.type_entry, 2, 1)

        # Overdekt (ja/nee) invoerveld
        self.overdekt_label = QLabel("overdekt:")
        self.overdekt_entry = QComboBox(self)
        self.overdekt_entry.addItems(["Ja", "Nee"])
        self.layout.addWidget(self.overdekt_label, 3, 0)
        self.layout.addWidget(self.overdekt_entry, 3, 1)

        # Geschatte wachttijd invoerveld
        self.wachttijd_label = QLabel("Geschatte Wachttijd (min):")
        self.wachttijd_entry = QLineEdit(self)
        self.layout.addWidget(self.wachttijd_label, 4, 0)
        self.layout.addWidget(self.wachttijd_entry, 4, 1)

        # Doorlooptijd invoerveld
        self.doorlooptijd_label = QLabel("Doorlooptijd (min):")
        self.doorlooptijd_entry = QLineEdit(self)
        self.layout.addWidget(self.doorlooptijd_label, 5, 0)
        self.layout.addWidget(self.doorlooptijd_entry, 5, 1)

        # Actief (ja/nee) invoerveld
        self.actief_label = QLabel("Actief:")
        self.actief_entry = QComboBox(self)
        self.actief_entry.addItems(["Ja", "Nee"])
        self.layout.addWidget(self.actief_label, 6, 0)
        self.layout.addWidget(self.actief_entry, 6, 1)

        # Minimale lengte invoerveld
        self.min_lengte_label = QLabel("Minimale Lengte (cm):")
        self.min_lengte_entry = QLineEdit(self)
        self.layout.addWidget(self.min_lengte_label, 7, 0)
        self.layout.addWidget(self.min_lengte_entry, 7, 1)

        # Maximale lengte invoerveld
        self.max_lengte_label = QLabel("Maximale Lengte (cm):")
        self.max_lengte_entry = QLineEdit(self)
        self.layout.addWidget(self.max_lengte_label, 8, 0)
        self.layout.addWidget(self.max_lengte_entry, 8, 1)

        # Minimale leeftijd invoerveld
        self.min_leeftijd_label = QLabel("Minimale Leeftijd:")
        self.min_leeftijd_entry = QLineEdit(self)
        self.layout.addWidget(self.min_leeftijd_label, 9, 0)
        self.layout.addWidget(self.min_leeftijd_entry, 9, 1)

        # Maximale gewicht invoerveld
        self.max_gewicht_label = QLabel("Maximale Gewicht (kg):")
        self.max_gewicht_entry = QLineEdit(self)
        self.layout.addWidget(self.max_gewicht_label, 10, 0)
        self.layout.addWidget(self.max_gewicht_entry, 10, 1)

        # Opslaan en annuleren knoppen
        self.opslaan_button = QPushButton("Apply", self)
        self.opslaan_button.clicked.connect(self.accept)
        self.annuleren_button = QPushButton("Cancel", self)
        self.annuleren_button.clicked.connect(self.reject)

        self.layout.addWidget(self.opslaan_button, 12, 0)
        self.layout.addWidget(self.annuleren_button, 12, 1)

    def get_IOdata(self):
        return {
            #"id": self.id_entry.text(),
            "naam": self.naam_entry.text(),
            "type": self.type_entry.currentText(),
            "overdekt": self.overdekt_entry.currentText(),
            "geschatte_wachttijd": self.wachttijd_entry.text(),
            "doorlooptijd": self.doorlooptijd_entry.text(),
            "actief": self.actief_entry.currentText(),
            "attractie_min_lengte": self.min_lengte_entry.text() or None,
            "attractie_max_lengte": self.max_lengte_entry.text() or None,
            "attractie_min_leeftijd": self.min_leeftijd_entry.text() or None,
            "attractie_max_gewicht": self.max_gewicht_entry.text() or None,

        }

    def add_into_database(self):
        data = self.get_IOdata()

        try:
            db = Database(host="localhost", gebruiker="user", wachtwoord="password", database="attractiepark_software")
            db.connect()

            # SQL-query om een attractie toe te voegen
            query = """
            INSERT INTO voorziening (naam, type, overdekt, geschatte_wachttijd, doorlooptijd, actief, attractie_min_lengte, attractie_max_lengte, attractie_min_leeftijd, attractie_max_gewicht) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            
            """

            params = (
                #int(data["id"]),  # Ensure id is an integer
                data["naam"],  # naam is a string
                data["type"],  # type is a string
                1 if data["overdekt"].lower() == "ja" else 0,  # overdekt is stored as 1 or 0 (tinyint)
                int(data["geschatte_wachttijd"]),  # wachttijd should be an integer
                int(data["doorlooptijd"]),  # doorlooptijd should be an integer
                1 if data["actief"].lower() == "ja" else 0,  # actief is stored as 1 or 0 (tinyint)
                int(data["attractie_min_lengte"]) if data["attractie_min_lengte"] else None,  # Convert to int or None if empty
                int(data["attractie_max_lengte"]) if data["attractie_max_lengte"] else None,  # Convert to int or None if empty
                int(data["attractie_min_leeftijd"]) if data["attractie_min_leeftijd"] else None,  # Convert to int or None if empty
                int(data["attractie_max_gewicht"]) if data["attractie_max_gewicht"] else None,  # Convert to int or None if empty


            )

            print(f"Data to insert: {data}")
            print("Verbonden met de database!")
            print("Query:", query)
            print("Params:", params)

            # Execute the query
            db.execute_query(query)

            QMessageBox.information(self, "Succes", "Attractie succesvol toegevoegd.")
            db.close()

        except Exception as e:
            print("Fout bij uitvoeren van query:", e)
            db.close()


class AttractieBewerkenDialoog(QDialog):
    def __init__(self, parent=None, bestaande_gegevens=None):
        super().__init__(parent)
        self.setWindowTitle("Attractie Bewerken")

        self.layout = QGridLayout(self)

        # Vul de invoervelden met bestaande gegevens als we bewerken
        self.bestaande_gegevens = bestaande_gegevens or {
            "naam": "",
            "type": "",
            "min_lengte": "",
            "max_lengte": "",
            "min_leeftijd": "",
            "max_gewicht": "",
            "wachttijd": "",
            "doorlooptijd": "",
            "overdekt": "Nee",
            "actief": "Ja",
            "product": ""
        }

        # Naam invoerveld
        self.naam_label = QLabel("Naam:")
        self.naam_entry = QLineEdit(self)
        self.naam_entry.setText(self.bestaande_gegevens["naam"])
        self.layout.addWidget(self.naam_label, 0, 0)
        self.layout.addWidget(self.naam_entry, 0, 1)

        # Type invoerveld
        self.type_label = QLabel("Type:")
        self.type_entry = QComboBox(self)
        self.type_entry.addItems(["Achtbaan", "Water", "Draaien", "Familie", "Simulator"])
        self.type_entry.setCurrentText(self.bestaande_gegevens["type"])
        self.layout.addWidget(self.type_label, 1, 0)
        self.layout.addWidget(self.type_entry, 1, 1)

        # Minimale lengte invoerveld
        self.min_lengte_label = QLabel("Minimale Lengte (cm):")
        self.min_lengte_entry = QLineEdit(self)
        self.min_lengte_entry.setText(self.bestaande_gegevens["min_lengte"])
        self.layout.addWidget(self.min_lengte_label, 2, 0)
        self.layout.addWidget(self.min_lengte_entry, 2, 1)

        # Maximale lengte invoerveld
        self.max_lengte_label = QLabel("Maximale Lengte (cm):")
        self.max_lengte_entry = QLineEdit(self)
        self.max_lengte_entry.setText(self.bestaande_gegevens["max_lengte"])
        self.layout.addWidget(self.max_lengte_label, 3, 0)
        self.layout.addWidget(self.max_lengte_entry, 3, 1)

        # Minimale leeftijd invoerveld
        self.min_leeftijd_label = QLabel("Minimale Leeftijd:")
        self.min_leeftijd_entry = QLineEdit(self)
        self.min_leeftijd_entry.setText(self.bestaande_gegevens["min_leeftijd"])
        self.layout.addWidget(self.min_leeftijd_label, 4, 0)
        self.layout.addWidget(self.min_leeftijd_entry, 4, 1)

        # Maximale gewicht invoerveld
        self.max_gewicht_label = QLabel("Maximale Gewicht (kg):")
        self.max_gewicht_entry = QLineEdit(self)
        self.max_gewicht_entry.setText(self.bestaande_gegevens["max_gewicht"])
        self.layout.addWidget(self.max_gewicht_label, 5, 0)
        self.layout.addWidget(self.max_gewicht_entry, 5, 1)

        # Gemiddelde wachttijd invoerveld
        self.wachttijd_label = QLabel("Gemiddelde Wachttijd (min):")
        self.wachttijd_entry = QLineEdit(self)
        self.wachttijd_entry.setText(self.bestaande_gegevens["wachttijd"])
        self.layout.addWidget(self.wachttijd_label, 6, 0)
        self.layout.addWidget(self.wachttijd_entry, 6, 1)

        # Doorlooptijd invoerveld
        self.doorlooptijd_label = QLabel("Doorlooptijd (min):")
        self.doorlooptijd_entry = QLineEdit(self)
        self.doorlooptijd_entry.setText(self.bestaande_gegevens["doorlooptijd"])
        self.layout.addWidget(self.doorlooptijd_label, 7, 0)
        self.layout.addWidget(self.doorlooptijd_entry, 7, 1)

        # Overdekt (ja/nee) invoerveld
        self.overdekt_label = QLabel("Overdekt:")
        self.overdekt_entry = QComboBox(self)
        self.overdekt_entry.addItems(["Ja", "Nee"])
        self.overdekt_entry.setCurrentText(self.bestaande_gegevens["overdekt"])
        self.layout.addWidget(self.overdekt_label, 8, 0)
        self.layout.addWidget(self.overdekt_entry, 8, 1)

        # Actief (ja/nee) invoerveld
        self.actief_label = QLabel("Actief:")
        self.actief_entry = QComboBox(self)
        self.actief_entry.addItems(["Ja", "Nee"])
        self.actief_entry.setCurrentText(self.bestaande_gegevens["actief"])
        self.layout.addWidget(self.actief_label, 9, 0)
        self.layout.addWidget(self.actief_entry, 9, 1)

        # Productaanbod invoerveld
        self.product_label = QLabel("Productaanbod:")
        self.product_entry = QLineEdit(self)
        self.product_entry.setText(self.bestaande_gegevens["product"])
        self.layout.addWidget(self.product_label, 10, 0)
        self.layout.addWidget(self.product_entry, 10, 1)

        # Opslaan knop
        self.opslaan_button = QPushButton("Opslaan", self)
        self.opslaan_button.clicked.connect(GuiBackEnd.update_database())
        self.layout.addWidget(self.opslaan_button, 11, 1)

    def get_IOdata(self):
        return {
            "naam": self.naam_entry.text(),
            "type": self.type_entry.currentText(),
            "min_lengte": self.min_lengte_entry.text(),
            "max_lengte": self.max_lengte_entry.text(),
            "min_leeftijd": self.min_leeftijd_entry.text(),
            "max_gewicht": self.max_gewicht_entry.text(),
            "wachttijd": self.wachttijd_entry.text(),
            "doorlooptijd": self.doorlooptijd_entry.text(),
            "overdekt": self.overdekt_entry.currentText(),
            "actief": self.actief_entry.currentText(),
            "product": self.product_entry.text(),
        }

    def update_database(self, data):
        try:
            db = Database(host="localhost", gebruiker="user", wachtwoord="password", database="attractiepark_software")
            db.connect()

            # SQL-query om een attractie bij te werken
            query = """
               UPDATE voorziening
               SET naam = ?, type = ?, overdekt = ?, geschatte_wachttijd = ?, doorlooptijd = ?,
                   actief = ?, attractie_min_lengte = ?, attractie_max_lengte = ?, 
                   attractie_min_leeftijd = ?, attractie_max_gewicht = ?, productaanbod = ?
               WHERE id = ?  -- Zorg ervoor dat je hier het juiste ID gebruikt
               """

            # Update de attractie in de database
            db.execute_query(query, (
                data['naam'],
                data['type'],
                data['productaanbod'],
                float(data['min_lengte']) if data['min_lengte'] else None,
                float(data['max_lengte']) if data['max_lengte'] else None,
                int(data['min_leeftijd']) if data['min_leeftijd'] else None,
                int(data['max_gewicht']) if data['max_gewicht'] else None,
                int(data['wachttijd']) if data['wachttijd'] else None,
                int(data['doorlooptijd']) if data['doorlooptijd'] else None,
                data['overdekt'] == "Ja",  # Omzetten van string naar boolean
                data['actief'] == "Ja",  # Omzetten van string naar boolean
                1  # Dummy ID voor demonstratie; dit moet het ID zijn van de attractie die je wilt bijwerken
            ))

            QMessageBox.information(self, "Succes", "Attractie succesvol bijgewerkt.")
            db.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Fout bij het bijwerken: {e}")
            db.close()
