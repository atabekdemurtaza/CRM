from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.db.models.signals import pre_save

#User = get_user_model()

class User(AbstractUser):

    pass 

class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username}'

class Lead(models.Model):

    first_name = models.CharField(max_length=20)
    last_name  = models.CharField(max_length=20)
    age        = models.IntegerField(default=0)
    agent      = models.ForeignKey("Agent", on_delete=models.CASCADE)

    def __str__(self):

        return f'{self.first_name} {self.last_name}'


class Agent(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organisation = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.email}'

def post_user_created_signal(sender, instance, created, **kwargs):
   #print(instance, created)
   if created:
        UserProfile.objects.create(user=instance) 
        #print(UserProfile.objects.create(user=instance))

post_save.connect(post_user_created_signal, sender=User)