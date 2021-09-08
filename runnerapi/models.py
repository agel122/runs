from django.db import models
from django.contrib.auth.models import User


class Run(models.Model):
    date = models.DateField()
    distance = models.DecimalField(max_digits=5, decimal_places=3)
    time = models.SmallIntegerField()
    owner = models.ForeignKey(User, related_name='runs', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.distance)



