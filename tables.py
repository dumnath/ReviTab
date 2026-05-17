from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QLineEdit, QInputDialog, QMessageBox, QDialog
from PySide6.QtGui import QFont, QColor
from PySide6.QtCore import Qt
from dialogs import ExerciseCreationSettings, ScoreWindow
from utils import normalize_text
import random as rd

class BaseTable(QTableWidget) :
    def __init__(self, parent, filepath) :
        super().__init__(parent)
        self.parent = parent
        self.filepath = filepath
        self.texts = parent.texts
        self.separator = self.parent.separator

        self.elements_list = []
        self.header_list = []
        
    def load_file(self) :
        self.elements_list.clear()
        self.header_list.clear()
        self.separator = self.parent.separator
        with open(self.filepath, encoding = 'utf-8') as csvfile :
            line = csvfile.readline()
            row = line.split(self.separator)
            self.header_list = [row[i].strip('\n') for i in range(len(row))]
            for line in csvfile.readlines():
                row = line.split(self.separator)
                if len(row) >= 1 :
                    self.elements_list.append({self.header_list[i] : row[i].strip('\n') for i in range(len(row))})

    def configure_table(self) :
        if self.parent.alternating_row_colors == True :
            self.setAlternatingRowColors(True)
        self.setColumnCount(len(self.header_list))
        for i in range(self.columnCount()) :
            self.setColumnWidth(i, int((self.parent.width()-50)/self.columnCount()))
        self.setHorizontalHeaderLabels(self.header_list)
        self.setRowCount(len(self.elements_list))

    def populate_table(self) :
        for row, e in enumerate(self.elements_list) :
            for f in range(len(self.header_list)) :
                self.setItem(row, f, QTableWidgetItem(e[self.header_list[f]]))


class EditTable(BaseTable) :
    def __init__(self, parent, filepath) :
        super().__init__(parent, filepath)
        self.modified = False

        if filepath == 'Untitled.csv' :
            self.setColumnCount(2)
            self.setRowCount(3)
            self.setHorizontalHeaderLabels(['Column 1', 'Column 2'])
            self.header_list = ['Column 1', 'Column 2']
            if self.parent.alternating_row_colors == True :
                self.setAlternatingRowColors(True)
        else :
            self.load_file()
            self.configure_table()
            self.populate_table()

        self.itemChanged.connect(self.mark_modified)

    def mark_modified(self) :
        self.modified = True

    def insert_eszett(self) :
        editor = self.focusWidget()
        if editor and isinstance(editor, QLineEdit) :
            editor.insert("ß")

    def extract_data(self) :
        content = ""
        content += self.separator.join(self.header_list) +'\n'

        for row in range(self.rowCount()) :
            row_data = []
            for col in range(self.columnCount()) :
                item = self.item(row, col)
                if item != None :
                    row_data.append(item.text() if item else "")
            content += self.separator.join(row_data) +'\n'

        self.modified = False
        return content

    def add_row(self) :
        self.insertRow(self.rowCount())

    def add_column(self) :
        header, ok = QInputDialog.getText(self, self.texts['add_column'], self.texts['header'])
        if header and ok :
            self.insertColumn(self.columnCount())
            self.setHorizontalHeaderItem(self.columnCount()-1, QTableWidgetItem(header))
            self.header_list.append(header)

    def rename_column(self) :
        new_header, ok = QInputDialog.getText(self, self.texts['rename_column'], self.texts['new_header'])
        if new_header and ok :
            self.setHorizontalHeaderItem(self.currentColumn(), QTableWidgetItem(new_header))
            self.header_list[self.currentColumn()] = new_header

    def delete_row(self) :
        if self.confirmation('row', self.currentRow()) :
            self.removeRow(self.currentRow())

    def delete_column(self) :
        if self.confirmation('column', self.currentColumn()) :
            col = self.currentColumn()
            self.removeColumn(col)
            self.header_list.pop(col)

    def confirmation(self, item, item_number) :
        question = QMessageBox.question(self, self.texts['confirm_title'], f"{self.texts['delete_confirmation']} {item} {item_number+1} ?")

        if question == QMessageBox.StandardButton.Yes :
            return True
        

class PracticeTable(BaseTable) :
    def __init__(self, parent, filepath) :
        super().__init__(parent, filepath)
        self.failed = False

        try :
            self.load_file()
        except FileNotFoundError :
            QMessageBox.critical(self, self.texts['error'], self.texts['file_not_found'])
            self.failed = True
            return

        exercise_settings = ExerciseCreationSettings(self)
        result = exercise_settings.exec()
        if result != QDialog.DialogCode.Accepted :
            self.failed = True
            return

        self.configure_table()
        self.load_table()

    def load_table(self) :
        self.clearContents()
        rd.shuffle(self.elements_list)
        self.populate_table()

        for row in range(self.rowCount()) :
            self.column_shown = self.parent.column_shown
            if self.column_shown == "first" :
                col_kept = 0
            elif self.column_shown == "random" :
                col_kept = row % self.columnCount()
            else :
                col_kept = self.columnCount()-1
            for col in range(self.columnCount()) :
                if col == col_kept :
                    item = self.item(row, col)
                    font = QFont()
                    font.setBold(True)
                    item.setFont(font)
                    item.setFlags(Qt.ItemIsEnabled)
                else :
                    self.setItem(row, col, QTableWidgetItem(""))

    def reload(self) :        
        self.load_file()
        exercise_settings = ExerciseCreationSettings(self)
        result = exercise_settings.exec()
        if result != QDialog.DialogCode.Accepted :
            return
        self.setRowCount(len(self.elements_list))
        self.load_table()

    def check_answers(self) :
        score = 0
        self.max_score = 0
        for row in range(self.rowCount()) :
            for col in range(self.columnCount()) :
                item = self.item(row, col)
                if item.flags() != Qt.ItemIsEnabled :
                    self.max_score +=1
                    if self.normalize_text(item.text()) == self.normalize_text(self.elements_list[row][self.header_list[col]]) :
                        score += 1   
                        item.setForeground(QColor('lightgreen'))
                    elif item.text() != "" :
                        item.setForeground(QColor('red'))

        score_window = ScoreWindow(self, score, self.max_score, self.parent.settings)
        score_window.show()
