import subprocess
import sys
import re

def get_latest_version(package_name):
    """
    Запрашивает у PyPI самую последнюю версию.
    """
    print(f"📡 Проверяю {package_name}...")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "index", "versions", package_name],
            capture_output=True, text=True, timeout=5
        )
        match = re.search(r"LATEST:\s+([\d.]+)", result.stdout)
        if match:
            return match.group(1)
    except Exception:
        pass
    return None

def run_security_audit():
    """
    Проверяет установленные пакеты на наличие известных уязвимостей.
    """
    print("\n🛡️ Запускаю аудит безопасности (pip-audit)...")
    try:
        subprocess.run(["pip-audit", "--version"], capture_output=True, check=True)
        
        result = subprocess.run(["pip-audit", "-r", "requirements.txt"], text=True)
        
        if result.returncode == 0:
            print("✅ Уязвимостей не обнаружено.")
        else:
            print("⚠️ Внимание! В ваших библиотеках найдены уязвимости.")
            
    except FileNotFoundError:
        print("ℹ️ pip-audit не установлен. Пропускаю проверку.")
        print("💡 Чтобы включить аудит, выполни в терминале: pip install pip-audit")

def update_requirements(file_path='requirements.txt'):
    new_lines = []
    updated_count = 0

    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                new_lines.append(line)
                continue

            if '==' in line:
                name, current_version = line.split('==')
                latest_version = get_latest_version(name)

                if latest_version and latest_version != current_version:
                    print(f"✨ Найдено: {name} ({current_version} -> {latest_version})")
                    new_lines.append(f"{name}=={latest_version}")
                    updated_count += 1
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)

        with open(file_path, 'w') as f:
            f.write('\n'.join(new_lines) + '\n')

        print(f"\n✅ Готово! Файл обновлен. Записей: {updated_count}")

    except FileNotFoundError:
        print(f"❌ Ошибка: Файл {file_path} не найден.")

if __name__ == "__main__":
    update_requirements()
    
    run_security_audit()
    
    print("\n🚀 Теперь можно выполнить: pip install -r requirements.txt")