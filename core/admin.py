from django.contrib import admin
from .models import StudentRecord, PaymentRecord

# Register your models here.
admin.site.register(StudentRecord)
admin.site.register(PaymentRecord)