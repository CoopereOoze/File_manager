"""
Файловый менеджер 
"""

import os
import shutil
from config import WORK_DIR

# Создаём рабочую директорию
os.makedirs(WORK_DIR, exist_ok=True)

def in_work_dir(path):
    """Проверка, что путь внутри рабочей директории"""
    return os.path.abspath(path).startswith(os.path.abspath(WORK_DIR))

current_dir = os.path.abspath(WORK_DIR)

print(f"Рабочая директория: {current_dir}")
print("Команды: mkdir, ls, cd, pwd, touch, cat, write, rm, cp, mv, rename, rmdir, exit\n")

while True:
    try:
        cmd = input(f"{os.path.basename(current_dir)}> ").strip()
        if not cmd:
            continue
        
        parts = cmd.split()
        command = parts[0]
        
        # Создание директории
        if command == "mkdir":
            if len(parts) < 2:
                print("Нужно имя папки")
                continue
            new_dir = os.path.join(current_dir, parts[1])
            try:
                os.mkdir(new_dir)
                print(f"Папка {parts[1]} создана")
            except FileExistsError:
                print(f"Папка {parts[1]} уже существует")
        
        # Перечисление файлов 
        elif command == "ls":
            target = current_dir
            if len(parts) > 1:
                target = os.path.abspath(os.path.join(current_dir, parts[1]))
                if not in_work_dir(target):
                    print("Выход за пределы рабочей директории запрещён")
                    continue
            
            if not os.path.exists(target):
                print("Путь не существует")
                continue
            
            # Обход
            for root, dirs, files in os.walk(target):
                for file in files:
                    print(os.path.join(root, file))
        
        # Смена директории
        elif command == "cd":
            if len(parts) < 2:
                print("Нужен путь")
                continue
            
            if parts[1] == "..":
                new_path = os.path.dirname(current_dir)
            else:
                new_path = os.path.abspath(os.path.join(current_dir, parts[1]))
            
            if not in_work_dir(new_path):
                print("Выход за пределы рабочей директории запрещён")
            elif os.path.isdir(new_path):
                current_dir = new_path
            else:
                print("Не директория")
        
        # Показать текущий путь
        elif command == "pwd":
            print(current_dir)
        
        # Создание файла
        elif command == "touch":
            if len(parts) < 2:
                print("Нужно имя файла")
                continue
            file_path = os.path.join(current_dir, parts[1])
            if os.path.exists(file_path):
                print("Файл уже существует")
            else:
                open(file_path, 'w').close()
                print(f"Файл {parts[1]} создан")
        
        # Чтение файла
        elif command == "cat":
            if len(parts) < 2:
                print("Нужно имя файла")
                continue
            file_path = os.path.join(current_dir, parts[1])
            if os.path.isfile(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    print(f.read())
            else:
                print("Файл не найден")
        
        # Запись в файл
        elif command == "write":
            if len(parts) < 3:
                print("Нужно имя файла и текст")
                continue
            file_path = os.path.join(current_dir, parts[1])
            content = " ".join(parts[2:])
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Записано в {parts[1]}")
        
        # Удаление файла
        elif command == "rm":
            if len(parts) < 2:
                print("Нужно имя файла")
                continue
            file_path = os.path.join(current_dir, parts[1])
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Файл {parts[1]} удалён")
            else:
                print("Файл не найден")
        
        # Копирование файла
        elif command == "cp":
            if len(parts) < 3:
                print("Нужно указать источник и цель")
                continue
            src = os.path.join(current_dir, parts[1])
            dst = os.path.join(current_dir, parts[2])
            if os.path.isfile(src):
                shutil.copy(src, dst)
                print(f"Скопировано {parts[1]} -> {parts[2]}")
            else:
                print("Источник не файл")
        
        # Перемещение файла
        elif command == "mv":
            if len(parts) < 3:
                print("Нужно указать источник и цель")
                continue
            src = os.path.join(current_dir, parts[1])
            dst = os.path.join(current_dir, parts[2])
            if os.path.exists(src):
                shutil.move(src, dst)
                print(f"Перемещено {parts[1]} -> {parts[2]}")
            else:
                print("Источник не найден")
        
        # Переименование
        elif command == "rename":
            if len(parts) < 3:
                print("Нужно указать старое и новое имя")
                continue
            old = os.path.join(current_dir, parts[1])
            new = os.path.join(current_dir, parts[2])
            if os.path.exists(old):
                os.rename(old, new)
                print(f"Переименовано {parts[1]} -> {parts[2]}")
            else:
                print("Файл не найден")
        
        # Удаление директории
        elif command == "rmdir":
            if len(parts) < 2:
                print("Нужно имя папки")
                continue
            dir_path = os.path.join(current_dir, parts[1])
            if os.path.isdir(dir_path):
                shutil.rmtree(dir_path)
                print(f"Папка {parts[1]} удалена")
            else:
                print("Не директория или не существует")
        
        elif command in ("exit", "quit"):
            print("До свидания")
            break
        
        else:
            print("Неизвестная команда. Доступно: mkdir, ls, cd, pwd, touch, cat, write, rm, cp, mv, rename, rmdir, exit")
    
    except KeyboardInterrupt:
        print("\nВыход")
        break
    except Exception as e:
        print(f"Ошибка: {e}")
