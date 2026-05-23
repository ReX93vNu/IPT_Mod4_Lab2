from django.db import models
from django.contrib.auth.models import User
from cryptography.fernet import Fernet

FERNET_KEY = b'L7z_uTf1hA6F3rV-A5_pS-7YqP8H_rJ9Yp4q1VwY8s0='
cipher = Fernet(FERNET_KEY)

class StudentRecord(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    course = models.CharField(max_length=50)
    year_level = models.IntegerField()

    def __str__(self):
        return self.full_name


class PaymentRecord(models.Model):
    user_name = models.CharField(max_length=100)
    card_number = models.CharField(max_length=255) # has to be long

    def save(self, *args, **kwargs):
        if not self.card_number.startswith('gAAAAA'):
            encrypted_bytes = cipher.encrypt(self.card_number.encode('utf-8'))
            self.card_number = encrypted_bytes.decode('utf-8')
            
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"Payment by {self.user_name}"