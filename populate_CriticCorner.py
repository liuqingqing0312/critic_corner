import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'tango_with_django_project.settings')

import django
django.setup()
from CriticCorner.models import Movie, Review, UserProfile

# def populate():



