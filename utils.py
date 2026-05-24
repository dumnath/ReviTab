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