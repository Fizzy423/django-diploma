import os
from pathlib import Path

# Путь к проекту
BASE_DIR = Path(__file__).resolve().parent.parent

# --- 1. ОСНОВНЫЕ НАСТРОЙКИ БЕЗОПАСНОСТИ ---
# В продакшене SECRET_KEY должен быть в переменных окружения
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-zb^z$h#$-h_c&hv6t_&97@+(=#onp^hv6*k4n$r=xo^&h8k=57')

DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

# В список ALLOWED_HOSTS нужно добавить домен вашего сервера при деплое
ALLOWED_HOSTS = ['*']


# --- 2. ПРИЛОЖЕНИЯ ---
INSTALLED_APPS = [
    'dal',             # Должен быть выше django.contrib.admin
    'dal_select2',     # Должен быть выше django.contrib.admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Сторонние библиотеки
    'crispy_forms',
    'crispy_bootstrap5',
    'django_filters',
    'guardian',
    'widget_tweaks',

    # Ваше приложение
    'main_app',
]


# --- 3. MIDDLEWARE ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ВОТ ЭТА СТРОКА
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # Защита от Clickjacking
]

ROOT_URLCONF = 'abiturient_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'abiturient_project.wsgi.application'


# --- 4. БАЗА ДАННЫХ (PostgreSQL) ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'MyBD',
        'USER': 'postgres',
        'PASSWORD': '1', # Смените на сложный пароль в продакшене!
        'HOST': os.environ.get('DATABASE_HOST', 'localhost'), # По умолчанию localhost, но в докере будет 'db'
        'PORT': '5432',
        'OPTIONS': {
            'client_encoding': 'UTF8',
        }
    }
}


# --- 5. ПАРОЛИ И АВТОРИЗАЦИЯ ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
)

# Перенаправления
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'


# --- 6. ЛОКАЛИЗАЦИЯ ---
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True


# --- 7. СТАТИКА И МЕДИА ---
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
# STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Ограничение размера файла (10 МБ), защита от переполнения диска
DATA_UPLOAD_MAX_MEMORY_SIZE = 10485760 


# --- 8. НАСТРОЙКИ БЕЗОПАСНОСТИ ДЛЯ ПРОДАКШЕНА (SSL/Cookies) ---
# Эти настройки активируются автоматически при DEBUG = False
if not DEBUG:
    # 1. Защита Cookies
    SESSION_COOKIE_SECURE = True       # Куки сессии только через HTTPS
    CSRF_COOKIE_SECURE = True          # CSRF-токен только через HTTPS
    SESSION_COOKIE_HTTPONLY = True     # Запрет доступа JS к кукам сессии
    CSRF_COOKIE_HTTPONLY = True

    # 2. Защита от XSS и сниффинга
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True

    # 3. HSTS и SSL редирект
    SECURE_SSL_REDIRECT = True         # Авто-редирект с http на https
    SECURE_HSTS_SECONDS = 31536000     # 1 год (строгое использование https)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    # 4. Защита от встраивания в iframe (Clickjacking)
    X_FRAME_OPTIONS = 'DENY'           # Полный запрет встраивания сайта в чужие окна


# --- 9. ПРОЧЕЕ ---
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'