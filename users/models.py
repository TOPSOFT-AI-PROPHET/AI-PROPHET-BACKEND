from django.db import models
from django.contrib.auth.models import UserManager, AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator

class CustomUserManager(UserManager):
    def get_by_natural_key(self, username):
        return self.get(
            models.Q(**{self.model.USERNAME_FIELD: username}) |
            models.Q(**{self.model.EMAIL_FIELD: username})
        )

class UserProfile(AbstractUser):
    nickname = models.CharField(blank=True, max_length=150, verbose_name='nick name')
    email = models.EmailField(blank=True, max_length=254, verbose_name='email address', validators=[UnicodeUsernameValidator()], unique=True)
    credit = models.DecimalField(max_digits=20, decimal_places=2, default=0, verbose_name='credit')
    profile_image_url = models.ImageField(upload_to='avatar/%Y%m%d/',blank=True, verbose_name='avatar')
    contact_number = models.TextField(blank=True, verbose_name='contact number')
    objects = CustomUserManager()