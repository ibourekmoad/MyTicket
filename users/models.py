from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('engineer', 'Engineer'),
        ('customer', 'Customer')
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_engineer(self):
        return self.role == 'engineer'

    @property
    def is_customer(self):
        return self.role == 'customer'
