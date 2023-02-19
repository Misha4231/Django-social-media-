from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateTimeField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)

    #def __str__(self):
    #    return self.user

    def get_absolute_url(self):
        return reverse('user_detail', args=[self.id,])