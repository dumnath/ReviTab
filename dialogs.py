from PySide6.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QGroupBox, QLabel, QComboBox, QCheckBox, QPushButton, QSpinBox, QLineEdit
from PySide6.QtGui import QIcon, QFont, QMovie
from PySide6.QtCore import Qt
from config import find_path, dir_path, config_path, set_app_style
import glob
import os
import tomlkit as tlk
import random as rd

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

        self.tables_gb = QGroupBox()
        self.tables_layout = QFormLayout()
        self.tables_gb.setLayout(self.tables_layout)
        settings_layout.addWidget(self.tables_gb)

        self.alternating_row_colors_chb = QCheckBox()
        self.label_alternating_row_colors = QLabel()
        self.tables_layout.addRow(self.label_alternating_row_colors, self.alternating_row_colors_chb)

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

        self.alternating_row_colors_chb.setChecked(self.parent.alternating_row_colors)

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

        self.tables_gb.setTitle(texts['tables_settings'])
        self.label_alternating_row_colors.setText(texts['alternating_row_colors'])

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

        self.parent.settings['fichiers']['alternating_row_colors'] = self.alternating_row_colors_chb.isChecked()

        with open(config_path, mode = 'wt', encoding='utf-8') as config :
            tlk.dump(self.parent.settings, config)

        set_app_style(QApplication.instance())
        self.parent.load_settings()
        self.parent.apply_language()
        self.apply_language_settings()
        self.load_settings()

    def ok(self) :
        self.apply_changes()
        self.close()


class ScoreWindow(QDialog) :
    def __init__(self, parent, score, max_score, settings) :
        super().__init__(parent)
        texts = parent.texts
        self.parent = parent

        self.setWindowTitle(texts['score'])
        self.setWindowIcon(QIcon(find_path('Icons/score.png')))

        layout = QVBoxLayout()
        self.setLayout(layout)
        label_gif = QLabel(alignment=Qt.AlignmentFlag.AlignHCenter)

        if score/max_score <= 0.25 :
            gifs_list = settings['frame_fin_exercice_gif']['gifs_very_bad']
            gif = rd.choice(gifs_list)
        elif score/max_score <= 0.5 :
            gifs_list = settings['frame_fin_exercice_gif']['gifs_quite_bad']
            gif = rd.choice(gifs_list)
        elif score/max_score <= 0.75 :
            gifs_list = settings['frame_fin_exercice_gif']['gifs_good']
            gif = rd.choice(gifs_list)
        else :
            gifs_list = settings['frame_fin_exercice_gif']['gifs_excellent']
            gif = rd.choice(gifs_list)
        if settings['frame_fin_exercice_gif']['gif_fin_exercice'] == True :
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
        maximum = len(self.parent.elements_list)
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


class ExportPDFSettings(QDialog) :
    def __init__(self, parent) :
        super().__init__(parent)
        self.parent = parent
        texts = self.parent.texts

        self.setWindowTitle(texts['export_pdf'])
        self.setWindowIcon(QIcon("Icons/pdf.png"))

        layout = QFormLayout()
        self.setLayout(layout)

        self.pdf_title = QLineEdit()
        self.pdf_title.setText("PDF Export")
        layout.addRow(QLabel(texts['pdf_title']), self.pdf_title)

        self.pdf_header_chb = QCheckBox()
        layout.addRow(QLabel(texts['pdf_header']), self.pdf_header_chb)

        self.pdf_column_header_chb = QCheckBox()
        layout.addRow(QLabel(texts['pdf_column_header']), self.pdf_column_header_chb)

        self.pdf_insert_image_after = QCheckBox()
        layout.addRow(QLabel(texts['pdf_insert_image_after']), self.pdf_insert_image_after)

        layout_button = QHBoxLayout()
        self.ok_button = QPushButton(texts['ok'])
        self.ok_button.clicked.connect(self.ok)
        layout_button.addWidget(self.ok_button)
        self.cancel_button = QPushButton(texts['cancel'])
        self.cancel_button.clicked.connect(self.close)
        layout_button.addWidget(self.cancel_button)
        layout.addRow(layout_button)

    def ok(self) :
        self.parent.pdf_title = self.pdf_title.text()
        self.parent.pdf_header = self.pdf_header_chb.isChecked()
        self.parent.pdf_column_header = self.pdf_column_header_chb.isChecked()
        self.parent.pdf_insert_image_after = self.pdf_insert_image_after.isChecked()
        self.accept()