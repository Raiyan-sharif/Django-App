from django.db import models
from datetime import date
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password
from django.utils import timezone
# from accounts.models import ClubModel
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin, Permission, Group
)


USER_Type_CHOICE = (
    ('1', 'Player'),
    ('2', 'Club'),
    ('3', 'Governing body'),
    ('4', 'Admin')
)


GENDER_OPTION = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other')
)


MARITAL_STATUS=(
    (True, 'Yes'),
    (False, 'No')
)


class UserManager(BaseUserManager):

    def create_user(self, username, email=None, phone_number=None, password=None, is_staff=False, is_superuser=False,
                    is_active=True):
        if not username:
            raise ValueError("user must have a user name")
        if not password:
            raise ValueError("password can not be empty")

        user_obj = self.model(
            email=self.normalize_email(email),
            username=username,
            phone_number=phone_number
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.active = is_active
        user_obj.is_superuser = is_superuser
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, username, email=None, phone_number=None, password=None):
        user = self.create_user(
            username=username,
            email=email,
            phone_number=phone_number,
            password=password,
            is_staff=True
        )
        user.user_type = '3'
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, phone_number=None, password=None):
        user = self.create_user(
            username=username,
            email=email,
            phone_number=phone_number,
            password=password,
            is_superuser=True,
            is_staff=True
        )
        user.user_type = '4'
        user.save(using=self._db)
        return user


class UserModel(AbstractBaseUser, PermissionsMixin):
    username = models.CharField("user name", max_length=100, default='Anonymous', unique=True)
    email = models.EmailField("email", max_length=255, null=True, blank=True, unique=True)
    phone_number = models.CharField("phone number", max_length=20, unique=True)
    staff = models.BooleanField(default=False)
    is_club_auth = models.BooleanField(default=False)
    is_governing_body = models.BooleanField(default=False)
    is_player = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    joining_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    user_type = models.CharField("user type", max_length=2, default='1', choices=USER_Type_CHOICE)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone_number']

    objects = UserManager()

    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        super(UserModel, self).save(*args, **kwargs)

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.is_superuser

    @property
    def is_active(self):
        return self.active

    @is_active.setter
    def is_active(self, active):
        self.active = active

    @property
    def is_a_player(self):
        return self.is_player

    @property
    def is_club(self):
        return self.is_club_auth

    @property
    def profile(self):
        return PlayerModel.objects.get(user=self.pk)



class SuperUserModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)


class ClubModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    club_starting_date = models.DateField(default=date.today, blank=True, null=True)
    number_of_tables = models.PositiveIntegerField(default=1)
    profile_pic = models.ImageField(upload_to='user/', null=True, blank=True)
    is_valid = models.BooleanField(default=False)
    is_affiliated = models.BooleanField(default=False)
    address = models.TextField(null=False, blank=False)
    latitude = models.CharField(max_length=255, null=True, blank=True, default=None)
    longitude = models.CharField(max_length=255, null=True, blank=True, default=None)

    def __str__(self):
        return self.user.username


class PlayerModel(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, unique=True)
    date_of_birth = models.DateField(default=date.today, blank=True, null=True)
    nationality = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_OPTION, default="Male")
    profile_pic = models.ImageField(upload_to='user/', null=True, blank=True)
    marital_status = models.BooleanField(default=False, choices=MARITAL_STATUS)
    home_club = models.ForeignKey(ClubModel, on_delete=models.SET_NULL, null=True, blank=True)
    gameFrequency = models.PositiveIntegerField(default=0)
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username


class GoverningBody(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='user/', null=True, blank=True)
    root_parent = models.CharField(default='1', max_length=10, null=True, blank=True)

    def __str__(self):
        return self.user.username

