# Create your models here.
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class UserManager(BaseUserManager):
    def create_user(self, email,first_name,city,last_name,password=None,password2=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            city=city
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,first_name,last_name, password=None):
        user = self.create_user(
            email,
            first_name,
            last_name=last_name,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='Email',max_length=255,unique=True) 
    first_name=models.CharField(max_length=20)
    last_name=models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    city=models.CharField(max_length=10)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Student(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)


class Product(models.Model):
    name=models.CharField(max_length=100)
    price=models.IntegerField()


class Cart(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    userid=models.IntegerField()

    def __str__(self):
        return self.product.name


class Person(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    city=models.CharField(max_length=100)
    age=models.IntegerField()