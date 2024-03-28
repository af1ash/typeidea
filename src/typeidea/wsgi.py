"""
WSGI config for typeidea project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.contrib.staticfiles.handlers import StaticFilesHandler
from django.core.wsgi import get_wsgi_application
from django.conf import settings

profile = os.environ.get("PROFILE", "develop")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"typeidea.settings.{profile}")

# When in production you never, ever put gunicorn in front. 
# Instead you use a server like nginx which dispatches requests 
# to a pool of gunicorn workers and also serves the static files.
if settings.WITH_STATIC:
    application = StaticFilesHandler(get_wsgi_application())
else:
    application = get_wsgi_application()
