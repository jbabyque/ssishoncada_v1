from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QHBoxLayout

class StudentDialog(QDialog):
    def __init__(self, parent=None, student=None):
        super().__init__(parent)
        self.setWindowTitle("Add/Edit Student")
        self.layout = QVBoxLayout(self)

        self.form_layout = QFormLayout()
        self.id_number = QLineEdit(self)
        self.last_name = QLineEdit(self)
        self.first_name = QLineEdit(self)
        self.middle_name = QLineEdit(self)
        self.gender = QLineEdit(self)
        self.year_level = QLineEdit(self)
        self.program_code = QLineEdit(self)
        self.college_code = QLineEdit(self)

        self.form_layout.addRow("ID Number:", self.id_number)
        self.form_layout.addRow("Last Name:", self.last_name)
        self.form_layout.addRow("First Name:", self.first_name)
        self.form_layout.addRow("Middle Name:", self.middle_name)
        self.form_layout.addRow("Gender:", self.gender)
        self.form_layout.addRow("Year Level:", self.year_level)
        self.form_layout.addRow("Program Code:", self.program_code)
        self.form_layout.addRow("College Code:", self.college_code)

        self.layout.addLayout(self.form_layout)

        self.button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save", self)
        self.cancel_button = QPushButton("Cancel", self)
        self.button_layout.addWidget(self.save_button)
        self.button_layout.addWidget(self.cancel_button)

        self.layout.addLayout(self.button_layout)

        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        if student:
            self.id_number.setText(student["ID Number"])
            self.last_name.setText(student["Last Name"])
            self.first_name.setText(student["First Name"])
            self.middle_name.setText(student["Middle Name"])
            self.gender.setText(student["Gender"])
            self.year_level.setText(student["Year Level"])
            self.program_code.setText(student["Program Code"])
            self.college_code.setText(student["College Code"])

    def get_student_data(self):
        return {
            "ID Number": self.id_number.text(),
            "Last Name": self.last_name.text(),
            "First Name": self.first_name.text(),
            "Middle Name": self.middle_name.text(),
            "Gender": self.gender.text(),
            "Year Level": self.year_level.text(),
            "Program Code": self.program_code.text(),
            "College Code": self.college_code.text()
        }