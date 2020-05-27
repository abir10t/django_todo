from django.db import models
from django.contrib.auth.models import User #for one to many relationship

class Todo(models.Model): #search django model field
    title = models.CharField(max_length=100)
    memo = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True , blank=True)
    important =  models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)#ForeignKey store the relationship between this todo and that.
#python3 manage.py makemigrations
#python3 manage.py migrate
    def __str__(self): #for showing the title in the database.
     return self.title
