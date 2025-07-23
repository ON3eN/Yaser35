from pathlib import Path
import os
import cloudinary  # ✅ ضروري للتهيئة اليدوية

# المسار الأساسي للمشروع
BASE_DIR = Path(__file__).resolve().parent.parent

# الأمان
SECRET_KEY = 'django-insecure-m@4=mmn-d%#vgtpw@lkeg%)m40l0awa8v223)vj_3k)r($+i)4'
DEBUG = True
ALLOWED_HOSTS = []

# التطبيقات المثبتة
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # التطبيقات الخاصة بالمشروع
    'store',
    'order',
    'account',
    'cart',

    # Cloudinary
    'cloudinary',
    'cloudinary_storage',
]

# وسائط المعالجة
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Yaser35.urls'

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

WSGI_APPLICATION = 'Yaser35.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'ar-sa'
TIME_ZONE = 'Asia/Riyadh'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dehrixr6p',
    'API_KEY': '459857656957381',
    'API_SECRET': 'UX16iTpfmfXdqaMCp8i4lrLE0Ro'
}

cloudinary.config(
    cloud_name='dehrixr6p',
    api_key='459857656957381',
    api_secret='UX16iTpfmfXdqaMCp8i4lrLE0Ro'
)

# ✅ إعدادات الإيميل لإرسال الرسائل من Gmail
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'goto6946@gmail.com'  # بريدك
EMAIL_HOST_PASSWORD = 'vbyh gyec rfdo jnae'  # كلمة مرور التطبيق أو كلمة المرور العادية (لو ما عندك تحقق بخطوتين)

# يمكنك استخدام هذا للإرسال مثل:
# send_mail('العنوان', 'النص', EMAIL_HOST_USER, ['to@example.com'])

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# المفتاح الافتراضي
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
