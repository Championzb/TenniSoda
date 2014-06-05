from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from court.models import Court
from city.models import City

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
    court = models.ForeignKey(Court, null=True,blank=True)
    city = models.ForeignKey(City, null=True, blank=True)
    first_name = models.CharField(max_length = 40, null=True,blank=True)
    last_name = models.CharField(max_length = 20, null=True,blank=True)
    birth_date = models.DateField(null=True,blank=True)
    level = models.CharField(max_length=15, null=True,blank=True)
    real_level = models.CharField(max_length=15, null=True,blank=True)
    ladder_points = models.IntegerField(null=True, blank=True)
    phone = models.CharField(max_length=11, null=True,blank=True)
    gender = models.CharField(max_length=2, null=True,blank=True)
    league_rank = models.IntegerField(null=True,blank=True)
    local_rank = models.IntegerField( null=True,blank=True)

    def __unicode__(self):
        username = self.user.email.split('@')[0]
        if self.last_name != '' and self.last_name is not None:
            username = self.last_name + " " +self.first_name
        return u" %s" % username

	
Account.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])
