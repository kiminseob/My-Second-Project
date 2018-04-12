from django.db import models

# Create your models here.
class MY_HOME(models.Model):
  userID = models.CharField(max_length=50,default="0",primary_key=True)
  name = models.CharField(max_length=20,default="0")
  studentNum = models.CharField(max_length=9,default="0")
  major = models.CharField(max_length=20,default="0")
  createDate = models.DateTimeField()
  announcement = models.TextField(default="0")
  subject = models.TextField(default="0")
  resource = models.TextField(default="0")