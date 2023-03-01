from django.db import models
from django.contrib.auth.models import User


def profile_avatar_directory_path(instanse: "User", filename):
    return "users/user_{pk}/avatar/{filename}".format(pk=instanse.pk, filename=filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    agreement_accepted = models.BooleanField(default=False)
    avatar = models.ImageField(null=True, blank=True, upload_to=profile_avatar_directory_path)
