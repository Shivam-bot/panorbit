from enum import unique, Enum

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.hashers import make_password
from django.dispatch import receiver
from django.db.models.signals import post_save
from panorbitapp.validators import CustomValidations as Vldtsr
from .custom_function import *


# Create your models here.

# Unique decorator so we make sure no value is getting repeated


@unique
class GenderEnum(Enum):
    Male = "M"
    Female = "F"
    TransGender = "T"
    NotToDisclose = "N"

    @classmethod
    def gender_choices(cls):
        return [(gender.value, gender.name) for gender in cls]


@unique
class OTPChoiceEnum(Enum):
    Email = "email"
    Mobile = "mobile"

    @classmethod
    def otp_verification_choices(cls):
        return [(otp.value, otp.name) for otp in cls]


@unique
class ContinentEnum(Enum):
    ASIA = 'Asia'
    EUROPE = 'Europe'
    NORTH_AMERICA = 'North America'
    AFRICA = 'Africa'
    OCENIA = 'Oceania'
    ANTARTICA = 'Antartica'
    SOUTH_AMERICA = 'South America'

    @classmethod
    def continent_choices(cls):
        return [(continent.value, continent.name) for continent in cls]


@unique
class IsOfficialEnum(Enum):
    T="T"
    F="F"

    @classmethod
    def is_offocial_choices(cls):
        return [(offocial_choices.value, offocial_choices.name) for offocial_choices in cls]


class CustomUser(AbstractUser):
    email = models.EmailField(max_length=200, primary_key=True, validators=[Vldtsr.validate_name])
    first_name = models.CharField(max_length=50, error_messages=" first name cannot be null",
                                  validators=[Vldtsr.validate_name])
    last_name = models.CharField(max_length=50, error_messages=" last name cannot be null",
                                 validators=[Vldtsr.validate_name])
    gender = models.CharField(choices=GenderEnum.gender_choices(), max_length=1, default="N")
    mob_no = models.BigIntegerField(validators=[Vldtsr.validate_mobile_number])
    email_verified = models.BooleanField(default=False)
    mob_verified = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    modified_date = models.DateTimeField(auto_now=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "custom_user"

    def __str__(self):
        return self.email


class UserOTP(models.Model):
    object = None
    user_otp_id = models.AutoField(primary_key=True)
    request_for = models.CharField(max_length=6, choices=OTPChoiceEnum.otp_verification_choices())
    otp = models.TextField()
    user = models.ForeignKey(CustomUser, related_name="user", on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "usr_otp"
        unique_together = ('request_for', 'user')

    def save(self, *args, **kwargs):
        self.otp = make_password(self.otp)
        return super(UserOTP, self).save(*args, **kwargs)


@receiver(post_save, sender=CustomUser)
def send_otp(sender, instance, created, **kwargs):
    if created:
        print(sender.email, "fghjkolijh")
        print(instance.email, "bhjkjhb")
        otp = str(random_number(0000, 9999))
        send_email("Panorbit Email Verification ", f"Email verification code is : {otp} ", instance.email)

        UserOTP.objects.create(otp=otp, request_for="email", user=instance)


class Country(models.Model):
    objects = None
    code = models.CharField(primary_key=True, max_length=3)
    name = models.CharField(max_length=52, null=False)
    continent = models.CharField(choices=ContinentEnum.continent_choices(), max_length=15, default='Asia')
    region = models.CharField(max_length=26, null=True, blank=True)
    surface_area = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    indep_year = models.SmallIntegerField(null=True)
    population = models.IntegerField(default=0)
    life_expectancy = models.DecimalField(max_digits=3, decimal_places=1, default=0,null=True)
    gnp = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    gnp_old = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    local_name = models.CharField(max_length=45, blank=True)
    government_form = models.CharField(max_length=45, blank=True)
    head_of_state = models.CharField(max_length=60, null=True)
    capital = models.IntegerField(null=True)
    code_2 = models.CharField(max_length=2, blank=True)

    class Meta:
        db_table = 'country'

    def __str__(self):
        return self.code


class City(models.Model):

    objects = None
    city_id = models.AutoField(primary_key= True)
    name = models.CharField(max_length=35, null=False, blank=True)
    country_code = models.ForeignKey(Country,related_name='city',on_delete=models.CASCADE, blank=True)
    district = models.CharField(max_length=20, null=False, blank=True)
    population = models.IntegerField(null=False, default=0)

    class Meta:
        db_table = 'city'

    def __int__(self):
        return self.city_id


class CountryLanguage(models.Model):

    objects = None
    country_code = models.ForeignKey(Country,related_name='language',on_delete=models.CASCADE, blank=True)
    language = models.CharField(max_length=30, null=False, blank=True)
    is_official = models.BooleanField(default=False)
    percentage = models.DecimalField(max_digits=4, decimal_places=1, null=False, default=0.0)

    class Meta:
        db_table = 'country_language'
        unique_together = ('country_code','language' )
        managed = True

    def __str__(self):
        return f"{self.country_code}: {self.language}"

