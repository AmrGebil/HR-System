from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

class Group(models.Model):
    name= models.CharField(max_length=15,default='Employee')

    def __str__(self):
        return self.name


class EmployeeManager(BaseUserManager):
    def create_user(self,name,email,group,password=None):
        if not email:
            raise  ValueError('user must has email address')
        if not name:
            raise  ValueError('user must has name')
        if not group:
            raise  ValueError('user must has group')
        user =self.model(
            email=self.normalize_email(email),
            name=name,
            group=group

        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,name,email,group,password):
        user = self.create_user(
            email=self.normalize_email(email),
            name=name,
            password=password,
            group=group
        )
        user.is_admin=True
        user.is_admin = True
        user.is_staff = True
        user.is_active = True
        user.is_superadmin = True

        user.save(using=self._db)
        return user



class Employee(AbstractBaseUser):
    name= models.CharField(max_length=50,unique=True)
    email = models.EmailField(max_length=100,unique=True)
    group=models.ForeignKey(Group,on_delete=models.CASCADE,default=1)

    #required
    data_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name',]

    objects=EmployeeManager()

    def __str__(self):
        return self.email

    def has_perm(self,perm,obj=None):
        return self.is_admin

    def has_module_perms(self,add_label):
        return True

class Attendance (models.Model):
    employee=models.ForeignKey(Employee,on_delete=models.CASCADE)
    attendance=models.BooleanField()
    date=models.DateField()

