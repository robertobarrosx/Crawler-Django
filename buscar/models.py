# from django.contrib.postgres.fields import ArrayField
from django.db import models
# from django.contrib.postgres.fields import ArrayField

class Link(models.Model):
    url = models.URLField()
    # tags = ArrayField(models.CharField(max_length=200), blank=True)

    def __str__(self):
        return self.url