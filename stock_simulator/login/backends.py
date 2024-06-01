# backends.py

from django.contrib.auth.backends import BaseBackend
from members.models import Customer

class CustomBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = Customer.objects.get(account=username)
            if user.check_password(password):
                return user
        except Customer.DoesNotExist:
            return None
    
    def get_user(self, user_id):
        try:
            return Customer.objects.get(pk=user_id)
        except Customer.DoesNotExist:
            return None
