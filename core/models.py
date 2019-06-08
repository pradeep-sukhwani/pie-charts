from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from datetime import datetime

# Create your models here.

User = get_user_model()


class IdMapping(models.Model):
    name = models.CharField("Student Name", max_length=50, help_text='Name of the student')

    def __str__(self):
        return self.name


class Report(models.Model):
    students = models.ForeignKey(IdMapping, on_delete=models.SET_NULL, null=True, help_text='Select a Student')
    std = models.CharField("Result Standard", max_length=50, help_text='Define Standard/Class')
    year = models.PositiveSmallIntegerField("Passing Year", help_text='What was passing year', default=datetime.now().year)
    sci = models.FloatField("Science Marks", help_text='Define Science Marks',
                            validators=[MinValueValidator(0.0),
                                        MaxValueValidator(100.0)], default=0.0)
    math = models.FloatField("Maths Marks", help_text='Define Maths Marks',
                            validators=[MinValueValidator(0.0),
                                        MaxValueValidator(100.0)], default=0.0)
    language = models.FloatField("Language Marks", help_text='Define Language Marks',
                            validators=[MinValueValidator(0.0),
                                        MaxValueValidator(100.0)], default=0.0)
    social = models.FloatField("Social Marks", help_text='Define Social Marks',
                            validators=[MinValueValidator(0.0),
                                        MaxValueValidator(100.0)], default=0.0)
    total = models.FloatField("Total Marks Of Student", help_text='Define Total Marks',
                            validators=[MinValueValidator(0.0),
                                        MaxValueValidator(100.0)], default=0.0)
    grade = models.CharField("Grade As Per Result", max_length=5, help_text='Define Grade such as A, A+, etc')
    pass_fail = models.BooleanField("Pass Or Fail", help_text='Tick if the student is pass', default=True)

    def __str__(self):
        return "{year} - {std}".format(year=self.year, std=self.std)


class Login(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    allowed_ip = models.GenericIPAddressField("IP Address")

    def __str__(self):
        return self.user.username

    class Meta:
        pass
