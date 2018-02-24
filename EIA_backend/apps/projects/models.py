from django.db import models

# Create your models here.


class Projects(models.Model):
    name=models.CharField(max_length=50)
    unit = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.name