#user/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Create your models here.
#장고가 제공하는 기본적인 auth_user =AbstractUser
class UserModel(AbstractUser):
    class Meta:
        db_table = "my_user"

    bio = models.CharField(max_length=256, default='')
    # Authusermodel이 우리 사용자 모들이다.
    follow = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followee')
    #장고에서 제공해주는건 그냥 사용하고 우리는 bio만 추가했다.