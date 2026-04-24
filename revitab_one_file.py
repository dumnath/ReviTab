import sys
import os
from pathlib import Path
import tomlkit as tlk
import glob
import random as rd
from PySide6.QtWidgets import (QApplication, QWidget, QGroupBox, 
                               QFormLayout, QComboBox, QCheckBox, 
                               QVBoxLayout, QPushButton, QHBoxLayout,
                               QMainWindow, QToolBar, QTabWidget, 
                               QLabel, QFileDialog, QTextEdit, 
                               QTableWidget, QMessageBox, QTableWidgetItem,
                               QDialog, QInputDialog, QLineEdit, QSpinBox)
from PySide6.QtGui import QIcon, QAction, QPixmap, QFont, QColor, QMovie, QShortcut, QKeySequence
from PySide6.QtCore import Qt


dir_path = Path.home() / '.revitab'
config_path =dir_path / 'config.toml'


def find_path(path) :
    try :
        filepath = os.path.join(sys._MEIPASS, path)
    except AttributeError:
        filepath = path
    return filepath

def check_config() :
    with open(find_path("Configurations/default_config.toml"), mode = 'rt', encoding = 'utf-8') as f :
        default_config = tlk.load(f)
    if not dir_path.exists() :
        dir_path.mkdir()
        for lang in default_config['langue'].keys() :
            lang_file_path = dir_path / f'{lang}.toml'
            with open(lang_file_path, mode = 'w', encoding ="utf-8") as lang_f :
                tlk.dump(default_config['langue'][lang], lang_f)
    if not config_path.exists() :
        default_config.pop('langue')
        with open(config_path, mode = 'w', encoding='utf-8') as new_f :
            tlk.dump(default_config, new_f)

def set_app_style() :
    with open(config_path, mode = 'rt', encoding = 'utf-8') as config :
        theme = tlk.load(config)['fenetre']['style']
    if theme != 'default' :
        app.setStyleSheet(Path(find_path(f'Themes/{theme}.qss')).read_text())
    else :
        app.setStyleSheet("")

