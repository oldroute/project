# -*- coding: utf-8 -*-
import os

DEBUG = False
ALLOWED_HOSTS = ["*", ]

LANGUAGE_CODE = 'ru-ru'
PYTHON_PATH = os.path.join(os.sep, 'usr', 'local', 'bin', 'python3.6')
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
TMP_DIR = os.path.join(MEDIA_ROOT, "tmp")

MEDIA_URL = '/media/'
STATIC_URL = '/static/'
ROOT_URLCONF = 'project.urls'
WSGI_APPLICATION = 'project.wsgi.application'

STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, 'project', 'static'),
]
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_ROOT, 'project', 'templates'), ],
        'APP_DIRS': False,
        'OPTIONS': {
            'debug': DEBUG,
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                'django.template.loaders.eggs.Loader',
            ],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
             ],
         }
    },
]

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'project.profile',
    'tinymce',
    'mptt',
    'adminsortable2',
    'project',
    'project.sources',
    'project.courses',
    'project.executors',
    'project.groups',
    'project.modules',
    'project.news',
    'project.tasks',
    'project.training',
    'project.langs',
)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'project.middleware.LoginRequiredMiddleware',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': "pt",
    }
}

SESSION_COOKIE_AGE = 4 * 60 * 60
SESSION_SAVE_EVERY_REQUEST = True

# Настройки tinymce
TINYMCE_DEFAULT_CONFIG = {
    'plugins': 'spellchecker',
    'theme_advanced_buttons1':
        'undo,redo,|,bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,|,'
        'bullist,numlist,blockquote,|,formatselect,|,fontsizeselect,|,forecolor,backcolor,|,'
        'removeformat,|,code',
    'width': '100%',
    'height': 100,
    'theme_advanced_resizing': 'True',
    'extended_valid_elements ': '*[*]',
    'content_style': '.mcecontentbody{font-size:14px;}',
}


SITE_ID = 1
# EMAIL_HOST = 'smtp.yandex.ru'
# EMAIL_PORT = 465
# EMAIL_HOST_USER = 'mailUser'
# EMAIL_HOST_PASSWORD = 'pass'
# EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = 'info@cappa.ru'
