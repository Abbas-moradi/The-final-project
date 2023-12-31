from django.contrib.auth.models import BaseUserManager

"""
This custom manager allows you to create and manage user objects
in a more structured way, and it enforces the required fields 
for creating users and superusers.
"""

class UserManager(BaseUserManager):
    """ 
Creates and saves a User with the given email,and password. 
"""
    def create_user(self, phone_number, email, full_name, password):
        if not phone_number:
            raise ValueError('The phone is forgotten')
        
        if not email:
            raise ValueError('The email is forgotten')
        
        if not full_name:
            raise ValueError('The full name is forgotten')
        
        user = self.model(phone_number=phone_number, email=self.normalize_email(email), full_name=full_name)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self,phone_number, email, full_name, password):
        user = self.create_user(phone_number, email, full_name, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