class MainWindow(QMainWindow) :
    def __init__(self) :
        super().__init__()

        self.setWindowTitle("RéviTab")
        self.setWindowIcon(QIcon(find_path("Icons/logo.ico")))
        self.setGeometry(275, 100, 800, 500)

        self.filepaths = {}
        self.elements_list = []
        self.table_data = {}
        self.tab_type = {}
        self.table_modified = {}
        self.load_settings()

        self.shortcut_eszett = QShortcut(QKeySequence("Ctrl+Shift+S"), self)
        self.shortcut_eszett.activated.connect(self.insert_eszett)

        menu_bar = self.menuBar()

        self.file_menu = menu_bar.addMenu("")
        self.edit_menu = menu_bar.addMenu("")
        self.settings_menu = menu_bar.addMenu("")
        self.help_menu = menu_bar.addMenu("")


        #====================FILE MENU====================
        self.open_action = self.create_action('Icons/open_file.png', self.open_document, 'Ctrl+O')
        self.file_menu.addAction(self.open_action)

        self.new_action = self.create_action('Icons/new_file.png', lambda : self.create_csv_tab('Untitled.csv'), 'Ctrl+N')
        self.file_menu.addAction(self.new_action)

        self.save_action = self.create_action('Icons/save.png', self.save_file, 'Ctrl+S')
        self.file_menu.addAction(self.save_action)

        self.file_menu.addSeparator()
        
        self.exit_action = self.create_action('Icons/exit.png', self.on_close, 'Alt+F4')
        self.file_menu.addAction(self.exit_action)

        #====================EDIT MENU====================
        self.add_row_action = self.create_action('Icons/add_row.png', self.add_row)
        self.edit_menu.addAction(self.add_row_action)
        
        self.add_column_action = self.create_action('Icons/add_column.png', self.add_column)
        self.edit_menu.addAction(self.add_column_action)

        self.edit_menu.addSeparator()

        self.delete_row_action = self.create_action('Icons/delete_row.png', self.delete_row)
        self.edit_menu.addAction(self.delete_row_action)

        self.delete_column_action = self.create_action('Icons/delete_column.png', self.delete_column)
        self.edit_menu.addAction(self.delete_column_action)

        self.edit_menu.addSeparator()

        self.rename_header_action = self.create_action('Icons/rename_header.png', self.rename_column)
        self.edit_menu.addAction(self.rename_header_action)

        #====================SETTINGS MENU====================
        self.settings_action = self.create_action('Icons/settings.png', self.change_settings, 'Ctrl+,')
        self.settings_menu.addAction(self.settings_action)

        self.settings_menu.addSeparator()

        self.reset_action = self.create_action('Icons/reset.png', self.reset_settings)
        self.settings_menu.addAction(self.reset_action)

        #====================HELP MENU====================
        self.user_guide_action = self.create_action('Icons/help.png', self.open_user_guide, 'F1')
        self.help_menu.addAction(self.user_guide_action)

        self.about_action = self.create_action('Icons/logo.ico', self.open_about)
        self.help_menu.addAction(self.about_action)

        #====================TOOLBAR WELCOME PAGE====================
        self.toolbar_welcome = QToolBar('')
        self.addToolBar(self.toolbar_welcome)

        self.toolbar_welcome.addAction(self.open_action)
        self.toolbar_welcome.addAction(self.new_action)
        self.toolbar_welcome.addAction(self.user_guide_action)
        self.toolbar_welcome.addAction(self.settings_action)

        #====================TOOLBAR CSV EDITING====================
        self.toolbar_edit = QToolBar('')

        self.toolbar_edit.addAction(self.add_row_action)
        self.toolbar_edit.addAction(self.add_column_action)
        self.toolbar_edit.addSeparator()

        self.toolbar_edit.addAction(self.delete_row_action)
        self.toolbar_edit.addAction(self.delete_column_action)
        self.toolbar_edit.addSeparator()
        
        self.toolbar_edit.addAction(self.rename_header_action)
        self.toolbar_edit.addSeparator()

        self.toolbar_edit.addAction(self.save_action)
        self.exercise_action = self.create_action('Icons/practice.png', self.create_exercise, 'Ctrl+T')
        self.toolbar_edit.addAction(self.exercise_action)

        #====================TOOLBAR PRACTICE TABLE====================
        self.toolbar_practice = QToolBar('')

        self.reload_table_action = self.create_action('Icons/reload.png', self.reload, 'Ctrl+R')
        self.toolbar_practice.addAction(self.reload_table_action)

        self.check_answers_action = self.create_action('Icons/check.png', self.check_answers)
        self.toolbar_practice.addAction(self.check_answers_action)

        #====================STATUSBAR====================
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("RéviTab v2.3", 5000)

        #====================CENTRAL WIDGET====================
        self.tab = QTabWidget(movable=True, tabsClosable=True)
        self.tab.tabCloseRequested.connect(self.confirm_tab_close)
        self.tab.currentChanged.connect(self.on_tab_change)
        self.setCentralWidget(self.tab)

        #====================FIRST PAGE====================
        first_page = QWidget()
        layout_first_page = QVBoxLayout()
        first_page.setLayout(layout_first_page)

        #====================LOGO AND TITLE LAYOUT====================
        layout_header = QHBoxLayout()
        label_logo = QLabel()
        logo_pixmap = QPixmap(find_path('Icons/logo.ico'))
        label_logo.setPixmap(logo_pixmap.scaled(80, 80))
        label_titre = QLabel("RéviTab")
        label_titre.setFont(QFont('Helvetica', 14))
        layout_header.addWidget(label_logo)
        layout_header.addWidget(label_titre)
        layout_header.addStretch()
        layout_first_page.addLayout(layout_header)
        layout_first_page.addStretch()

        #====================CREATE ALL THE OPTION LABELS====================
        self.label_open, layout = self.create_option_layout(find_path('Icons/open_file.png'))
        layout_first_page.addLayout(layout)
        self.label_new, layout = self.create_option_layout(find_path('Icons/new_file.png'))
        layout_first_page.addLayout(layout)
        self.settings_label, layout = self.create_option_layout(find_path('Icons/settings.png'))
        layout_first_page.addLayout(layout)
        self.user_guide_label, layout = self.create_option_layout(find_path('Icons/help.png'))
        layout_first_page.addLayout(layout)
        layout_first_page.addStretch()

        self.tab_type[first_page] = "information"
        self.tab.addTab(first_page, self.texts['welcome_page_title'])
        self.apply_language()

    def on_tab_change(self) :

        self.removeToolBar(self.toolbar_welcome)
        self.removeToolBar(self.toolbar_edit)
        self.removeToolBar(self.toolbar_practice)
        self.current_widget = self.tab.currentWidget()
        if self.current_widget == None :
            self.addToolBar(self.toolbar_welcome)
            self.toolbar_welcome.show()
        elif self.tab_type[self.current_widget]  == 'practice':
            self.addToolBar(self.toolbar_practice)
            self.toolbar_practice.show()
        elif self.tab_type[self.current_widget] == 'information':
            self.addToolBar(self.toolbar_welcome)
            self.toolbar_welcome.show()
        else :
            self.addToolBar(self.toolbar_edit)
            self.toolbar_edit.show()

    def is_tab(self, tab_type) :
        if self.current_widget is not None and self.tab_type[self.current_widget] == tab_type :
            return True
    
    def create_action(self, icon, slot, shortcut =None) :
        action = QAction(QIcon(find_path(icon)), "", self)
        if shortcut :
            action.setShortcut(shortcut)
        action.triggered.connect(slot)
        return action


    def create_option_layout(self, icon_path) :
        layout = QHBoxLayout()
        label_picture = QLabel()
        pixmap = QPixmap(icon_path)
        label_picture.setPixmap(pixmap)
        label_text = QLabel()
        label_text.setFont(QFont('Arial', 13))
        layout.addWidget(label_picture)
        layout.addWidget(label_text)
        layout.addStretch()
        return label_text, layout
    
    def open_document(self) :
        filepath, _ = QFileDialog.getOpenFileName(self, self.texts['select_file'], filter = 'CSV File (*.csv)')
        if filepath :
            self.create_csv_tab(filepath)

    def create_csv_tab(self, filepath) :
        table_edit = QTableWidget()
        self.tab_type[table_edit] = 'edit'
        self.tab.addTab(table_edit, f'{os.path.basename(filepath)}')
        if filepath == 'Untitled.csv' :
            table_edit.setColumnCount(2)
            table_edit.setRowCount(3)
            table_edit.setHorizontalHeaderLabels(['Column 1', 'Column 2'])
            table_edit.setAlternatingRowColors(True)
        else :
            self.get_list(filepath)
            table_edit.setColumnCount(len(self.header_list))
            for i in range(table_edit.columnCount()) :
                table_edit.setColumnWidth(i, int((self.width()-50)/table_edit.columnCount()))
            table_edit.setHorizontalHeaderLabels(self.header_list)
            table_edit.setRowCount(self.nb_questions)
            row = 0
            for v in self.elements_list :
                for f in range(len(self.header_list)) :
                    table_edit.setItem(row, f, QTableWidgetItem(v[self.header_list[f]]))
                row += 1

        self.filepaths[table_edit] = filepath
        self.table_modified[table_edit] = False
        table_edit.itemChanged.connect(lambda : self.mark_modified(table_edit))
        self.tab.setCurrentWidget(table_edit)

    def mark_modified(self, table) :
        self.table_modified[table] = True

    def insert_eszett(self) :
        if self.current_widget == None :
            return
        elif self.tab_type[self.current_widget] == 'information' :
            return
        
        row = self.current_widget.currentRow()
        col = self.current_widget.currentColumn()
        item = self.current_widget.item(row, col)

        editor = self.current_widget.focusWidget()
        if editor and isinstance(editor, QLineEdit) :
            editor.insert("ß")

    def save_file(self) :    
        if not self.is_tab('edit') :
            return
          
        filepath = self.filepaths[self.current_widget]

        if filepath == 'Untitled.csv' :
            filepath, _ = QFileDialog.getSaveFileName(self, self.texts['save_file'], filter ="CSV File (*.csv)")
            if not filepath :
                return
            self.filepaths[self.current_widget] = filepath
            self.tab.setTabText(self.tab.currentIndex(), os.path.basename(filepath))

        row_count = self.current_widget.rowCount()
        col_count = self.current_widget.columnCount()
        content = ""
        header_list = []
        for header in range(col_count) :
            item = self.current_widget.horizontalHeaderItem(header)
            if item != None :
                header_list.append(item.text())
        content += self.separator.join(header_list) +'\n'

        for row in range(row_count) :
            row_data = []
            for col in range(col_count) :
                item = self.current_widget.item(row, col)
                if item != None :
                    row_data.append(item.text() if item else "")
            content += self.separator.join(row_data) +'\n'

        with open(filepath, mode="w", encoding = "utf-8") as csvfile :
            csvfile.write(content)

        self.table_modified[self.current_widget] = False
        self.status_bar.showMessage("File saved", 5000)

    def on_close(self) :
        if self.confirm_exit() :
            self.close()
    
    def confirm_exit(self) :
        if not self.unsaved_files() :
            return True
        
        answer = QMessageBox.question(self, 
                                      self.texts['confirm_title'], 
                                      self.texts['confirm_exit_text'], 
                                      QMessageBox.StandardButton.Yes |
                                      QMessageBox.StandardButton.No)

        if answer == QMessageBox.StandardButton.Yes :
            return True
        else :
            return False

    def unsaved_files(self) :
        for i in range(self.tab.count()) :
            widget = self.tab.widget(i)
            if self.tab_type[widget]  == 'edit':
                if self.table_modified[widget] == True :
                    return True
        return False        

    def confirm_tab_close(self, index) :
        current_widget = self.tab.widget(index)
        if not self.tab_type[current_widget] == 'edit' or self.table_modified[current_widget] == False:
            self.tab.removeTab(index)
            return
        
        answer = QMessageBox.question(self, 
                                      self.texts['confirm_title'], 
                                      self.texts['confirm_exit_text'], 
                                      QMessageBox.StandardButton.Yes |
                                      QMessageBox.StandardButton.No)

        if answer == QMessageBox.StandardButton.Yes :
            self.tab.removeTab(index)    

    def add_row(self) :    
        if not self.is_tab('edit') :
            return
        row = self.current_widget.rowCount()
        self.current_widget.insertRow(row)

    def add_column(self) :    
        if not self.is_tab('edit') :
            return
        column = self.current_widget.columnCount()
        header, ok = QInputDialog.getText(self, self.texts['add_column'], self.texts['header'])
        if header and ok :
            self.current_widget.insertColumn(column)
            self.current_widget.setHorizontalHeaderItem(column, QTableWidgetItem(header))

    def rename_column(self) :    
        if not self.is_tab('edit') :
            return
        column = self.current_widget.currentColumn()
        new_header, ok = QInputDialog.getText(self, self.texts['rename_column'], self.texts['new_header'])
        if new_header and ok :
            self.current_widget.setHorizontalHeaderItem(column, QTableWidgetItem(new_header))

    def delete_row(self) :    
        if not self.is_tab('edit') :
            return
        row = self.current_widget.currentRow()
        if self.confirmation('row', row) :
            self.current_widget.removeRow(row)

    def delete_column(self) :    
        if not self.is_tab('edit') :
            return
        column = self.current_widget.currentColumn()
        if self.confirmation('column', column) :
            self.current_widget.removeColumn(column)

    def confirmation(self, item, item_number) :
        question = QMessageBox.question(self, self.texts['confirm_title'], f"{self.texts['delete_confirmation']} {item} {item_number+1} ?")

        if question == QMessageBox.StandardButton.Yes :
            return True

    def create_exercise(self) :
        if not self.tab_type[self.current_widget] == 'edit' :
            return
        
        if self.table_modified[self.current_widget] == True :
            QMessageBox.information(self, self.texts['save'], self.texts['ask_saving_file'])
            return
        
        try :
            self.get_list(self.filepaths[self.current_widget])
        except :
            QMessageBox.critical(self, self.texts['error'], self.texts['file_not_found'])
            return
        table = QTableWidget()
        self.tab_type[table] = 'practice'
        self.filepaths[table] = self.filepaths[self.current_widget]
        exercise_settings = ExerciseCreationSettings(self)
        result = exercise_settings.exec()
        if result != QDialog.DialogCode.Accepted :
            return
        self.tab.addTab(table, f"{self.texts['exercise_page_title']} {self.tab.tabText(self.tab.currentIndex())}")
        table.setColumnCount(len(self.header_list))
        for i in range(table.columnCount()) :
            table.setColumnWidth(i, int(750/table.columnCount()))
        table.setHorizontalHeaderLabels(self.header_list)
        table.setRowCount(self.nb_questions)
        self.tab.setCurrentWidget(table)
        self.load_table(table)
        
    def get_list(self, filepath) :
        self.elements_list.clear()
        with open(filepath, encoding = 'utf-8') as csvfile :
            line = csvfile.readline()
            row = line.split(self.separator)
            self.header_list = [row[i].strip('\n') for i in range(len(row))]
            for line in csvfile.readlines():
                row = line.split(self.separator)
                if len(row) >= 1 :
                    self.elements_list.append({self.header_list[i] : row[i].strip('\n') for i in range(len(row))})
        self.nb_questions = len(self.elements_list)

    def load_table(self, table) :
        table.clearContents()
        rd.shuffle(self.elements_list)
        self.table_data[table] = self.elements_list.copy()
        row = 0
        for v in self.elements_list :
            for f in range(len(self.header_list)) :
                table.setItem(row, f, QTableWidgetItem(v[self.header_list[f]]))
            row += 1

        for row in range(table.rowCount()) :
            if self.column_shown == "first" :
                col_kept = 0
            elif self.column_shown == "random" :
                col_kept = row % table.columnCount()
            else :
                col_kept = table.columnCount()-1
            for col in range(table.columnCount()) :
                if col == col_kept :
                    item = table.item(row, col)
                    font = QFont()
                    font.setBold(True)
                    item.setFont(font)
                    item.setFlags(Qt.ItemIsEnabled)
                else :
                    table.setItem(row, col, QTableWidgetItem(""))
        
    def reload(self) :    
        if not self.is_tab('practice') :
            return
        
        filepath = self.filepaths[self.current_widget]
        self.get_list(filepath)
        exercise_settings = ExerciseCreationSettings(self)
        result = exercise_settings.exec()
        if result != QDialog.DialogCode.Accepted :
            return
        self.current_widget.setRowCount(self.nb_questions)
        self.load_table(self.current_widget)

    def check_answers(self) :    
        if not self.is_tab('practice') :
            return
        data = self.table_data[self.current_widget]
        headers = list(data[0].keys())
        score = 0
        self.max_score = 0
        for row in range(self.current_widget.rowCount()) :
            for col in range(self.current_widget.columnCount()) :
                item = self.current_widget.item(row, col)
                if item.flags() != Qt.ItemIsEnabled :
                    self.max_score +=1
                    if self.normalize_text(item.text()) == self.normalize_text(data[row][headers[col]]) :
                        score += 1   
                        item.setForeground(QColor('lightgreen'))
                    elif item.text() != "" :
                        item.setForeground(QColor('red'))

        score_window = ScoreWindow(self, score, self.max_score)
        score_window.show()

    def normalize_text(self, text) :
        if self.case_tolerance == True :
            text = text.lower()
        if self.space_tolerance == True :
            text = text.strip()
        return text

    def load_settings(self) :
        with open(config_path, mode = 'rt', encoding = 'utf-8') as config :
            self.settings = tlk.load(config)
            self.default_language = self.settings['fenetre']['langue_par_defaut']
            self.case_tolerance = self.settings['exercice']['tolerance_casse']
            self.space_tolerance = self.settings['exercice']['tolerance_espaces']
            self.column_shown = self.settings['exercice']['column_shown']
            self.display_images = self.settings['frame_fin_exercice_gif']['gif_fin_exercice']
            self.separator = self.settings['fichiers']['separateur']
        lang_path = dir_path / f'{self.default_language}.toml'
        try :
            with open(lang_path, mode = 'rt', encoding = "utf-8") as lang_config :
                self.texts = tlk.load(lang_config)
        except FileNotFoundError :
            QMessageBox.critical(self, 'FileNotFoundError',  f'{lang_path} not found.')

    def change_settings(self) :
        self.settings_window = SettingsWindow(self)
        self.settings_window.show()

    def reset_settings(self) :
        self.settings['fenetre']['langue_par_defaut'] = 'english'
        self.settings['fenetre']['style'] = 'default'
        self.settings['fichiers']['separateur'] = ';'
        self.settings['exercice']['tolerance_casse'] = True
        self.settings['exercice']['tolerance_espaces'] = True
        self.settings['exercice']['column_shown'] = "random"
        self.settings['frame_fin_exercice_gif']['gif_fin_exercice'] = True
        with open(config_path, mode = 'wt', encoding = 'utf-8') as config :
            tlk.dump(self.settings, config)
        self.load_settings()
        set_app_style()
        self.apply_language()

    def open_user_guide(self) :
        title = self.texts['user_guide']
        self.show_help_doc(find_path('README.md'), title, True)
    
    def open_about(self) :
        title = self.texts['about']
        self.show_help_doc(find_path('LICENSE'), title)

    def show_help_doc(self, filepath, title, html=None) :
        with open(filepath, encoding='utf-8') as about :
            contenu = about.read()
        text_edit = QTextEdit()
        if html :
            text_edit.setHtml(contenu)
        else :
            text_edit.setText(contenu)
        text_edit.setFont(QFont('Helvetica', 12))
        text_edit.setReadOnly(True)
        text_edit.document().setModified(False)
        self.tab_type[text_edit] = 'information'
        self.tab.addTab(text_edit, title)
        self.tab.setCurrentWidget(text_edit)

    def apply_language(self) :

        self.file_menu.menuAction().setText(f"&{self.texts['file']}")
        self.edit_menu.menuAction().setText(f"&{self.texts['edit']}")
        self.settings_menu.menuAction().setText(f"&{self.texts['settings']}")
        self.help_menu.menuAction().setText(f"&{self.texts['help']}")

        self.open_action.setText(self.texts['open'])
        self.open_action.setStatusTip(self.texts['open_description'])

        self.new_action.setText(self.texts['new'])
        self.new_action.setStatusTip(self.texts['new_description'])

        self.save_action.setText(self.texts['save'])
        self.save_action.setStatusTip(self.texts['save_description'])

        self.exit_action.setText(self.texts['exit'])
        self.exit_action.setStatusTip(self.texts['exit'])
        
        self.settings_action.setText(self.texts['settings'] + "...")
        self.settings_action.setStatusTip(self.texts['settings_description'])
        
        self.reset_action.setText(self.texts['reset'])
        self.reset_action.setStatusTip(self.texts['reset_description'])
        
        self.user_guide_action.setText(self.texts['user_guide'])
        self.user_guide_action.setStatusTip(self.texts['user_guide_description'])

        self.about_action.setText(self.texts['about'])
        self.about_action.setStatusTip(self.texts['about_description'])

        self.exercise_action.setText(self.texts['practice'])
        self.exercise_action.setStatusTip(self.texts['practice_description'])

        self.reload_table_action.setText(self.texts['reload'])
        self.reload_table_action.setStatusTip(self.texts['reload_description'])

        self.check_answers_action.setText(self.texts['check'])
        self.check_answers_action.setStatusTip(self.texts['check_description'])

        self.add_row_action.setText(self.texts['add_row'])
        self.add_row_action.setStatusTip(self.texts['add_row_description'])

        self.add_column_action.setText(self.texts['add_column'])
        self.add_column_action.setStatusTip(self.texts['add_column_description'])

        self.delete_row_action.setText(self.texts['delete_row'])
        self.delete_row_action.setStatusTip(self.texts['delete_row_description'])

        self.delete_column_action.setText(self.texts['delete_column'])
        self.delete_column_action.setStatusTip(self.texts['delete_column_description'])

        self.rename_header_action.setText(self.texts['rename_column'])
        self.rename_header_action.setStatusTip(self.texts['rename_column_description'])

        self.toolbar_welcome.setWindowTitle(self.texts['welcome_toolbar'])
        self.toolbar_edit.setWindowTitle(self.texts['edit_toolbar'])
        self.toolbar_practice.setWindowTitle(self.texts['practice_toolbar'])

        self.label_open.setText(self.texts['open_description'] + ' : Ctrl+O')
        self.label_new.setText(self.texts['new_description'] + ' : Ctrl+N')
        self.settings_label.setText(self.texts['settings_description'] + ' : Ctrl+,')
        self.user_guide_label.setText(self.texts['user_guide_description'] + ' : F1')


