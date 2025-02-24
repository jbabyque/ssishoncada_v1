from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QHBoxLayout

class ProgramDialog(QDialog):
    def __init__(self, parent=None, program=None):
        super().__init__(parent)
        self.setWindowTitle("Add/Edit Program")
        self.layout = QVBoxLayout(self)

        self.form_layout = QFormLayout()
        self.program_code = QLineEdit(self)
        self.college_school = QLineEdit(self)
        self.program_name = QLineEdit(self)
        self.level = QLineEdit(self)

        self.form_layout.addRow("Program Code:", self.program_code)
        self.form_layout.addRow("College/School:", self.college_school)
        self.form_layout.addRow("Program Name:", self.program_name)
        self.form_layout.addRow("Level:", self.level)

        self.layout.addLayout(self.form_layout)

        self.button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save", self)
        self.cancel_button = QPushButton("Cancel", self)
        self.button_layout.addWidget(self.save_button)
        self.button_layout.addWidget(self.cancel_button)

        self.layout.addLayout(self.button_layout)

        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        if program:
            self.program_code.setText(program["program_code"])
            self.college_school.setText(program["college_school"])
            self.program_name.setText(program["program_name"])
            self.level.setText(program["level"])

    def get_program_data(self):
        return {
            "program_code": self.program_code.text(),
            "college_school": self.college_school.text(),
            "program_name": self.program_name.text(),
            "level": self.level.text()
        }