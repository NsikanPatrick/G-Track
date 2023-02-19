from email.policy import default
from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# The user model will be extended to accomodate profile photo
# {{user.userprofile.username}
#  
class UserProfile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    address = models.CharField(max_length=65, null=True, blank=True)
    phone = models.CharField(max_length=65, null=True, blank=True)
    privilege = models.CharField(max_length=50, null=True, blank=True)
    ip_address = models.CharField(max_length=50, null=True, blank=True)
    date_created = models.DateTimeField(default=timezone.now()) 
    last_seen = models.DateTimeField(default=timezone.now(), null=True, blank=True)
    profile_pic = models.FileField(null=True, blank=True, upload_to="uploads/profile_pictures", validators = [FileExtensionValidator(allowed_extensions=['jpg','jpeg','png'])])

    def __str__(self):
        return str(self.user)

# Extending the Users table to accomodate Debtors

class Debtor(models.Model):
    # client = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    client_id = models.IntegerField(blank=True, null=True)
    firstname = models.CharField(max_length=65, null=True, blank=True)
    surname = models.CharField(max_length=65, null=True, blank=True)
    address = models.CharField(max_length=65, null=True, blank=True)
    phone = models.CharField(max_length=65, null=True, blank=True)
    email = models.CharField(max_length=65, null=True, blank=True)
    amount_owed = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date_captured = models.DateTimeField(auto_now=True)
    due_date = models.DateField(null=True, blank=True)


class Payment(models.Model):
    debtor_id = models.IntegerField(blank=True, null=True)
    client_id = models.IntegerField(blank=True, null=True)
    medium_of_payment = models.CharField(max_length=65, null=True, blank=True)
    amount_payed = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    status = models.CharField(max_length=65, null=True, blank=True)
    balance_left = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date_payed = models.DateTimeField(auto_now=True)

