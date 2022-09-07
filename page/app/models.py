import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Employee(models.Model):
    user = models.OneToOneField(User,on_delete=(models.CASCADE))
    department = models.CharField(max_length=100)
    def __str__(self):
        return self.department

class Work(models.Model):
    work_title = models.CharField(max_length=100)
    price = models.IntegerField()
    time = models.IntegerField()
    employer = models.CharField(max_length = 100)
    info = models.CharField(max_length = 300, default = '')
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.work_title

