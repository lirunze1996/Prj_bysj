# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.

class movie(models.Model):
    mid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    count = models.IntegerField()
    score = models.FloatField()

    class Meta:
        db_table = "movie"
