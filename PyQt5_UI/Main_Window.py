import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QCheckBox, QTextEdit, QPushButton
from PyQt5.QtGui import QValidator
from urllib.parse import urlparse

from PyQt5.QtGui import QRegExpValidator, QIntValidator
from PyQt5.QtCore import QRegExp



class App(QWidget):
    def __init__(self):
        super().__init__()

        # Window Configurations
        self.setWindowTitle("OLX Scrapper Command Generator")
        self.setGeometry(200, 200, 400, 400)

        layout = QVBoxLayout()

        # URL Input
        self.url_label = QLabel("URL")
        self.url_input = QLineEdit(self)

        regex = QRegExp("^(https?://)?[a-z0-9.-]+\.[a-z]{2,}(/.*)?$")
        self.url_validator = QRegExpValidator(regex)
        self.url_input.setValidator(self.url_validator)

        layout.addWidget(self.url_label)
        layout.addWidget(self.url_input)

        # Database Input
        self.database_label = QLabel("Database")
        self.database_input = QLineEdit(self)
        layout.addWidget(self.database_label)
        layout.addWidget(self.database_input)

        # Future placeholder
        self.placeholder_label = QLabel("Placeholder for Future Use")
        self.placeholder_input = QLineEdit(self)
        layout.addWidget(self.placeholder_label)
        layout.addWidget(self.placeholder_input)


        # Checkboxes
        self.attributes = ["Ads_id", "Title", "Price", "Location", "Area", "Price_per_meter2", "URL", "Validity"]
        self.checkboxes = {}
        self.text_fields = {}

        for attrib in self.attributes:
            checkbox = QCheckBox(attrib, self)
            checkbox.stateChanged.connect(self.Element_hiding_unhiding)
            layout.addWidget(checkbox)
            self.checkboxes[attrib] = checkbox

            # Create a corresponding text field
            Horizontal_Layout = QHBoxLayout()

            text_field = QLineEdit("Max",self)
            self.text_fields[f"{attrib}_MAX"] = text_field
            Horizontal_Layout.addWidget(text_field)
            text_field.setDisabled(True)

            text_field = QLineEdit("Min",self)
            self.text_fields[f"{attrib}_MIN"] = text_field
            Horizontal_Layout.addWidget(text_field)
            text_field.setDisabled(True)  # Initially disabled

            layout.addLayout(Horizontal_Layout)


        # Generate Button
        self.generate_button = QPushButton("Generate", self)
        self.generate_button.clicked.connect(self.generate_cmd)
        layout.addWidget(self.generate_button)

        # Text Area
        self.text_area = QTextEdit(self)
        layout.addWidget(self.text_area)

        # Setting layout
        self.setLayout(layout)

    #Accesing the elements
    def Element_hiding_unhiding(self):
        calling_checkbox =  self.sender()
        for keys, checkbox_object in self.checkboxes.items():
            if checkbox_object == calling_checkbox:
                self.text_fields[f"{keys}_MIN"].setDisabled(False)
                self.text_fields[f"{keys}_MAX"].setDisabled(False)
                self.text_fields[f"{keys}_MIN"].setText("")
                self.text_fields[f"{keys}_MAX"].setText("")

    def generate_cmd(self):
        url = self.url_input.text()
        db_url = f"{self.database_input.text()}"
        checked_attributes = ' '.join(
            [f'"{attrib}"' for attrib, checkbox in self.checkboxes.items() if checkbox.isChecked()])
        filter_values = ' '.join([f"{key} {Value.text()}" for key, Value in self.text_fields.items() if Value.isEnabled() == True and Value.text()])

        # Construct the command
        cmd = f'python Main_file.py --URL "{url}" --DB_url "{db_url}" --Element_to_extract {checked_attributes} --Limitation_Dict {filter_values}'

        # Display the generated command in the text area
        self.text_area.setText(cmd)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())
