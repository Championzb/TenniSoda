from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from court.models import Court


# Create your models here.

class AccountManager(BaseUserManager):
    def create_user(self, email, password=None):
        """

        Creates and saves a User with the given email and password
        :param email:
        :param password:
        :return:
        """
        if not email:
            raise ValueError('You must provide an email address')

        user = self.model(
            email=self.normalize_email(email),
        )


        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """

        Creates and saves a superuser with the email and password.
        :param email:
        :param password:
        :return:
        """
        user = self.create_user(email, password=password,)
        user.is_admin = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        db_index=True,
    )
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class Profile(models.Model):
    user = models.OneToOneField(Account,primary_key=True)
    court = models.ForeignKey(Court)
    first_name = models.CharField(max_length = 40)
    last_name = models.CharField(max_length = 20)
    birth_date = models.DateField(blank=True, null=True)
    level = models.CharField(max_length=15)
    real_level = models.CharField(max_length=15)
    ladder_points = models.IntegerField()
    phone = models.CharField(max_length=11)
    gender = models.CharField(max_length=2)
    city = models.CharField(max_length=3)
    league_rank = models.IntegerField()
    local_rank = models.IntegerField()

    def __unicode__(self):
        return self.first_name + self.last_name

	
Account.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])
