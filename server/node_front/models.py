from django.db import models


class Wait_task(models.Model):   
    uid = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    time_to_wait = models.PositiveSmallIntegerField(default = 5)

    def __str__(self):
        return self.name

class Result(models.Model):
    uid = models.CharField(max_length=100)
    name = models.CharField(max_length=50)
    body = models.CharField(max_length=1000)