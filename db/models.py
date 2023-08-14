from django.db import models

# Create your models here.
class Electrify(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.CharField(max_length=100)
    date = models.DateField()
    units = models.IntegerField()
    unit = models.IntegerField()
    cost = models.IntegerField()

    def __str__(self):
        return self.name