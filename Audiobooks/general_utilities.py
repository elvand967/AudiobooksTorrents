# D:\Python\django\AudiobooksTorrents\Audiobooks\general_utilities.py
# Служебные утилиты
import json
import os
from django import setup


# Устанавливаем переменную окружения, указывающую Django, в каком проекте искать настройки
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Audiobooks.settings")

# Настраиваем Django
setup()

import sys
sys.path.append("/")

from datetime import datetime
import shutil





def main():
    print(f"{' Резервное копирование базы данных ':.^50}\n")
    stop = input('Для продолжения нажмите любую клавишу,\nдля остановки нажмите "Q" ')
    if stop.upper() == "Q" or stop.upper() == "Й":
        return
    # Резервная копия Базы данных
    database_backup()




    pass


def database_backup():
    # Генерировать имя резервной копии с использованием даты и времени
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f'folder_files\\backup_folder\\db_backup_{timestamp}.sqlite3'
    try:
        # Создать резервную копию
        shutil.copy('db.sqlite3', backup_file)
        print(f'Создана резервная копия: {backup_file}')
    except Exception as e:
        print(f'Ошибка при создании резервной копии: {e}')



if __name__ == "__main__":
    main()