class SettingsWindow(QDialog) :
    def __init__(self, parent) :
        super().__init__(parent)
        self.parent = parent

        self.setWindowTitle("Settings")
        self.setWindowIcon(QIcon(find_path("Icons/settings.png")))

        settings_layout = QVBoxLayout()
        self.setLayout(settings_layout)

        self.app_gb = QGroupBox()
        self.app_layout = QFormLayout()
        self.app_gb.setLayout(self.app_layout)
        settings_layout.addWidget(self.app_gb)

        self.language_cb = QComboBox()
        self.label_default_language = QLabel()
        self.app_layout.addRow(self.label_default_language, self.language_cb)

        self.style_cb = QComboBox()
        self.label_style = QLabel()
        self.app_layout.addRow(self.label_style, self.style_cb)

        self.exercise_gb = QGroupBox()
        self.exercise_layout = QFormLayout()
        self.exercise_gb.setLayout(self.exercise_layout)
        settings_layout.addWidget(self.exercise_gb)

        self.case_tol_chb = QCheckBox()
        self.label_case_tol = QLabel()
        self.exercise_layout.addRow(self.label_case_tol, self.case_tol_chb)

        self.space_tol_chb = QCheckBox()
        self.label_space_tol = QLabel()
        self.exercise_layout.addRow(self.label_space_tol, self.space_tol_chb)

        self.display_images_chb = QCheckBox()
        self.label_display_images = QLabel()
        self.exercise_layout.addRow(self.label_display_images, self.display_images_chb)

        self.column_shown_cb = QComboBox()
        self.label_column_shown = QLabel()
        self.exercise_layout.addRow(self.label_column_shown, self.column_shown_cb)

        self.file_gb = QGroupBox()
        self.file_layout = QFormLayout()
        self.file_gb.setLayout(self.file_layout)
        settings_layout.addWidget(self.file_gb)

        self.separator_cb = QComboBox(editable=True)
        self.label_sep = QLabel()
        self.file_layout.addRow(self.label_sep, self.separator_cb)

        buttons_layout = QHBoxLayout()
        settings_layout.addLayout(buttons_layout)

        self.ok_button = QPushButton()
        self.ok_button.clicked.connect(self.ok)
        buttons_layout.addWidget(self.ok_button)

        self.apply_button = QPushButton()
        self.apply_button.clicked.connect(self.apply_changes)
        buttons_layout.addWidget(self.apply_button)

        self.cancel_button = QPushButton()
        self.cancel_button.clicked.connect(self.close)
        buttons_layout.addWidget(self.cancel_button)
        
        self.apply_language_settings()
        self.load_settings()

    def load_settings(self) :
        self.language_cb.clear()
        self.style_cb.clear()
        self.column_shown_cb.clear()
        self.separator_cb.clear()

        language_path_list = (dir_path.glob('*.toml'))
        language_list = [os.path.basename(f).strip('.toml') for f in language_path_list]
        language_list.remove('config')
        self.language_cb.addItems(language_list)
        self.language_cb.setCurrentText(self.parent.default_language)

        
        style_path_list = glob.glob(find_path('Themes/*.qss'))
        style_list = [os.path.basename(f).strip('.qss') for f in style_path_list]
        style_list.append('default')
        default_style = self.parent.settings['fenetre']['style']
        self.style_cb.addItems(style_list)
        self.style_cb.setCurrentText(default_style)

        self.case_tol_chb.setChecked(self.parent.case_tolerance)
        self.space_tol_chb.setChecked(self.parent.space_tolerance)
        self.display_images_chb.setChecked(self.parent.display_images)
        self.column_shown_cb.addItems(['first', 'random', 'last'])
        self.column_shown_cb.setCurrentText(self.parent.settings['exercice']['column_shown'])

        self.separator_cb.addItems([';', ',', '|', '.'])
        self.separator_cb.setCurrentText(self.parent.separator)

    def apply_language_settings(self) :
        texts = self.parent.texts

        self.app_gb.setTitle(texts['application'])
        self.label_default_language.setText(texts['default_language'])
        self.label_style.setText(texts['app_style'])

        self.exercise_gb.setTitle(texts['exercise_page_title'])
        self.label_case_tol.setText(texts['case_tolerance'])
        self.label_space_tol.setText(texts['space_tolerance'])
        self.label_display_images.setText(texts['display_images'])
        self.label_column_shown.setText(texts['column_shown'])

        self.file_gb.setTitle(texts['csv_file_settings'])
        self.label_sep.setText(texts['separator'])

        self.ok_button.setText(texts['ok'])
        self.apply_button.setText(texts['apply'])
        self.cancel_button.setText(texts['cancel'])


    def apply_changes(self) :
        self.parent.settings['fenetre']['langue_par_defaut'] = self.language_cb.currentText()
        self.parent.settings['fenetre']['style'] = self.style_cb.currentText()

        self.parent.settings['exercice']['tolerance_casse'] = self.case_tol_chb.isChecked()
        self.parent.settings['exercice']['tolerance_espaces'] = self.space_tol_chb.isChecked()
        self.parent.settings['frame_fin_exercice_gif']['gif_fin_exercice'] = self.display_images_chb.isChecked()
        self.parent.settings['exercice']['column_shown'] = self.column_shown_cb.currentText()

        self.parent.settings['fichiers']['separateur'] = self.separator_cb.currentText()

        with open(config_path, mode = 'wt', encoding='utf-8') as config :
            tlk.dump(self.parent.settings, config)

        set_app_style()
        self.parent.load_settings()
        self.parent.apply_language()
        self.apply_language_settings()
        self.load_settings()


    def ok(self) :
        self.apply_changes()
        self.close()


