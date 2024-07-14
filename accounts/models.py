from django.db import models
from django.contrib.auth.models import User

# Create your models here.

USER_TYPE = (
    ('teacher','Teacher'),
    ('student','Student'),
)

class CustomUser(models.Model):
    user = models.OneToOneField(User,related_name='custom_user',on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10,choices=USER_TYPE)

    def __str__(self):
        return self.user.username
