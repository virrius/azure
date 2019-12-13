from django.db import models


class Wait_task(models.Model):   
    name = models.CharField(max_length=50, unique=True)
    time_to_wait = models.PositiveSmallIntegerField(default = 5)

    def __str__(self):
        return self.name
