'''
This is where I keep my Django Registration Redux views
'''
from registration.backends.simple.views import RegistrationView
from . import settings

class MyRegistrationView(RegistrationView):
    success_url = 'tasklist'
