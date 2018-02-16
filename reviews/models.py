# Imports
import math

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Sum
from django.db.models.signals import m2m_changed
from django.urls import reverse
from django.utils import timezone

from reviews.choices import TEN_YEARS_DEGREES, TWELVE_YEARS_DEGREES, UNIVERSITIES, DEPARTMENTS, grade_dict_int_key, \
    grade_dict_str_key, SCORE_CHOICES, GRADE_CHOICES


# Models
class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=5, unique=True)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=225)
    code = models.CharField(max_length=225, blank=True, null=True)
    ten_years_degree = models.CharField(max_length=225, choices=TEN_YEARS_DEGREES, blank=True, null=True)
    twelve_years_degree = models.CharField(max_length=225, choices=TWELVE_YEARS_DEGREES, blank=True, null=True)
    undergraduate_degree = models.CharField(max_length=225, blank=True, null=True)
    graduate_degree = models.CharField(max_length=225, blank=True, null=True)
    phd_degree = models.CharField(max_length=225, blank=True, null=True)
    is_professor = models.BooleanField(default=False)
    is_tutor = models.BooleanField(default=False)
    university = models.CharField(max_length=225, choices=UNIVERSITIES, blank=True, null=True)
    department = models.CharField(max_length=225, choices=DEPARTMENTS, blank=True, null=True)
    courses = models.ManyToManyField(Course, related_name="professor_subjects", blank=True)
    verified = models.BooleanField(default=False)

    # Rating and review related fields
    number_of_reviews = models.IntegerField(default=0)

    # These are all averages
    easiness = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        default=0.0,
        blank=True,
        null=True
    )
    clarity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        default=0.0,
        blank=True,
        null=True
    )
    helpfulness = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        default=0.0,
        blank=True,
        null=True
    )
    overall = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        default=0.0,
        blank=True,
        null=True
    )

    # Grade fields
    number_of_grades = models.IntegerField(default=0, blank=True, null=True)
    average_grade = models.CharField(max_length=3, default='N/A', blank=True, null=True)

    def __str__(self):
        if self.university:
            return self.full_name + ' - ' + self.university
        else:
            return self.full_name

    def get_pk(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        self.slug = self.full_name.lower().replace(' ', '-')

        if self.pk:
            # Only hits DB if the teacher exists
            professor_reviews = Review.objects.filter(professor=self)
            self.number_of_reviews = professor_reviews.count()
            if not self.number_of_reviews == 0:  # Only calculate if there is at least one review
                # Reviews for this professor exists
                # Calculating the averages and overall
                self.easiness = float(professor_reviews.aggregate(Sum('easiness'))['easiness__sum']) / float(
                    self.number_of_reviews)
                self.clarity = float(professor_reviews.aggregate(Sum('clarity'))['clarity__sum']) / float(
                    self.number_of_reviews)
                self.helpfulness = float(professor_reviews.aggregate(Sum('helpfulness'))['helpfulness__sum']) / float(
                    self.number_of_reviews)
                get_overall_rating(self.easiness, self.clarity, self.helpfulness)

                # Setting up the average grades
                self.number_of_grades = professor_reviews.aggregate(Sum('is_proper_grade'))['is_proper_grade__sum']
                if self.number_of_grades > 0:  # Only calculate grade if at least one proper grade has been given out.
                    self.average_grade = grade_dict_int_key[
                        int(math.ceil(
                            float(professor_reviews.aggregate(Sum('grade_as_a_number'))[
                                      'grade_as_a_number__sum']) / float(self.number_of_grades)
                        ))
                    ]

        super(Teacher, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('reviews:professor_detail', kwargs={
            'pk': str(self.pk),
            'slug': str(self.slug),
        })

    def __unicode__(self):
        return self.full_name

    class Meta:
        unique_together = ('full_name', 'code', 'department', 'university')
        ordering = ('full_name',)


def get_overall_rating(easiness, clarity, helpfulness):
    pass


class Tag(models.Model):
    """
    The data model used to represent tags which describe professors.
    """
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Review(models.Model):
    """
    The data model used to represent reviews.
    """
    author = models.ForeignKey(User, related_name='user_reviews', on_delete=models.SET_NULL, blank=True, null=True)
    professor = models.ForeignKey(Teacher, related_name='professor_reviews', on_delete=models.DO_NOTHING, null=False)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)
    text = models.TextField(max_length=600, blank=False)

    # The rating fields
    easiness = models.IntegerField(default=3, choices=SCORE_CHOICES)
    clarity = models.IntegerField(default=3, choices=SCORE_CHOICES)
    helpfulness = models.IntegerField(default=3, choices=SCORE_CHOICES)
    overall = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        default=3.0,
    )

    # Grading related fields
    grade = models.CharField(max_length=3, choices=GRADE_CHOICES, default='N/A')
    is_proper_grade = models.IntegerField(
        default=0,
        validators=[
            MaxValueValidator(1),  # 1 if grade is NOT N/A
            MinValueValidator(0)  # 0 otherwise
        ]
    )
    grade_as_a_number = models.IntegerField(default=0)  # Hidden, used for calculations

    # Tags
    tags = models.ManyToManyField(Tag, related_name='review_tags', blank=False)

    # Vote field(s)
    votes = models.IntegerField(default=0)

    class Meta:
        unique_together = [('author', 'professor')]
        ordering = ('votes', '-updated',)

    def __str__(self):
        return 'Professor - ' + self.professor.full_name + ', Author - ' + self.author.username + ', Rating - ' + str(
            self.overall)

    def save(self, *args, **kwargs):
        # Calculating the overall
        get_overall_rating(self.easiness, self.clarity, self.helpfulness)
        # Setting the grade fields
        if not self.grade == 'N/A':
            self.is_proper_grade = 1
        else:
            self.is_proper_grade = 0
        self.grade_as_a_number = grade_dict_str_key[self.grade]

        if self.pk:
            # Update only
            self.updated = timezone.now()
        super(Review, self).save(*args, **kwargs)
        # Calling the professor's save method after super
        self.professor.save()


# Limiting the max number of tags to 3 for every review
def tags_changed(sender, **kwargs):
    if kwargs['instance'].tags.count() > 3:
        raise ValidationError("You cannot assign more than 3 tags to one review.")


m2m_changed.connect(tags_changed, sender=Review.tags.through)


class Vote(models.Model):
    """
    The data model is used to determine which user found which reviews
    helpful.
    """
    user = models.ForeignKey(User, related_name='user_votes', on_delete=models.SET_NULL, blank=True, null=True)
    review = models.ForeignKey(Review, related_name='review_votes', on_delete=models.SET_NULL, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = [('user', 'review')]

    def __str__(self):
        return self.user.username + ' - ' + str(self.review.id)
