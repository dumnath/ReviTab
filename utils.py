import sys
import os

def find_path(path) :
    try :
        filepath = os.path.join(sys._MEIPASS, path)
    except AttributeError:
        filepath = path
    return filepath

def translate_action(action, text, description) :
    action.setText(text)
    action.setStatusTip(description)


def normalize_text(self, text) :
    if self.parent.case_tolerance == True :
        text = text.lower()
    if self.parent.space_tolerance == True :
        text = text.strip()
    return text