import sys
import logging
import csv
from PyQt6.QtWidgets import QMainWindow, QApplication, QLabel, QListWidgetItem, QWidget, QGridLayout, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QMessageBox, QLineEdit, QComboBox, QHeaderView
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap, QFont

from ssishoncada_ui import Ui_MainWindow
from studentDialog import StudentDialog
from programDialog import ProgramDialog
from collegeDialog import CollegeDialog

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

STUDENT_FIELD_MAP = {
    "ID Number": "id_number",
    "Last Name": "last_name",
    "First Name": "first_name",
    "Middle Name": "middle_name",
    "Gender": "gender",
    "Year Level": "year_level",
    "Program Code": "program_code",
    "College Code": "college_code"
}

PROGRAM_FIELD_MAP = {
    "Program Code": "program_code",
    "College School": "college_school",
    "Program Name": "program_name",
    "Level": "level"
}

COLLEGE_FIELD_MAP = {
    "College Code": "college_code",
    "College Name": "college_name"
}

class MainWindow(QMainWindow):
    STUDENT_CSV = 'students.csv'
    PROGRAM_CSV = 'programs.csv'
    COLLEGE_CSV = 'colleges.csv'

    STUDENT_HEADERS = ["ID Number", "Last Name", "First Name", "Middle Name", "Gender", "Year Level", "Program Code", "College Code"]
    PROGRAM_HEADERS = ["Program Code", "College School", "Program Name", "Level"]
    COLLEGE_HEADERS = ["College Code", "College Name"]

    def __init__(self):
        super().__init__()

        try:
            self.ui = Ui_MainWindow()
            self.ui.setupUi(self)
            
            self.titleLabel = self.ui.titleLabel 
            self.titleLabel.setText("S.S.I.S")
            
            self.titleIcon = self.ui.titleIcon
            self.titleIcon.hide()
            
            self.side_menu = self.ui.listWidget
            self.side_menu.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            self.side_menu_iconOnly = self.ui.iconOnly
            self.side_menu_iconOnly.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            
            self.menu_button = self.ui.pushButton
            self.menu_button.setObjectName("")
            
            self.menu_button.setText("")
            self.menu_button.setIcon(QIcon("menu.svg"))
            self.menu_button.setIconSize(QSize(20,20))
            self.menu_button.setCheckable(True)
            self.menu_button.setChecked(False)
            self.main_content = self.ui.stackedWidget
            
            self.menu_list = [
                {
                    "name": "Student",
                    "icon": "./icons/user.svg"
                },
                {
                    "name": "Program",
                    "icon": "./icons/database.svg"
                },
                {
                    "name": "College",
                    "icon": "./icons/home.svg"
                },
            ]

            self.__init_signal_slot()
            self.init_list_widget()
            self.init_stackwidget()
            self.load_data_from_csv(self.STUDENT_CSV, self.student_table, self.STUDENT_HEADERS, STUDENT_FIELD_MAP)
            self.load_data_from_csv(self.PROGRAM_CSV, self.program_table, self.PROGRAM_HEADERS, PROGRAM_FIELD_MAP)
            self.load_data_from_csv(self.COLLEGE_CSV, self.college_table, self.COLLEGE_HEADERS, COLLEGE_FIELD_MAP)
        except Exception as e:
            logging.error("Error initializing MainWindow: %s", e)
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")
            self.close()

    def __init_signal_slot(self):
        self.menu_button.toggled["bool"].connect(self.side_menu.setHidden)
        self.menu_button.toggled["bool"].connect(self.titleLabel.setHidden)
        self.menu_button.toggled["bool"].connect(self.side_menu.setHidden)
        self.menu_button.toggled["bool"].connect(self.side_menu_iconOnly.setVisible)
        
        self.side_menu.currentRowChanged['int'].connect(self.main_content.setCurrentIndex)
        self.side_menu_iconOnly.currentRowChanged['int'].connect(self.main_content.setCurrentIndex)
        self.side_menu.currentRowChanged['int'].connect(self.side_menu_iconOnly.setCurrentRow)
        self.side_menu_iconOnly.currentRowChanged['int'].connect(self.side_menu.setCurrentRow)
        self.menu_button.toggled.connect(self.button_icon_change)

    def init_list_widget(self):
        self.side_menu_iconOnly.clear()
        self.side_menu.clear()

        for menu in self.menu_list:
            item = QListWidgetItem()
            item.setIcon(QIcon(menu.get("icon")))
            item.setSizeHint(QSize(40, 40))
            self.side_menu_iconOnly.addItem(item)
            self.side_menu_iconOnly.setCurrentRow(0)

            item_new = QListWidgetItem()
            item_new.setIcon(QIcon(menu.get("icon")))
            item_new.setText(menu.get("name"))
            self.side_menu.addItem(item_new)
            self.side_menu.setCurrentRow(0)

    def init_stackwidget(self):
        widget_list = self.main_content.findChildren(QWidget)
        for widget in widget_list:
            self.main_content.removeWidget(widget)

        for menu in self.menu_list:
            text = menu.get("name")

            if text == "Student":
                new_page = self.create_student_page()
            elif text == "Program":
                new_page = self.create_program_page()
            elif text == "College":
                new_page = self.create_college_page()
            else:
                layout = QGridLayout()
                label = QLabel(text)
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                font = QFont()
                font.setPixelSize(20)
                label.setFont(font)
                layout.addWidget(label)
                new_page = QWidget()
                new_page.setLayout(layout)

            self.main_content.addWidget(new_page)

    def create_student_page(self):
        layout = QVBoxLayout()
        
        label = QLabel("Student Information")
        font = QFont("Century Gothic")
        font.setBold(True)
        font.setPixelSize(18)
        label.setFont(font)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        search_sort_layout = QHBoxLayout()
        
        search_label = QLabel("Search by:")
        self.student_search_combo = QComboBox()
        self.student_search_combo.addItems(self.STUDENT_HEADERS)
        self.student_search_input = QLineEdit()
        self.student_search_input.setPlaceholderText("Enter search term")
        self.student_search_input.textChanged.connect(self.search_student)
        search_sort_layout.addWidget(search_label)
        search_sort_layout.addWidget(self.student_search_combo)
        search_sort_layout.addWidget(self.student_search_input)

        sort_label = QLabel("Sort by:")
        self.student_sort_combo = QComboBox()
        self.student_sort_combo.addItems(self.STUDENT_HEADERS)
        self.student_sort_combo.currentIndexChanged.connect(self.sort_student)
        search_sort_layout.addWidget(sort_label)
        search_sort_layout.addWidget(self.student_sort_combo)

        layout.addLayout(search_sort_layout)

        self.student_table = QTableWidget()
        self.student_table.setColumnCount(8)
        self.student_table.setHorizontalHeaderLabels(self.STUDENT_HEADERS)
        self.student_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.student_table)

        button_layout = QHBoxLayout()
        add_button = QPushButton("Add")
        add_button.setFixedSize(100, 30)
        add_button.clicked.connect(self.add_student)
        edit_button = QPushButton("Edit")
        edit_button.setFixedSize(100, 30)
        edit_button.clicked.connect(self.edit_student)
        delete_button = QPushButton("Delete")
        delete_button.setFixedSize(100, 30)
        delete_button.clicked.connect(self.delete_student)
        button_layout.addWidget(add_button)
        button_layout.addWidget(edit_button)
        button_layout.addWidget(delete_button)
        layout.addLayout(button_layout)

        page = QWidget()
        page.setLayout(layout)

        return page

    def create_program_page(self):
        layout = QVBoxLayout()
        
        label = QLabel("Program Information")
        font = QFont("Century Gothic")
        font.setBold(True)
        font.setPixelSize(18)
        label.setFont(font)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        search_sort_layout = QHBoxLayout()
        
        search_label = QLabel("Search by:")
        self.program_search_combo = QComboBox()
        self.program_search_combo.addItems(self.PROGRAM_HEADERS)
        self.program_search_input = QLineEdit()
        self.program_search_input.setPlaceholderText("Enter search term")
        self.program_search_input.textChanged.connect(self.search_program)
        search_sort_layout.addWidget(search_label)
        search_sort_layout.addWidget(self.program_search_combo)
        search_sort_layout.addWidget(self.program_search_input)

        sort_label = QLabel("Sort by:")
        self.program_sort_combo = QComboBox()
        self.program_sort_combo.addItems(self.PROGRAM_HEADERS)
        self.program_sort_combo.currentIndexChanged.connect(self.sort_program)
        search_sort_layout.addWidget(sort_label)
        search_sort_layout.addWidget(self.program_sort_combo)

        layout.addLayout(search_sort_layout)

        self.program_table = QTableWidget()
        self.program_table.setColumnCount(4)
        self.program_table.setHorizontalHeaderLabels(self.PROGRAM_HEADERS)
        self.program_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.program_table)

        program_name_col_index = self.PROGRAM_HEADERS.index("Program Name")
        self.program_table.setColumnWidth(program_name_col_index, 250)

        button_layout = QHBoxLayout()
        add_button = QPushButton("Add")
        add_button.setFixedSize(100, 30)
        add_button.clicked.connect(self.add_program)
        edit_button = QPushButton("Edit")
        edit_button.setFixedSize(100, 30)
        edit_button.clicked.connect(self.edit_program)
        delete_button = QPushButton("Delete")
        delete_button.setFixedSize(100, 30)
        delete_button.clicked.connect(self.delete_program)
        button_layout.addWidget(add_button)
        button_layout.addWidget(edit_button)
        button_layout.addWidget(delete_button)
        layout.addLayout(button_layout)

        page = QWidget()
        page.setLayout(layout)

        return page

    def create_college_page(self):
        layout = QVBoxLayout()
        
        label = QLabel("College Information")
        font = QFont("Century Gothic")
        font.setBold(True)
        font.setPixelSize(18)
        label.setFont(font)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        search_sort_layout = QHBoxLayout()
        
        search_label = QLabel("Search by:")
        self.college_search_combo = QComboBox()
        self.college_search_combo.addItems(self.COLLEGE_HEADERS)
        self.college_search_input = QLineEdit()
        self.college_search_input.setPlaceholderText("Enter search term")
        self.college_search_input.textChanged.connect(self.search_college)
        search_sort_layout.addWidget(search_label)
        search_sort_layout.addWidget(self.college_search_combo)
        search_sort_layout.addWidget(self.college_search_input)

        sort_label = QLabel("Sort by:")
        self.college_sort_combo = QComboBox()
        self.college_sort_combo.addItems(self.COLLEGE_HEADERS)
        self.college_sort_combo.currentIndexChanged.connect(self.sort_college)
        search_sort_layout.addWidget(sort_label)
        search_sort_layout.addWidget(self.college_sort_combo)

        layout.addLayout(search_sort_layout)

        self.college_table = QTableWidget()
        self.college_table.setColumnCount(2)
        self.college_table.setHorizontalHeaderLabels(self.COLLEGE_HEADERS)
        self.college_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.college_table)
        
        college_name_col_index = self.COLLEGE_HEADERS.index("College Name")
        self.college_table.setColumnWidth(college_name_col_index, 250)

        button_layout = QHBoxLayout()
        add_button = QPushButton("Add")
        add_button.setFixedSize(100, 30)
        add_button.clicked.connect(self.add_college)
        edit_button = QPushButton("Edit")
        edit_button.setFixedSize(100, 30)
        edit_button.clicked.connect(self.edit_college)
        delete_button = QPushButton("Delete")
        delete_button.setFixedSize(100, 30)
        delete_button.clicked.connect(self.delete_college)
        button_layout.addWidget(add_button)
        button_layout.addWidget(edit_button)
        button_layout.addWidget(delete_button)
        layout.addLayout(button_layout)

        page = QWidget()
        page.setLayout(layout)

        return page

    def add_student(self):
        dialog = StudentDialog(self)
        if dialog.exec() == StudentDialog.DialogCode.Accepted:
            student_data = dialog.get_student_data()
            row_position = self.student_table.rowCount()
            self.student_table.insertRow(row_position)
            for col, header in enumerate(self.STUDENT_HEADERS):
                field = STUDENT_FIELD_MAP[header]
                self.student_table.setItem(row_position, col, QTableWidgetItem(student_data[field]))
            self.save_data_to_csv(self.STUDENT_CSV, self.student_table, self.STUDENT_HEADERS, STUDENT_FIELD_MAP)

    def edit_student(self):
        selected_row = self.student_table.currentRow()
        if selected_row >= 0:
            student_data = {header: self.student_table.item(selected_row, col).text() for col, header in enumerate(self.STUDENT_HEADERS)}
            dialog = StudentDialog(self, student_data)
            if dialog.exec() == StudentDialog.DialogCode.Accepted:
                student_data = dialog.get_student_data()
                for col, header in enumerate(self.STUDENT_HEADERS):
                    field = STUDENT_FIELD_MAP[header]
                    self.student_table.setItem(selected_row, col, QTableWidgetItem(student_data[field]))
                self.save_data_to_csv(self.STUDENT_CSV, self.student_table, self.STUDENT_HEADERS, STUDENT_FIELD_MAP)

    def delete_student(self):
        selected_row = self.student_table.currentRow()
        if selected_row >= 0:
            self.student_table.removeRow(selected_row)
            self.save_data_to_csv(self.STUDENT_CSV, self.student_table, self.STUDENT_HEADERS, STUDENT_FIELD_MAP)

    def add_program(self):
        dialog = ProgramDialog(self)
        if dialog.exec() == ProgramDialog.DialogCode.Accepted:
            program_data = dialog.get_program_data()
            row_position = self.program_table.rowCount()
            self.program_table.insertRow(row_position)
            for col, header in enumerate(self.PROGRAM_HEADERS):
                field = PROGRAM_FIELD_MAP[header]
                self.program_table.setItem(row_position, col, QTableWidgetItem(program_data[field]))
            self.save_data_to_csv(self.PROGRAM_CSV, self.program_table, self.PROGRAM_HEADERS, PROGRAM_FIELD_MAP)

    def edit_program(self):
        selected_row = self.program_table.currentRow()
        if selected_row >= 0:
            program_data = {header: self.program_table.item(selected_row, col).text() for col, header in enumerate(self.PROGRAM_HEADERS)}
            dialog = ProgramDialog(self, program_data)
            if dialog.exec() == ProgramDialog.DialogCode.Accepted:
                program_data = dialog.get_program_data()
                for col, header in enumerate(self.PROGRAM_HEADERS):
                    field = PROGRAM_FIELD_MAP[header]
                    self.program_table.setItem(selected_row, col, QTableWidgetItem(program_data[field]))
                self.save_data_to_csv(self.PROGRAM_CSV, self.program_table, self.PROGRAM_HEADERS, PROGRAM_FIELD_MAP)

    def delete_program(self):
        selected_row = self.program_table.currentRow()
        if selected_row >= 0:
            self.program_table.removeRow(selected_row)
            self.save_data_to_csv(self.PROGRAM_CSV, self.program_table, self.PROGRAM_HEADERS, PROGRAM_FIELD_MAP)

    def add_college(self):
        dialog = CollegeDialog(self)
        if dialog.exec() == CollegeDialog.DialogCode.Accepted:
            college_data = dialog.get_college_data()
            row_position = self.college_table.rowCount()
            self.college_table.insertRow(row_position)
            for col, header in enumerate(self.COLLEGE_HEADERS):
                field = COLLEGE_FIELD_MAP[header]
                self.college_table.setItem(row_position, col, QTableWidgetItem(college_data[field]))
            self.save_data_to_csv(self.COLLEGE_CSV, self.college_table, self.COLLEGE_HEADERS, COLLEGE_FIELD_MAP)

    def edit_college(self):
        selected_row = self.college_table.currentRow()
        if selected_row >= 0:
            college_data = {header: self.college_table.item(selected_row, col).text() for col, header in enumerate(self.COLLEGE_HEADERS)}
            dialog = CollegeDialog(self, college_data)
            if dialog.exec() == CollegeDialog.DialogCode.Accepted:
                college_data = dialog.get_college_data()
                for col, header in enumerate(self.COLLEGE_HEADERS):
                    field = COLLEGE_FIELD_MAP[header]
                    self.college_table.setItem(selected_row, col, QTableWidgetItem(college_data[field]))
                self.save_data_to_csv(self.COLLEGE_CSV, self.college_table, self.COLLEGE_HEADERS, COLLEGE_FIELD_MAP)

    def delete_college(self):
        selected_row = self.college_table.currentRow()
        if selected_row >= 0:
            self.college_table.removeRow(selected_row)
            self.save_data_to_csv(self.COLLEGE_CSV, self.college_table, self.COLLEGE_HEADERS, COLLEGE_FIELD_MAP)

    def button_icon_change(self, status):
        if status:
            self.menu_button.setIcon(QIcon("./icon/open.svg"))
        else:
            self.menu_button.setIcon(QIcon("./icon/close.svg"))

    def load_data_from_csv(self, file_path, table_widget, headers, field_map):
        try:
            with open(file_path, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                table_widget.setRowCount(0)
                for row in reader:
                    row_position = table_widget.rowCount()
                    table_widget.insertRow(row_position)
                    for col, header in enumerate(headers):
                        field = field_map[header]
                        table_widget.setItem(row_position, col, QTableWidgetItem(row[field]))
        except FileNotFoundError:
            pass  # File not found, no data to load

    def save_data_to_csv(self, file_path, table_widget, headers, field_map):
        with open(file_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=field_map.values())
            writer.writeheader()
            for row in range(table_widget.rowCount()):
                row_data = {field_map[header]: table_widget.item(row, col).text() for col, header in enumerate(headers)}
                writer.writerow(row_data)
                
    def search_student(self):
        search_term = self.student_search_input.text().lower()
        search_column = self.student_search_combo.currentIndex()
        for row in range(self.student_table.rowCount()):
            item = self.student_table.item(row, search_column)
            match = search_term in item.text().lower()
            self.student_table.setRowHidden(row, not match)

    def sort_student(self):
        column = self.student_sort_combo.currentIndex()
        self.student_table.sortItems(column)

    def search_program(self):
        search_term = self.program_search_input.text().lower()
        search_column = self.program_search_combo.currentIndex()
        for row in range(self.program_table.rowCount()):
            item = self.program_table.item(row, search_column)
            match = search_term in item.text().lower()
            self.program_table.setRowHidden(row, not match)

    def sort_program(self):
        column = self.program_sort_combo.currentIndex()
        self.program_table.sortItems(column)

    def search_college(self):
        search_term = self.college_search_input.text().lower()
        for row in range(self.college_table.rowCount()):
            match = False
            for col in range(self.college_table.columnCount()):
                item = self.college_table.item(row, col)
                if search_term in item.text().lower():
                    match = True
                    break
            self.college_table.setRowHidden(row, not match)

    def sort_college(self):
        column = self.college_sort_combo.currentIndex()
        self.college_table.sortItems(column)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    try:
        with open("style.qss") as f:
            style_str = f.read()
        app.setStyleSheet(style_str)
    except Exception as e:
        logging.error("Error loading stylesheet: %s", e)
        QMessageBox.critical(None, "Error", f"An error occurred loading the stylesheet: {e}")

    try:
        window = MainWindow()
        window.show()
    except Exception as e:
        logging.error("Error showing MainWindow: %s", e)
        QMessageBox.critical(None, "Error", f"An error occurred: {e}")

    sys.exit(app.exec())

