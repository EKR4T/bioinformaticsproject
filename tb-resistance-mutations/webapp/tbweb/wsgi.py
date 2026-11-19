import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tbweb.settings")

application = get_wsgi_application()
app = application  # Vercel's Python runtime looks for a variable named `app`
