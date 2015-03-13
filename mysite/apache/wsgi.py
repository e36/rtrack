"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os, sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
sys.path.append('/usr/lib/python3.4/site-packages')
sys.path.append('/var/www/rtrack')
sys.path.append('/var/www/rtrack/mysite')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
