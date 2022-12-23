from email.policy import default
from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User

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
