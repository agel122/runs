from django.db import models


class Run(models.Model):
    date = models.DateField()
    distance = models.DecimalField(max_digits=5, decimal_places=3)
    time = models.SmallIntegerField()

    def __str__(self):
        return str(self.distance)



