from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFormLayout, QHBoxLayout

class CollegeDialog(QDialog):
    def __init__(self, parent=None, college=None):
        super().__init__(parent)
        self.setWindowTitle("Add/Edit College")
        self.layout = QVBoxLayout(self)

        self.form_layout = QFormLayout()
        self.college_code = QLineEdit(self)
        self.college_name = QLineEdit(self)

        self.form_layout.addRow("College Code:", self.college_code)
        self.form_layout.addRow("College Name:", self.college_name)

        self.layout.addLayout(self.form_layout)

        self.button_layout = QHBoxLayout()
        self.save_button = QPushButton("Save", self)
        self.cancel_button = QPushButton("Cancel", self)
        self.button_layout.addWidget(self.save_button)
        self.button_layout.addWidget(self.cancel_button)

        self.layout.addLayout(self.button_layout)

        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        if college:
            self.college_code.setText(college["college_code"])
            self.college_name.setText(college["college_name"])

    def get_college_data(self):
        return {
            "college_code": self.college_code.text(),
            "college_name": self.college_name.text()
        }