from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QHBoxLayout, QComboBox

class StudentDialog(QDialog):
    def __init__(self, parent=None, student=None, college_codes=None):
        super().__init__(parent)
        self.setWindowTitle("Add/Edit Student")
        self.layout = QVBoxLayout(self)

        self.form_layout = QFormLayout()
        self.id_number = QLineEdit(self)
        self.last_name = QLineEdit(self)
        self.first_name = QLineEdit(self)
        self.middle_name = QLineEdit(self)
        self.gender = QComboBox(self)
        self.gender.addItems(["Male", "Female", "Other"])
        self.year_level = QComboBox(self)
        self.year_level.addItems(["1", "2", "3", "4", "5"])
        self.program_code = QComboBox(self)
        self.program_code.addItems(["CS", "IT", "SE", "CE"])
        self.college_code = QComboBox(self)
        if college_codes:
            self.college_code.addItems(college_codes)

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
            self.gender.setCurrentText(student["Gender"])
            self.year_level.setCurrentText(student["Year Level"])
            self.program_code.setCurrentText(student["Program Code"])
            self.college_code.setCurrentText(student["College Code"])

    def get_student_data(self):
        return {
            "id_number": self.id_number.text(),
            "last_name": self.last_name.text(),
            "first_name": self.first_name.text(),
            "middle_name": self.middle_name.text(),
            "gender": self.gender.currentText(),
            "year_level": self.year_level.currentText(),
            "program_code": self.program_code.currentText(),
            "college_code": self.college_code.currentText()
        }