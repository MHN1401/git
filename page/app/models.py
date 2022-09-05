import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from faker import Faker
fake = Faker()
# Create your models here.
class Employee(models.Model):
    user = models.ForeignKey(User,on_delete=(models.CASCADE))
    department = models.CharField(max_length=100)
    def __str__(self):
        return self.department

class Work(models.Model):
    work_title = models.CharField(max_length=100)
    price = models.CharField(max_length = 100)
    time = models.CharField(max_length = 100)
    employer = models.CharField(max_length = 100)
    info = models.CharField(max_length = 300, default = '')
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.work_title

