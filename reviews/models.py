# Imports
from django.db import models

from reviews.choices import TEN_YEARS_DEGREES, TWELVE_YEARS_DEGREES, UNIVERSITIES, DEPARTMENTS


# Models
class Teacher(models.Model):
    user = models.ForeignKey('User', blank=True, null=True, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=225)
    code = models.CharField(max_length=80, blank=True, null=True)
    ten_years_degree = models.CharField(max_length=80, choices=TEN_YEARS_DEGREES, blank=True, null=True)
    twelve_years_degree = models.CharField(max_length=80, choices=TWELVE_YEARS_DEGREES, blank=True, null=True)
    undergraduate_degree = models.CharField(max_length=80, blank=True, null=True)
    graduate_degree = models.CharField(max_length=80, blank=True, null=True)
    phd_degree = models.CharField(max_length=80, blank=True, null=True)
    is_professor = models.BooleanField(default=False)
    is_tutor = models.BooleanField(default=False)
    university = models.CharField(max_length=80, choices=UNIVERSITIES, blank=True, null=True)
    department = models.CharField(max_length=80, choices=DEPARTMENTS, blank=True, null=True)
    courses = models.ManyToManyField(Course, related_name="professor_subjects", blank=True, null=True)
    verified = models.BooleanField(default=False)

    def __unicode__(self):
        return self.full_name

    class Meta:
        unique_together = ('fullname', 'code', 'department', 'university')
