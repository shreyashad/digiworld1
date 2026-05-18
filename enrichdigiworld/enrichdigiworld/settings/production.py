from .base import *

DEBUG = True

# ManifestStaticFilesStorage is recommended in production, to prevent
# outdated JavaScript / CSS assets being served from cache
# (e.g. after a Wagtail upgrade).
# See https://docs.djangoproject.com/en/5.2/ref/contrib/staticfiles/#manifeststaticfilesstorage
STORAGES["staticfiles"]["BACKEND"] = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"


ALLOWED_HOSTS = ["enrichdigiworld.com", "www.enrichdigiworld.com", '127.0.0.1', ]



STATIC_URL = "/static/"
STATIC_ROOT = "/home/shreyash/digiworld/digiworld1/static"

MEDIA_URL = "/media/"
MEDIA_ROOT = "/home/shreyash/digiworld/digiworld1/media"


SECRET_KEY ="_9vn6bgh+#bo^9p_fmy@1i9@d+i21wg781ljww-suobfxhn%72"

CSRF_TRUSTED_ORIGINS = [
    "https://enrichdigiworld.com",
    "https://www.enrichdigiworld.com",
]



try:
    from .local import *
except ImportError:
    pass
