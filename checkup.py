import subprocess
import os
from datetime import datetime

def run_command(command, description):
    print(f"\n--- ⚙️ {description} ---")
    try:
        result = subprocess.run(["python", "manage.py"] + command, check=True, text=True)
        print(f"✅ Успешно: {description}")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Ошибка во время: {description}")
        return False

def create_backup():
    print("\n--- 💾 Создание бэкапа базы данных ---")
    if not os.path.exists('backups'):
        os.makedirs('backups')
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"backups/db_backup_{timestamp}.json"
    
    try:
        with open(backup_file, 'w', encoding='utf-8') as f:
            subprocess.run(["python", "manage.py", "dumpdata", "--exclude", "auth.permission", "--exclude", "contenttypes"], stdout=f, check=True)
        print(f"✅ Бэкап сохранен в: {backup_file}")
    except Exception as e:
        print(f"❌ Не удалось создать бэкап: {e}")

def main():
    print(f"🚀 Запуск полной проверки проекта: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if not run_command(["check"], "Системная проверка Django"):
        return

    if not run_command(["makemigrations", "--check", "--dry-run"], "Проверка пропущенных миграций"):
        print("⚠️ У тебя есть изменения в моделях, которые не отражены в миграциях!")

    run_command(["test"], "Запуск тестов")

    create_backup()

    print("\n🌟 Проверка завершена!")

if __name__ == "__main__":
    main()