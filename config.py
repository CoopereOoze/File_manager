"""
Конфигурация файлового менеджера
"""

import json
import os

CONFIG_FILE = "config.json"

def load_config():
    """Загрузка конфигурации из файла"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    else:
        config = {"root_directory": "./my_files"}
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f)
        return config

config = load_config()
WORK_DIR = config["root_directory"]