from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QTableWidget, QTableWidgetItem, QWidget, QGridLayout, QDialog,
    QLineEdit
)

from database_wrapper import Database
from gui_wrapper import AttractieToevoegenDialoog, AttractieBewerkenDialoog, AttractieVerwijderenDialoog


class VoorzieningenWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Build main window
        self.setup_window()

        # Setup database
        self.setup_database()

        # Retrieve attractions and build table
        self.load_and_fill_table()

        # Add buttons for editing, addition, deletion
        self.add_buttons()

        # Setup search bar
        self.setup_search_bar()

    def setup_window(self):
        # Setup main window.
        self.setWindowTitle("Attractie beheer")
        self.setGeometry(100, 100, 1200, 800)

        # Main widget and layout.
        self.central_widget = QWidget(self)
        self.layout = QGridLayout(self.central_widget)
        self.setCentralWidget(self.central_widget)

    def setup_database(self):
        # Setup database connection.
        self.db = Database(host="localhost", gebruiker="user", wachtwoord="password", database="attractiepark_software")
        self.db.connect()

    def load_and_fill_table(self):
        #Load data from the database and populate the table.
        self.attracties = self.attracties_ophalen()

        # Define attributes for the table.
        self.attributen_attractie = [
            {"naam": "Naam", "type": "string", "verplicht": True},
            {"naam": "Type", "type": "options", "opties": ["Achtbaan", "Water", "Draaien", "Familie", "Simulator"],
             "verplicht": True},
            {"naam": "Overdekt", "type": "boolean", "verplicht": True},
            {"naam": "geschatteWachttijd", "type": "int", "verplicht": True},
            {"naam": "Doorlooptijd", "type": "int", "verplicht": True},
            {"naam": "Actief", "type": "boolean", "verplicht": True},
            {"naam": "minLengte", "type": "int"},
            {"naam": "maxLengte", "type": "int"},
            {"naam": "minLeeftijd", "type": "int"},
            {"naam": "maxGewicht", "type": "int"},
            {"naam": "Product", "type": "string", "verplicht": False},
        ]

        # Build table.
        self.setup_table()
        self.vul_tabel()

    def setup_table(self):
        #Create and set up the QTableWidget.
        self.attractie_tabel = QTableWidget(self)
        self.attractie_tabel.setColumnCount(len(self.attributen_attractie))
        self.attractie_tabel.setHorizontalHeaderLabels([attr["naam"] for attr in self.attributen_attractie])
        self.layout.addWidget(self.attractie_tabel, 1, 0, 1, 3)  # Adjust row placement

    def setup_search_bar(self):
        # Create and setup search bar.
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Zoek attracties (bijv. id:7)...")
        self.search_bar.returnPressed.connect(self.filter_table)  # Use returnPressed for search
        self.layout.addWidget(self.search_bar, 0, 0, 1, 3)  # Add search bar to layout

    def filter_table(self):
        #Filter table based on user input.
        search_text = self.search_bar.text().strip()

        # Default to all attractions if the input is empty.
        if not search_text:
            self.attracties = self.attracties_ophalen()
            self.vul_tabel()
            return

        # Use match-case to decide what the user is filtering.
        match search_text.split(":"):
            case ["id", id_value]:
                try:
                    id_value = int(id_value)
                    self.attracties = self.attracties_ophalen_by_filter("id", id_value)
                except ValueError:
                    print("Invalid ID format.")
                    self.attracties = self.attracties_ophalen()

            case ["naam", name]:
                self.attracties = self.attracties_ophalen_by_filter("naam", name.strip())

            case ["type", attraction_type]:
                self.attracties = self.attracties_ophalen_by_filter("type", attraction_type.strip())

            case ["overdekt", overdekt_value]:
                try:
                    overdekt_value = int(overdekt_value)
                    if overdekt_value in (0, 1):
                        self.attracties = self.attracties_ophalen_by_filter("overdekt", overdekt_value)
                    else:
                        print("Invalid value for overdekt. Must be 0 or 1.")
                        self.attracties = self.attracties_ophalen()
                except ValueError:
                    print("Invalid format for overdekt.")
                    self.attracties = self.attracties_ophalen()

            case ["wachttijd", wait_time_value]:
                try:
                    wait_time_value = int(wait_time_value)
                    self.attracties = self.attracties_ophalen_by_filter("wachttijd", wait_time_value,
                                                                        condition='<=')
                except ValueError:
                    print("Invalid format for geschatte wachttijd.")
                    self.attracties = self.attracties_ophalen()

            case ["doorlooptijd", duration_value]:
                try:
                    duration_value = int(duration_value)
                    self.attracties = self.attracties_ophalen_by_filter("doorlooptijd", duration_value, condition='<=')
                except ValueError:
                    print("Invalid format for doorlooptijd.")
                    self.attracties = self.attracties_ophalen()

            case ["actief", actief_value]:
                try:
                    actief_value = int(actief_value)
                    if actief_value in (0, 1):
                        self.attracties = self.attracties_ophalen_by_filter("actief", actief_value)
                    else:
                        print("Invalid value for actief. Must be 0 or 1.")
                        self.attracties = self.attracties_ophalen()
                except ValueError:
                    print("Invalid format for actief.")
                    self.attracties = self.attracties_ophalen()

            case ["minLengte", min_length_value]:
                if min_length_value.lower() == "none":
                    self.attracties = self.attracties_ophalen_by_filter("minLengte", None,
                                                                        condition='IS NULL')
                else:
                    try:
                        min_length_value = int(min_length_value)
                        self.attracties = self.attracties_ophalen_by_filter("minLengte", min_length_value,
                                                                            condition='>=')
                    except ValueError:
                        print("Invalid format for min lengte.")
                        self.attracties = self.attracties_ophalen()

            case ["maxLengte", max_length_value]:
                if max_length_value.lower() == "none":
                    self.attracties = self.attracties_ophalen_by_filter("maxLengte", None,
                                                                        condition='IS NULL')
                else:
                    try:
                        max_length_value = int(max_length_value)
                        self.attracties = self.attracties_ophalen_by_filter("maxLengte", max_length_value,
                                                                            condition='<=')
                    except ValueError:
                        print("Invalid format for max lengte.")
                        self.attracties = self.attracties_ophalen()

            case ["minLeeftijd", min_age_value]:
                if min_age_value.lower() == "none":
                    self.attracties = self.attracties_ophalen_by_filter("minLeeftijd", None,
                                                                        condition='IS NULL')
                else:
                    try:
                        min_age_value = int(min_age_value)
                        self.attracties = self.attracties_ophalen_by_filter("minLeeftijd", min_age_value,
                                                                            condition='>=')
                    except ValueError:
                        print("Invalid format for min leeftijd.")
                        self.attracties = self.attracties_ophalen()

            case ["maxGewicht", max_weight_value]:
                if max_weight_value.lower() == "none":
                    self.attracties = self.attracties_ophalen_by_filter("maxGewicht", None,
                                                                        condition='IS NULL')
                else:
                    try:
                        max_weight_value = int(max_weight_value)
                        self.attracties = self.attracties_ophalen_by_filter("maxGewicht", max_weight_value,
                                                                            condition='<=')
                    except ValueError:
                        print("Invalid format for max gewicht.")
                        self.attracties = self.attracties_ophalen()

            case ["product", product]:
                self.attracties = self.attracties_ophalen_by_filter("product", product.strip())
            # Add more cases for other filters as needed.

            case _:
                print("Unknown filter.")
                self.attracties = self.attracties_ophalen()

        self.vul_tabel()  # Update the table with the filtered data.

    def add_buttons(self):
        #Add buttons for adding, editing, and deleting rows.
        self.toevoegen_button = QPushButton("Toevoegen", self)
        self.toevoegen_button.clicked.connect(self.toevoegen_voorziening)
        self.layout.addWidget(self.toevoegen_button, 2, 0)

        self.verwijderen_button = QPushButton("Verwijderen", self)
        self.verwijderen_button.clicked.connect(self.verwijderen_voorziening)
        self.layout.addWidget(self.verwijderen_button, 2, 1)

        self.bewerken_button = QPushButton("Bewerken", self)
        self.bewerken_button.clicked.connect(self.bewerken_voorziening)
        self.layout.addWidget(self.bewerken_button, 2, 2)

    def attracties_ophalen(self):
        # Fetch all attraction data from the database.
        query = """
        SELECT naam, type, overdekt, geschatte_wachttijd, doorlooptijd, actief, 
               attractie_min_lengte, attractie_max_lengte, attractie_min_leeftijd, 
               attractie_max_gewicht, productaanbod 
        FROM voorziening
        """
        return self.db.execute_query(query)

    def attracties_ophalen_by_filter(self, column_name, value, condition='='):

        # Fetch attractions based on a specified column and value from the database.
        column_mapping = {
            "id": "id",
            "naam": "naam",
            "type": "type",
            "overdekt": "overdekt",
            "wachttijd": "geschatte_wachttijd",
            "doorlooptijd": "doorlooptijd",
            "actief": "actief",
            "minLengte": "attractie_min_lengte",
            "maxLengte": "attractie_max_lengte",
            "minLeeftijd": "attractie_min_leeftijd",
            "maxGewicht": "attractie_max_gewicht",
            "product": "productaanbod"
        }

        if column_name in column_mapping:
            if condition == 'IS NULL': # SQL query for NULL datatypes.
                query = f"""
                SELECT naam, type, overdekt, geschatte_wachttijd, doorlooptijd, actief, 
                       attractie_min_lengte, attractie_max_lengte, attractie_min_leeftijd, 
                       attractie_max_gewicht, productaanbod 
                FROM voorziening WHERE {column_mapping[column_name]} IS NULL
                """
                return self.db.execute_query(query)
            else:
                query = f"""
                SELECT naam, type, overdekt, geschatte_wachttijd, doorlooptijd, actief, 
                       attractie_min_lengte, attractie_max_lengte, attractie_min_leeftijd, 
                       attractie_max_gewicht, productaanbod 
                FROM voorziening WHERE {column_mapping[column_name]} {condition} %s
                """
                return self.db.execute_query(query, (value,))
        else:
            print("Invalid column name.")
            return []  # Return an empty list for invalid column names.

    def vul_tabel(self):
        # Fill the table with data.
        self.attractie_tabel.setRowCount(len(self.attracties))
        for rij, attractie in enumerate(self.attracties):
            for kolom, waarde in enumerate(attractie):
                self.attractie_tabel.setItem(rij, kolom, QTableWidgetItem(str(waarde)))

    def refresh_data(self):
        self.setup_window() # Builds main window.
        self.setup_database() # Connects database.
        self.load_and_fill_table() # Loads attributes table and fills the table
        self.add_buttons() # Adds buttons for deletion, editing, addition
        self.setup_search_bar() # Adds search bar

    def toevoegen_voorziening(self):
        # Handle adding a new attraction.
        dialog = AttractieToevoegenDialoog(self) # Connects to class in the gui wrapper for adding new attractions.
        if dialog.exec_() == QDialog.Accepted:
            dialog.add_into_database()# Execute main function in class
        self.refresh_data() # Refreshes the window to show changes.

    def bewerken_voorziening(self):
        # Handle editing an attraction.
        dialog = AttractieBewerkenDialoog(self) # Connects to class in the gui wrapper for editing attractions.
        if dialog.exec_() == QDialog.Accepted:
            print("Bewerkte attractie: ", dialog.get_IOdata())# Execute main function in class
        self.refresh_data() # Refreshes the table to show changes.

    def verwijderen_voorziening(self):
        # Handle deleting an attraction.
        dialog = AttractieVerwijderenDialoog(self) # Connects to class in the gui wrapper for deleting attractions.
        dialog.exec_()  # Execute main function in class type shit. (im getting tired of adding documentation)
        self.refresh_data() # Refreshes table to show changes.


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = VoorzieningenWindow()
    window.show()
    sys.exit(app.exec_())
