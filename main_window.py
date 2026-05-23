from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QTabWidget, QToolBar, QFileDialog, QMessageBox, QTextEdit, QDialog)
from PySide6.QtGui import QIcon, QPixmap, QFont, QKeySequence, QAction, QShortcut
from config import config_path, dir_path, set_app_style
from utils import find_path, translate_action
from tables import EditTable, PracticeTable
from dialogs import SettingsWindow, ExportPDFSettings
from pdf_export import generate_pdf
import os
import tomlkit as tlk



class MainWindow(QMainWindow) :
    def __init__(self) :
        super().__init__()

        self.setWindowTitle("RéviTab")
        self.setWindowIcon(QIcon(find_path("Icons/logo.ico")))
        self.setGeometry(275, 100, 800, 500)

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

        self.export_pdf_action = self.create_action('Icons/pdf.png', self.export_pdf, 'Ctrl+P')
        self.file_menu.addAction(self.export_pdf_action)

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
        self.toolbar_edit.addAction(self.export_pdf_action)
        self.exercise_action = self.create_action('Icons/practice.png', self.create_exercise, 'Ctrl+T')
        self.toolbar_edit.addAction(self.exercise_action)

        #====================TOOLBAR PRACTICE TABLE====================
        self.toolbar_practice = QToolBar('')

        self.reload_table_action = self.create_action('Icons/reload.png', self.reload, 'Ctrl+R')
        self.toolbar_practice.addAction(self.reload_table_action)

        self.check_answers_action = self.create_action('Icons/check.png', self.check_answers)
        self.toolbar_practice.addAction(self.check_answers_action)

        self.toolbar_practice.addAction(self.export_pdf_action)

        #====================STATUSBAR====================
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("RéviTab v2.6", 5000)

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
        elif isinstance(self.current_widget, EditTable):
            self.addToolBar(self.toolbar_edit)
            self.toolbar_edit.show()
        elif isinstance(self.current_widget, PracticeTable):
            self.addToolBar(self.toolbar_practice)
            self.toolbar_practice.show()
        else :
            self.addToolBar(self.toolbar_welcome)
            self.toolbar_welcome.show() 
    
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
        table_edit = EditTable(self, filepath)
        self.tab.addTab(table_edit, f'{os.path.basename(filepath)}')
        self.tab.setCurrentWidget(table_edit)

    def insert_eszett(self) :
        if isinstance(self.current_widget, EditTable) :
            self.current_widget.insert_eszett()

    def save_file(self) :
        if not isinstance(self.current_widget, EditTable):
            return
          
        filepath = self.current_widget.filepath

        if filepath == 'Untitled.csv' :
            filepath, _ = QFileDialog.getSaveFileName(self, self.texts['save_file'], filter ="CSV File (*.csv)")
            if not filepath :
                return
            self.filepaths[self.current_widget] = filepath
            self.tab.setTabText(self.tab.currentIndex(), os.path.basename(filepath))


        with open(filepath, mode="w", encoding = "utf-8") as csvfile :
            csvfile.write(self.current_widget.extract_data())

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
            if isinstance(widget, EditTable) and widget.modified == True :
                    return True
        return False

    def confirm_tab_close(self, index) :
        current_widget = self.tab.widget(index)
        if not isinstance(current_widget, EditTable) or current_widget.modified == False:
            self.tab.removeTab(index)
            return
        
        answer = QMessageBox.question(self, 
                                      self.texts['confirm_title'], 
                                      self.texts['confirm_exit_text'], 
                                      QMessageBox.StandardButton.Yes |
                                      QMessageBox.StandardButton.No)

        if answer == QMessageBox.StandardButton.Yes :
            self.tab.removeTab(index)    

    def export_pdf(self) :
        if not isinstance(self.current_widget, PracticeTable) and not isinstance(self.current_widget, EditTable):
            return
        
        self.pdf_header = False
        self.pdf_column_header = False
        self.pdf_title = "PDF Export"
        self.pdf_insert_image_after = False
        export_settings = ExportPDFSettings(self)
        result = export_settings.exec()
        if result != QDialog.DialogCode.Accepted :
            return
        
        filepath, _ = QFileDialog.getSaveFileName(self, self.texts['export_pdf'], filter = "PDF File (*.pdf)")
        if not filepath :
            return
    
        data = [[self.current_widget.item(row, col).text() if self.current_widget.item(row, col) else "" 
                for col in range(self.current_widget.columnCount())] 
                for row in range(self.current_widget.rowCount())]
        
        generate_pdf(filepath, self.texts, data, self.pdf_title, self.pdf_header, 
                     self.pdf_column_header, self.current_widget.header_list, 
                     self.pdf_insert_image_after)

        
    def add_row(self) :    
        if isinstance(self.current_widget, EditTable) :
            self.current_widget.add_row()

    def add_column(self) :    
        if isinstance(self.current_widget, EditTable) :
            self.current_widget.add_column()

    def rename_column(self) :    
        if isinstance(self.current_widget, EditTable) :
            self.current_widget.rename_column()

    def delete_row(self) :    
        if isinstance(self.current_widget, EditTable) :
            self.current_widget.delete_row()

    def delete_column(self) :    
        if isinstance(self.current_widget, EditTable) :
            self.current_widget.delete_column()

    def create_exercise(self) :
        if not isinstance(self.current_widget, EditTable) :
            return
        
        if self.current_widget.modified == True :
            QMessageBox.information(self, self.texts['save'], self.texts['ask_saving_file'])
            return
        
        table = PracticeTable(self, self.current_widget.filepath)
        if table.failed == False :
            self.tab.addTab(table, f"{self.texts['exercise_page_title']} {self.tab.tabText(self.tab.currentIndex())}")
        self.tab.setCurrentWidget(table)

    def reload(self) :
        if isinstance(self.current_widget, PracticeTable) :
            self.current_widget.reload()

    def check_answers(self) :    
        if isinstance(self.current_widget, PracticeTable) :
            self.current_widget.check_answers()

    def load_settings(self) :
        with open(config_path, mode = 'rt', encoding = 'utf-8') as config :
            self.settings = tlk.load(config)
            self.default_language = self.settings['fenetre']['langue_par_defaut']
            self.case_tolerance = self.settings['exercice']['tolerance_casse']
            self.space_tolerance = self.settings['exercice']['tolerance_espaces']
            self.column_shown = self.settings['exercice']['column_shown']
            self.display_images = self.settings['frame_fin_exercice_gif']['gif_fin_exercice']
            self.separator = self.settings['fichiers']['separateur']
            self.alternating_row_colors = self.settings['fichiers']['alternating_row_colors']
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
        self.settings['fichiers']['alternating_row_colors'] = True
        with open(config_path, mode = 'wt', encoding = 'utf-8') as config :
            tlk.dump(self.settings, config)
        self.load_settings()
        set_app_style(QApplication.instance())
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
        self.tab.addTab(text_edit, title)
        self.tab.setCurrentWidget(text_edit)

    def apply_language(self) :
        self.file_menu.menuAction().setText(f"&{self.texts['file']}")
        self.edit_menu.menuAction().setText(f"&{self.texts['edit']}")
        self.settings_menu.menuAction().setText(f"&{self.texts['settings']}")
        self.help_menu.menuAction().setText(f"&{self.texts['help']}")

        translate_action(self.open_action, self.texts['open'], self.texts['open_description'])
        translate_action(self.new_action, self.texts['new'], self.texts['new_description'])
        translate_action(self.save_action, self.texts['save'], self.texts['save_description'])
        translate_action(self.export_pdf_action, self.texts['export_pdf'], self.texts['export_pdf_description'])
        translate_action(self.exit_action, self.texts['exit'], self.texts['exit'])

        translate_action(self.settings_action, self.texts['settings'] + "...", self.texts['settings_description'])
        translate_action(self.reset_action, self.texts['reset'], self.texts['reset_description'])

        translate_action(self.user_guide_action, self.texts['user_guide'], self.texts['user_guide_description'])
        translate_action(self.about_action, self.texts['about'], self.texts['about_description'])

        translate_action(self.exercise_action, self.texts['practice'], self.texts['practice_description'])
        translate_action(self.reload_table_action, self.texts['reload'], self.texts['reload_description'])
        translate_action(self.check_answers_action, self.texts['check'], self.texts['check_description'])

        translate_action(self.add_row_action, self.texts['add_row'], self.texts['add_row_description'])
        translate_action(self.add_column_action, self.texts['add_column'], self.texts['add_column_description'])
        translate_action(self.delete_row_action, self.texts['delete_row'], self.texts['delete_row_description'])
        translate_action(self.delete_column_action, self.texts['delete_column'], self.texts['delete_column_description'])
        translate_action(self.rename_header_action, self.texts['rename_column'], self.texts['rename_column_description'])

        self.toolbar_welcome.setWindowTitle(self.texts['welcome_toolbar'])
        self.toolbar_edit.setWindowTitle(self.texts['edit_toolbar'])
        self.toolbar_practice.setWindowTitle(self.texts['practice_toolbar'])

        self.label_open.setText(self.texts['open_description'] + ' : Ctrl+O')
        self.label_new.setText(self.texts['new_description'] + ' : Ctrl+N')
        self.settings_label.setText(self.texts['settings_description'] + ' : Ctrl+,')
        self.user_guide_label.setText(self.texts['user_guide_description'] + ' : F1')
