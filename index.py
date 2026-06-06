import sys
import os

# Add the ecombabyshoppingproject subdirectory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'ecombabyshoppingproject'))

from django.core.wsgi import get_wsgi_application

# Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecombabyshoppingproject.settings')

# Expose the WSGI handler as 'app' for Vercel
app = get_wsgi_application()
