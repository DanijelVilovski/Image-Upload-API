from django.db import models

from users.models import User

# Create your models here.
class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=80, blank=False, null=False)
    description = models.TextField(null=False, blank=True)
    image = models.ImageField(upload_to='images/')




