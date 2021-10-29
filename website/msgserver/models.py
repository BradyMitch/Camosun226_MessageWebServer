from django.db import models

# Create your models here.
class Message(models.Model):
    key = models.CharField(max_length=8)
    msg = models.CharField(max_length=120)

    def __str__(self):
        return '(' + str(self.key) + ',' + str(self.msg) + ')'