class ScoreWindow(QDialog) :
    def __init__(self, parent, score, max_score) :
        super().__init__(parent)
        self.parent = parent
        texts = self.parent.texts

        self.setWindowTitle(texts['score'])
        self.setWindowIcon(QIcon(find_path('Icons/score.png')))

        layout = QVBoxLayout()
        self.setLayout(layout)
        label_gif = QLabel(alignment=Qt.AlignmentFlag.AlignHCenter)

        if score/max_score <= 0.25 :
            gifs_list = self.parent.settings['frame_fin_exercice_gif']['gifs_very_bad']
            gif = rd.choice(gifs_list)
        elif score/max_score <= 0.5 :
            gifs_list = self.parent.settings['frame_fin_exercice_gif']['gifs_quite_bad']
            gif = rd.choice(gifs_list)
        elif score/max_score <= 0.75 :
            gifs_list = self.parent.settings['frame_fin_exercice_gif']['gifs_good']
            gif = rd.choice(gifs_list)
        else :
            gifs_list = self.parent.settings['frame_fin_exercice_gif']['gifs_excellent']
            gif = rd.choice(gifs_list)
        if self.parent.display_images == True :
            qmovie = QMovie(find_path(gif))
            qmovie.start()
            qmovie_size = qmovie.currentImage().size()
            qmovie.setScaledSize(qmovie_size*200/qmovie_size.width())

            label_gif.setMovie(qmovie)
            layout.addWidget(label_gif)
            layout.addStretch()
            self.setFixedSize(300, 300)
        else :
            self.setFixedSize(200, 100)

        label_score = QLabel(f"{texts['score_text']} {score} / {max_score}.", alignment = Qt.AlignmentFlag.AlignHCenter)
        label_score.setFont(QFont('Helvetica', 12))
        layout.addWidget(label_score)
        layout.addStretch()

        layout_btn = QHBoxLayout()
        layout.addLayout(layout_btn)

        ok_btn = QPushButton(texts['ok'])
        ok_btn.clicked.connect(self.close)
        layout_btn.addWidget(ok_btn)

        new_exercise_btn = QPushButton(texts['new_exercise'])
        new_exercise_btn.clicked.connect(self.new_exercise)
        layout_btn.addWidget(new_exercise_btn)

    def new_exercise(self) :
        self.parent.reload()
        self.close()


