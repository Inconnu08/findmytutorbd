# Imports
from django.db import models

from reviews.choices import TEN_YEARS_DEGREES, TWELVE_YEARS_DEGREES


# Models
class Teacher(models.Model):
    full_name = models.CharField(max_length=225)
    code = models.CharField(max_length=50, blank=True, null=True)
    ten_years_degree = models.CharField(max_length=50, choices=TEN_YEARS_DEGREES, blank=True, null=True)
    twelve_years_degree = models.CharField(max_length=50, choices=TWELVE_YEARS_DEGREES, blank=True, null=True)
    undergraduate = models.CharField(max_length=80, blank=True, null=True)
    graduate = models.CharField(max_length=80, blank=True, null=True)
    phd = models.CharField(max_length=80, blank=True, null=True)
    verified = models.BooleanField(default=False)
    user = models.ForeignKey('User', blank=True, null=True, on_delete=models.CASCADE)
