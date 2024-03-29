from django.db import models

# Create your models here.
# database ----> Excel workbook
# Models in Django Table of Databas---> Sheet of WorkBook

class Post(models.Model):
    sno = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.CharField(max_length=100)
    slug = models.CharField(max_length=200)
    timeStamp = models.DateTimeField(blank=True)

    def __str__(self):
        return self.title + ' by '+ self.author