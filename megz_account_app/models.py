from django.db import models
from django.contrib.auth.forms import User

# Create your models here.

class Accounts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    reason = models.TextField()
    amount = models.FloatField()

    def __str__(self):
        return self.reason
