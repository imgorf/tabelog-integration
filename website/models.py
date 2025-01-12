from django.db import models

class User(models.Model):
    userid = models.AutoField(primary_key=True)
    username = models.CharField()
    password = models.CharField()

    def __str__(self):
        return self.username
    
class Location(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField()
    address = models.CharField()