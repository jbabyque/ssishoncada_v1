from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QHBoxLayout, QComboBox, QMessageBox, QTableWidgetItem
import logging

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
        self.program_code = QLineEdit(self)
        self.college_code = QLineEdit(self)
        self.form_layout.addRow("College Code:", self.college_code)

        self.form_layout.addRow("ID Number:", self.id_number)
        self.form_layout.addRow("Last Name:", self.last_name)
        self.form_layout.addRow("First Name:", self.first_name)
        self.form_layout.addRow("Middle Name:", self.middle_name)
        self.form_layout.addRow("Gender:", self.gender)
        self.form_layout.addRow("Year Level:", self.year_level)
        self.form_layout.addRow("Program Code:", self.program_code)

        self.layout.addLayout(self.form_layout)

        self.button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save", self)
        self.cancel_button = QPushButton("Cancel", self)
        self.button_layout.addWidget(self.save_button)
        self.button_layout.addWidget(self.cancel_button)

        self.layout.addLayout(self.button_layout)

        self.save_button.clicked.connect(self.on_save)
        self.cancel_button.clicked.connect(self.reject)

        if student:
            self.id_number.setText(student.get("id_number", ""))
            self.last_name.setText(student.get("last_name", ""))
            self.first_name.setText(student.get("first_name", ""))
            self.middle_name.setText(student.get("middle_name", ""))
            self.gender.setCurrentText(student.get("gender", "Male"))
            self.year_level.setCurrentText(student.get("year_level", "1"))
            self.program_code.setText(student.get("program_code", ""))
            self.college_code.setText(student.get("college_code", ""))

    def get_student_data(self):
        return {
            "id_number": self.id_number.text(),
            "last_name": self.last_name.text(),
            "first_name": self.first_name.text(),
            "middle_name": self.middle_name.text(),
            "gender": self.gender.currentText(),
            "year_level": self.year_level.currentText(),
            "program_code": self.program_code.text(),
            "college_code": self.college_code.text()
        }

    def on_save(self):
        if not self.id_number.text() or not self.last_name.text() or not self.first_name.text():
            QMessageBox.warning(self, "Invalid Data", "Please fill out all required fields.")
            return
        self.accept()

    def add_student(self):
        dialog = StudentDialog(self)
        if dialog.exec() == StudentDialog.DialogCode.Accepted:
            student_data = dialog.get_student_data()
            row_position = self.student_table.rowCount()
            self.student_table.insertRow(row_position)
            for col, header in enumerate(self.STUDENT_HEADERS):
                field = STUDENT_FIELD_MAP[header]
                self.student_table.setItem(row_position, col, QTableWidgetItem(student_data[field]))
            logging.info("Adding student data")
            self.save_data_to_csv(self.STUDENT_CSV, self.student_table, self.STUDENT_HEADERS, STUDENT_FIELD_MAP)