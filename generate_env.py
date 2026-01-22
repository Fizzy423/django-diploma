import secrets
import os

def generate_env():
    env_path = '.env'
    if os.path.exists(env_path):
        print("⚠️ Файл .env уже существует. Пропускаю генерацию.")
        return
    new_key = secrets.token_urlsafe(50)
    
    env_content = f"""# Настройки Django
DJANGO_SECRET_KEY='{new_key}'
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Настройки базы данных
DB_NAME=MyBD
DB_USER=postgres
DB_PASSWORD=твои_пароль_здесь
DATABASE_HOST=localhost
DATABASE_PORT=5432
"""
    
    with open(env_path, 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print("✅ Файл .env успешно создан!")
    print("📢 Теперь добавь его в .gitignore, чтобы не скомпрометировать секреты!")

if __name__ == "__main__":
    generate_env()