from django.db import models

# Create your models here.

class Beer(models.Model):
    name = models.CharField(max_length=64)
    style = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"