class ExerciseCreationSettings(QDialog) :
    def __init__(self, parent) :
        super().__init__(parent)
        self.parent = parent
        maximum = self.parent.nb_questions
        texts = self.parent.texts

        self.setWindowTitle(texts['practice'])
        self.setWindowIcon(QIcon("Icons/practice.png"))

        layout = QFormLayout()
        self.setLayout(layout)

        self.label_nb_questions = QLabel(texts['nb_of_questions'])
        self.nb_questions_sb = QSpinBox(maximum=maximum, minimum=1, value = maximum, wrapping = True)
        self.nb_questions_sb.valueChanged.connect(self.on_change)
        layout.addRow(self.label_nb_questions, self.nb_questions_sb)

        self.label_from_questions = QLabel(texts['from_line'])
        self.from_questions_sb = QSpinBox(maximum=maximum, minimum=1, value = 1, wrapping=True)
        self.from_questions_sb.valueChanged.connect(self.on_change)
        layout.addRow(self.label_from_questions, self.from_questions_sb)

        self.label_to = QLabel(texts['to_line'])
        self.to_sb = QSpinBox(maximum=maximum, minimum=1, value=maximum, wrapping=True)
        self.to_sb.valueChanged.connect(self.on_change)
        layout.addRow(self.label_to, self.to_sb)

        layout_button = QHBoxLayout()
        self.ok_button = QPushButton(texts['ok'])
        self.ok_button.clicked.connect(self.ok)
        layout_button.addWidget(self.ok_button)
        self.cancel_button = QPushButton(texts['cancel'])
        self.cancel_button.clicked.connect(self.close)
        layout_button.addWidget(self.cancel_button)
        layout.addRow(layout_button)

    def on_change(self) :
        nb_questions = self.nb_questions_sb.value()
        from_value = self.from_questions_sb.value()
        to_value = self.to_sb.value()
        if from_value > to_value :
            self.to_sb.setValue(from_value)
        if nb_questions > to_value - from_value +1 :
            self.nb_questions_sb.setValue(to_value-from_value+1)

    def ok(self) :
        self.parent.nb_questions = self.nb_questions_sb.value()
        self.parent.elements_list = self.parent.elements_list[self.from_questions_sb.value()-1:self.to_sb.value()]
        self.accept()

if __name__ == '__main__' :
    check_config()
    app = QApplication(sys.argv)
    set_app_style()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())