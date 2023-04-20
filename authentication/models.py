from django.db import models
from django.contrib.auth.models import User


class MyUser(User):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    gender = models.TextField()

    class Meta:
        db_table = "user"
