from PyQt5.QtWidgets import (
    QPushButton, QLineEdit, QLabel, QDialog,
    QVBoxLayout, QGridLayout, QComboBox, QMessageBox
)
from database_wrapper import Database

# Attraction addition dialogue and logic
class AttractieToevoegenDialoog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Attractie Toevoegen")

        self.layout = QGridLayout(self)

        # Naam entry label
        self.naam_label = QLabel("naam:")
        self.naam_entry = QLineEdit(self)
        self.layout.addWidget(self.naam_label, 1, 0)
        self.layout.addWidget(self.naam_entry, 1, 1)

        # Type entry label
        self.type_label = QLabel("type:")
        self.type_entry = QComboBox(self)
        self.type_entry.addItems(["achtbaan", "water", "draaien", "familie", "simulator"])
        self.layout.addWidget(self.type_label, 2, 0)
        self.layout.addWidget(self.type_entry, 2, 1)

        # Overdekt (ja/nee) entry label
        self.overdekt_label = QLabel("overdekt:")
        self.overdekt_entry = QComboBox(self)
        self.overdekt_entry.addItems(["Ja", "Nee"])
        self.layout.addWidget(self.overdekt_label, 3, 0)
        self.layout.addWidget(self.overdekt_entry, 3, 1)

        # Geschatte wachttijd entry label
        self.wachttijd_label = QLabel("Geschatte Wachttijd (min):")
        self.wachttijd_entry = QLineEdit(self)
        self.layout.addWidget(self.wachttijd_label, 4, 0)
        self.layout.addWidget(self.wachttijd_entry, 4, 1)

        # Doorlooptijd entry label
        self.doorlooptijd_label = QLabel("Doorlooptijd (min):")
        self.doorlooptijd_entry = QLineEdit(self)
        self.layout.addWidget(self.doorlooptijd_label, 5, 0)
        self.layout.addWidget(self.doorlooptijd_entry, 5, 1)

        # Actief (ja/nee) entry label
        self.actief_label = QLabel("Actief:")
        self.actief_entry = QComboBox(self)
        self.actief_entry.addItems(["Ja", "Nee"])
        self.layout.addWidget(self.actief_label, 6, 0)
        self.layout.addWidget(self.actief_entry, 6, 1)

        # Minimale lengte entry label
        self.min_lengte_label = QLabel("Minimale Lengte (cm):")
        self.min_lengte_entry = QLineEdit(self)
        self.layout.addWidget(self.min_lengte_label, 7, 0)
        self.layout.addWidget(self.min_lengte_entry, 7, 1)

        # Maximale lengte entry label
        self.max_lengte_label = QLabel("Maximale Lengte (cm):")
        self.max_lengte_entry = QLineEdit(self)
        self.layout.addWidget(self.max_lengte_label, 8, 0)
        self.layout.addWidget(self.max_lengte_entry, 8, 1)

        # Minimale leeftijd entry label
        self.min_leeftijd_label = QLabel("Minimale Leeftijd:")
        self.min_leeftijd_entry = QLineEdit(self)
        self.layout.addWidget(self.min_leeftijd_label, 9, 0)
        self.layout.addWidget(self.min_leeftijd_entry, 9, 1)

        # Maximale gewicht entry label
        self.max_gewicht_label = QLabel("Maximale Gewicht (kg):")
        self.max_gewicht_entry = QLineEdit(self)
        self.layout.addWidget(self.max_gewicht_label, 10, 0)
        self.layout.addWidget(self.max_gewicht_entry, 10, 1)

        # Productaanbod
        self.product_label = QLabel("Product:")
        self.product_entry = QLineEdit(self)
        self.layout.addWidget(self.product_label, 11, 0)
        self.layout.addWidget(self.product_entry, 11, 1)

        # Opslaan and Annuleren buttons
        self.opslaan_button = QPushButton("Toevoegen", self)
        self.opslaan_button.clicked.connect(self.accept)
        self.annuleren_button = QPushButton("Annuleren", self)
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
            "productaanbod":self.product_entry.text() or None,

        }

    def add_into_database(self):
        data = self.get_IOdata() #fetch data

        try:
            db = Database(host="localhost", gebruiker="user", wachtwoord="password", database="attractiepark_software")
            db.connect()

            # SQL-query to add into the table
            query = """
            INSERT INTO voorziening (naam, type, overdekt, geschatte_wachttijd, doorlooptijd, actief, attractie_min_lengte, attractie_max_lengte, attractie_min_leeftijd, attractie_max_gewicht, productaanbod) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            
            """

            params = (
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
                data["productaanbod"] if data["productaanbod"] else None,


            )

            print(f"Data to insert: {data}")
            print("Verbonden met de database!")
            print("Query:", query)
            print("Params:", params)

            # Execute the query
            db.execute_query(query, params)

            QMessageBox.information(self, "Succes", "Attractie succesvol toegevoegd.")
            db.close()

        except Exception as e:
            QMessageBox.information(self, "Error", f"Fout bij uitvoeren van query: {str(e)}")
            print("Fout bij uitvoeren van query:", e)
            db.close()

