import os
import sys
from pathlib import Path
from urllib.parse import urlsplit

import dj_database_url
from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

IS_COLLECTSTATIC = "collectstatic" in sys.argv[1:]
DEBUG = os.environ.get("DJANGO_DEBUG", "False").lower() in {"true", "1", "yes"}
SECRET_KEY = (
    os.environ.get("DJANGO_SECRET_KEY") or os.environ.get("SECRET_KEY") or ""
).strip()
if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = "local-development-only-secret-key"
    elif IS_COLLECTSTATIC:
        SECRET_KEY = "collectstatic-build-only-key"
    else:
        raise ImproperlyConfigured(
            "Set DJANGO_SECRET_KEY or SECRET_KEY in the environment when DJANGO_DEBUG is False."
        )
if not DEBUG and SECRET_KEY in {
    "local-development-only-change-before-deployment",
    "local-development-only-secret-key",
}:
    raise ImproperlyConfigured("Replace the example DJANGO_SECRET_KEY before production.")
ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
    if host.strip()
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "catalog",
    "tracker",
    "social",
    "contact",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASE_URL = os.environ.get("DATABASE_URL", "").strip()
if not DEBUG and not DATABASE_URL and not IS_COLLECTSTATIC:
    raise ImproperlyConfigured(
        "DATABASE_URL must be set in production. Configure a persistent database; "
        "the Heroku filesystem is not persistent."
    )
if (
    not DEBUG
    and DATABASE_URL
    and urlsplit(DATABASE_URL).scheme.lower() not in {"postgres", "postgresql"}
):
    raise ImproperlyConfigured(
        "Production DATABASE_URL must use PostgreSQL. Configure the Neon or Heroku "
        "PostgreSQL connection URL."
    )

default_database_name = (
    "static-build.sqlite3" if IS_COLLECTSTATIC else "db.sqlite3"
)
database_url = DATABASE_URL or f"sqlite:///{(BASE_DIR / default_database_name).as_posix()}"
DATABASES = {
    "default": dj_database_url.parse(
        database_url,
        conn_max_age=600,
        ssl_require=database_url.lower().startswith(("postgres://", "postgresql://")),
    ),
}

CSRF_TRUSTED_ORIGINS = [
    origin.strip().rstrip("/")
    for origin in os.environ.get(
        "CSRF_TRUSTED_ORIGINS",
        "https://*.herokuapp.com,https://*.codeinstitute-ide.net",
    ).split(",")
    if origin.strip()
]

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "catalog:anime_list"
LOGOUT_REDIRECT_URL = "catalog:anime_list"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_REFERRER_POLICY = "same-origin"
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31_536_000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
