from utils import find_path
from pathlib import Path
import tomlkit as tlk

dir_path = Path.home() / '.revitab'
config_path =dir_path / 'config.toml'

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

def set_app_style(app) :
    with open(config_path, mode = 'rt', encoding = 'utf-8') as config :
        theme = tlk.load(config)['fenetre']['style']
    if theme != 'default' :
        app.setStyleSheet(Path(find_path(f'Themes/{theme}.qss')).read_text())
    else :
        app.setStyleSheet("")