# Attraction editing dialogue and logic
class AttractieBewerkenDialoog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_attractie_id = None
        self.setWindowTitle("Attractie Bewerken")

        # Set up the layout for the dialog using QGridLayout
        self.layout = QGridLayout(self)

        # ID entry label
        self.id_label = QLabel("Attractie ID:")
        self.id_input = QLineEdit(self)
        self.layout.addWidget(self.id_label, 0, 0)
        self.layout.addWidget(self.id_input, 0, 1)

        # Search button
        self.search_button = QPushButton("Zoeken", self)
        self.search_button.clicked.connect(self.fetch_data)
        self.layout.addWidget(self.search_button, 0, 2)

        # Naam entry label
        self.naam_label = QLabel("Naam:")
        self.naam_entry = QLineEdit(self)
        self.layout.addWidget(self.naam_label, 1, 0)
        self.layout.addWidget(self.naam_entry, 1, 1)

        # Type entry label
        self.type_label = QLabel("Type:")
        self.type_entry = QComboBox(self)
        self.type_entry.addItems(["Achtbaan", "Water", "Draaien", "Familie", "Simulator"])
        self.layout.addWidget(self.type_label, 2, 0)
        self.layout.addWidget(self.type_entry, 2, 1)

        # Overdekt (ja/nee) entry label
        self.overdekt_label = QLabel("Overdekt:")
        self.overdekt_entry = QComboBox(self)
        self.overdekt_entry.addItems(["Ja", "Nee"])
        self.layout.addWidget(self.overdekt_label, 3, 0)
        self.layout.addWidget(self.overdekt_entry, 3, 1)

        # Geschatte wachttijd entry label
        self.wachttijd_label = QLabel("Geschatte Wachttijd (min):")
        self.wachttijd_entry = QLineEdit(self)
        self.layout.addWidget(self.wachttijd_label, 4, 0)
        self.layout.addWidget(self.wachttijd_entry, 4, 1)

        # Doorlooptijd entry label
        self.doorlooptijd_label = QLabel("Doorlooptijd (min):")
        self.doorlooptijd_entry = QLineEdit(self)
        self.layout.addWidget(self.doorlooptijd_label, 5, 0)
        self.layout.addWidget(self.doorlooptijd_entry, 5, 1)

        # Actief (ja/nee) entry label
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

        # Productaanbod invoerveld
        self.product_label = QLabel("Product:")
        self.product_entry = QLineEdit(self)
        self.layout.addWidget(self.product_label, 11, 0)
        self.layout.addWidget(self.product_entry, 11, 1)

        # Opslaan en annuleren knoppen
        self.opslaan_button = QPushButton("Opslaan", self)
        self.opslaan_button.clicked.connect(self.update_database)
        self.annuleren_button = QPushButton("Annuleren", self)
        self.annuleren_button.clicked.connect(self.reject)

        self.layout.addWidget(self.opslaan_button, 12, 0)
        self.layout.addWidget(self.annuleren_button, 12, 1)

        # Initializing the form fields
        self.hide_form()

    def hide_form(self):
        for widget in self.layout.children():
            if isinstance(widget, QLineEdit) or isinstance(widget, QComboBox):
                widget.hide()
        self.opslaan_button.hide()
        self.annuleren_button.hide()

    def show_form(self):
        for widget in self.layout.children():
            if isinstance(widget, QLineEdit) or isinstance(widget, QComboBox):
                widget.show()
        self.opslaan_button.show()
        self.annuleren_button.show()

    def fetch_data(self):
        attractie_id = self.id_input.text().strip()
        if not attractie_id.isdigit():
            QMessageBox.warning(self, "Ongeldig ID", "Voer een geldig numeriek attractie ID in.")
            return

        try:
            db = Database(host="localhost", gebruiker="user", wachtwoord="password", database="attractiepark_software")
            db.connect()

            query = "SELECT naam, type, overdekt, geschatte_wachttijd, doorlooptijd, actief, attractie_min_lengte, attractie_max_lengte, attractie_min_leeftijd, attractie_max_gewicht, productaanbod FROM voorziening WHERE id = %s"

            result = db.execute_query(query, (attractie_id,))

            if result:
                data = result[0]
                self.fill_form_with_data(data)  # Fill form with retrieved data
                self.show_form()  # Show the form once the data is retrieved
            else:
                QMessageBox.warning(self, "Geen Gegevens", "Geen gegevens gevonden voor deze attractie ID.")
                self.hide_form()  # Ensure the form is hidden if no data found
            db.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Fout bij het ophalen van gegevens: {e}")
            self.hide_form()  # Ensure the form is hidden on error


    def fill_form_with_data(self, data):
        # Fills editing gui with the existing data.
        self.naam_entry.setText(data[0])
        self.type_entry.setCurrentText(data[1])
        self.overdekt_entry.setCurrentText("Ja" if data[2] == 1 else "Nee")
        self.wachttijd_entry.setText(str(data[3]))
        self.doorlooptijd_entry.setText(str(data[4]))
        self.actief_entry.setCurrentText("Ja" if data[5] == 1 else "Nee")
        self.min_lengte_entry.setText(str(data[6]) if data[6] is not None else "")
        self.max_lengte_entry.setText(str(data[7]) if data[7] is not None else "")
        self.min_leeftijd_entry.setText(str(data[8]) if data[8] is not None else "")
        self.max_gewicht_entry.setText(str(data[9]) if data[9] is not None else "")
        self.product_entry.setText(data[10])


    def get_IOdata(self):
        # Retrieves data and returns it.
        return {
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
            "productaanbod": self.product_entry.text() or None,
            "id": self.id_input.text().strip()
        }

    def update_database(self):
        data = self.get_IOdata()  # Collect data from form
        try:
            # Connect the database.
            db = Database(host="localhost", gebruiker="user", wachtwoord="password", database="attractiepark_software")
            db.connect()

            # SQL query to update data in the table, place holders get filled in with data retrieved from the form.
            query = """
            UPDATE voorziening 
            SET 
                naam = %s, 
                type = %s, 
                overdekt = %s, 
                geschatte_wachttijd = %s, 
                doorlooptijd = %s, 
                actief = %s, 
                attractie_min_lengte = %s, 
                attractie_max_lengte = %s, 
                attractie_min_leeftijd = %s, 
                attractie_max_gewicht = %s, 
                productaanbod = %s 
            WHERE 
                id = %s
                    """
            # Params for the placeholders in the SQL query.
            params = (
                data["naam"],  # naam is a string
                data["type"],  # type is a string
                1 if data["overdekt"].lower() == "ja" else 0,  # overdekt is stored as 1 or 0 (tinyint)
                data["geschatte_wachttijd"],  # wachttijd should be an integer
                data["doorlooptijd"],  # doorlooptijd should be an integer
                1 if data["actief"].lower() == "ja" else 0,  # actief is stored as 1 or 0 (tinyint)
                data["attractie_min_lengte"],
                data["attractie_max_lengte"],
                data["attractie_min_leeftijd"],
                data["attractie_max_gewicht"],
                data["productaanbod"],
                data["id"],
            )

            # Debugging.
            print(f"Data to change: {data}")
            print("Verbonden met de database!")
            print("Query:", query)
            print("Params:", params)
            # Execute the query
            db.execute_query(query, params)

            QMessageBox.information(self, "Succes", "Attractie succesvol bijgewerkt.")
            db.close()

        except Exception as e:
            QMessageBox.information(self, "Error", f"Fout bij uitvoeren van query: {str(e)}")
            print("Fout bij uitvoeren van query:", e)
            db.close()

