"""
Файловый менеджер
"""

import os
import shutil
from config import WORK_DIR

# Работа с файловой системой
def create_directory(path):
    """Создание директории """
    if os.path.exists(path):
        print(f"Директория {path} уже существует")
    else:
        os.makedirs(path)
        print(f"Директория {path} создана")

def list_all_files(directory):
    """Перечисление всех файлов в директории и поддиректориях """
    for root, dirs, files in os.walk(directory):
        for file in files:
            print(os.path.join(root, file))

#  Работа с процессами 
def run_command(command):
    pass

# Работа с системной информацией =

def show_system_info():
    """Отображение системной информации """
    import platform
    print(f"ОС: {platform.system()} {platform.release()}")
    print(f"Версия Python: {platform.python_version()}")
    print(f"Текущий рабочий каталог: {os.getcwd()}")

def show_env_vars():
    """Вывод переменных окружения """
    print("Переменные окружения:")
    for key, value in os.environ.items():
        print(f"{key}: {value}")

# Проверка безопасности 

def is_safe_path(path):
    """Проверка, что путь внутри рабочей директории"""
    return os.path.abspath(path).startswith(os.path.abspath(WORK_DIR))

# Основной класс 

class FileManager:
    def __init__(self, root_dir):
        self.root_dir = os.path.abspath(root_dir)
        self.current_dir = self.root_dir
    
    def make_directory(self, name):
        """Создание директории"""
        path = os.path.join(self.current_dir, name)
        create_directory(path)
    
    def list_files(self, path="."):
        """Перечисление файлов"""
        target = os.path.join(self.current_dir, path)
        if not is_safe_path(target):
            print("Выход за пределы рабочей директории запрещён")
            return
        if os.path.exists(target):
            list_all_files(target)
        else:
            print("Путь не существует")
    
    # Навигация
    def change_directory(self, path):
        """Смена директории"""
        if path == "..":
            new_path = os.path.dirname(self.current_dir)
        else:
            new_path = os.path.abspath(os.path.join(self.current_dir, path))
        
        if not is_safe_path(new_path):
            print("Выход за пределы рабочей директории запрещён")
        elif os.path.isdir(new_path):
            self.current_dir = new_path
            print(f"Текущий каталог: {self.current_dir}")
        else:
            print("Не директория")
    
    def get_current_dir(self):
        """Показать текущий каталог"""
        print(self.current_dir)
    
    # Работа с файлами
    def create_file(self, name, content=""):
        """Создание файла (аналог touch)"""
        path = os.path.join(self.current_dir, name)
        if os.path.exists(path):
            print("Файл уже существует")
        else:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Файл {name} создан")
    
    def read_file(self, name):
        """Чтение файла (аналог cat)"""
        path = os.path.join(self.current_dir, name)
        if os.path.isfile(path):
            with open(path, 'r', encoding='utf-8') as f:
                print(f.read())
        else:
            print("Файл не найден")
    
    def write_file(self, name, content):
        """Запись в файл"""
        path = os.path.join(self.current_dir, name)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Записано в {name}")
    
    def delete_file(self, name):
        """Удаление файла"""
        path = os.path.join(self.current_dir, name)
        if os.path.isfile(path):
            os.remove(path)
            print(f"Файл {name} удалён")
        else:
            print("Файл не найден")
    
    def copy_file(self, src, dst):
        """Копирование файла"""
        src_path = os.path.join(self.current_dir, src)
        dst_path = os.path.join(self.current_dir, dst)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
            print(f"Скопировано {src} -> {dst}")
        else:
            print("Источник не файл")
    
    def move_file(self, src, dst):
        """Перемещение файла"""
        src_path = os.path.join(self.current_dir, src)
        dst_path = os.path.join(self.current_dir, dst)
        if os.path.exists(src_path):
            shutil.move(src_path, dst_path)
            print(f"Перемещено {src} -> {dst}")
        else:
            print("Источник не найден")
    
    def rename_file(self, old, new):
        """Переименование"""
        old_path = os.path.join(self.current_dir, old)
        new_path = os.path.join(self.current_dir, new)
        if os.path.exists(old_path):
            os.rename(old_path, new_path)
            print(f"Переименовано {old} -> {new}")
        else:
            print("Файл не найден")
    
    def delete_directory(self, name):
        """Удаление директории"""
        path = os.path.join(self.current_dir, name)
        if os.path.isdir(path):
            shutil.rmtree(path)
            print(f"Папка {name} удалена")
        else:
            print("Не директория или не существует")
    
    def show_info(self):
        """Показать системную информацию"""
        show_system_info()
    
    def show_env(self):
        """Показать переменные окружения"""
        show_env_vars()

# Главная функция 

def main():
    fm = FileManager(WORK_DIR)
    
    print(f"ФАЙЛОВЫЙ МЕНЕДЖЕР")
    print(f"Рабочая директория: {fm.root_dir}")
    print("Команды: mkdir, ls, cd, pwd, touch, cat, write, rm, cp, mv, rename, rmdir, info, env, exit\n")
    
    while True:
        try:
            cmd = input(f"{os.path.basename(fm.current_dir)}> ").strip()
            if not cmd:
                continue
            
            parts = cmd.split()
            command = parts[0]
            
            if command == "mkdir":
                if len(parts) < 2:
                    print("Нужно имя папки")
                else:
                    fm.make_directory(parts[1])
            
            elif command == "ls":
                path = parts[1] if len(parts) > 1 else "."
                fm.list_files(path)
            
            elif command == "cd":
                if len(parts) < 2:
                    print("Нужен путь")
                else:
                    fm.change_directory(parts[1])
            
            elif command == "pwd":
                fm.get_current_dir()
            
            elif command == "touch":
                if len(parts) < 2:
                    print("Нужно имя файла")
                else:
                    content = " ".join(parts[2:]) if len(parts) > 2 else ""
                    fm.create_file(parts[1], content)
            
            elif command == "cat":
                if len(parts) < 2:
                    print("Нужно имя файла")
                else:
                    fm.read_file(parts[1])
            
            elif command == "write":
                if len(parts) < 3:
                    print("Нужно имя файла и текст")
                else:
                    content = " ".join(parts[2:])
                    fm.write_file(parts[1], content)
            
            elif command == "rm":
                if len(parts) < 2:
                    print("Нужно имя файла")
                else:
                    fm.delete_file(parts[1])
            
            elif command == "cp":
                if len(parts) < 3:
                    print("Нужно указать источник и цель")
                else:
                    fm.copy_file(parts[1], parts[2])
            
            elif command == "mv":
                if len(parts) < 3:
                    print("Нужно указать источник и цель")
                else:
                    fm.move_file(parts[1], parts[2])
            
            elif command == "rename":
                if len(parts) < 3:
                    print("Нужно указать старое и новое имя")
                else:
                    fm.rename_file(parts[1], parts[2])
            
            elif command == "rmdir":
                if len(parts) < 2:
                    print("Нужно имя папки")
                else:
                    fm.delete_directory(parts[1])
            
            elif command == "info":
                fm.show_info()
            
            elif command == "env":
                fm.show_env()
            
            elif command in ("exit", "quit"):
                print("До свидания")
                break
            
            else:
                print("Неизвестная команда. Доступно: mkdir, ls, cd, pwd, touch, cat, write, rm, cp, mv, rename, rmdir, info, env, exit")
        
        except KeyboardInterrupt:
            print("\nВыход")
            break
        except Exception as e:
            print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()
