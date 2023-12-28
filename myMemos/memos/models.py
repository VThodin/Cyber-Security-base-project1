
from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class Memo(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    memo = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.memo