# Attraction deletion dialogue and logic
class AttractieVerwijderenDialoog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Attractie Verwijderen")

        # Layout
        self.layout = QVBoxLayout(self)

        # Attractie ID entry label
        self.id_label = QLabel("Attractie ID:")
        self.id_input = QLineEdit(self)
        self.layout.addWidget(self.id_label)
        self.layout.addWidget(self.id_input)

        # Verwijderen button
        self.verwijder_button = QPushButton("Verwijderen", self)
        self.verwijder_button.clicked.connect(self.verwijder_attractie)
        self.layout.addWidget(self.verwijder_button)

        # Annuleren button
        self.annuleren_button = QPushButton("Annuleren", self)
        self.annuleren_button.clicked.connect(self.reject)
        self.layout.addWidget(self.annuleren_button)

    def verwijder_attractie(self):
        attractie_id = self.id_input.text().strip()

        if not attractie_id.isdigit(): # Error catching for invalid ID.
            QMessageBox.warning(self, "Ongeldig ID", "Voer een geldig numeriek attractie ID in.")
            return

        try:
            # Connect to the database.
            db = Database(host="localhost", gebruiker="user", wachtwoord="password", database="attractiepark_software")
            db.connect()

            # Check if the attraction exists.
            select_query = "SELECT * FROM voorziening WHERE id = %s"
            result = db.execute_query(select_query, (attractie_id,))
            if not result:
                QMessageBox.warning(self, "Fout", "Geen attractie gevonden met dit ID.")
                db.close()
                return

            # Delete the attraction.
            delete_query = "DELETE FROM voorziening WHERE id = %s"
            db.execute_query(delete_query, (attractie_id,))

            QMessageBox.information(self, "Succes", "Attractie succesvol verwijderd.")
            db.close()


        except Exception as e: # Error catching.
            QMessageBox.critical(self, "Fout", f"Fout bij het verwijderen van de attractie: {e}")
            db.close()
