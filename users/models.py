from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    Birth_date = models.DateField()

    def __str__(self):
        return self.first_name + " " + self.last_name
