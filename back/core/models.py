from django.contrib.auth.models import Group, AbstractUser
from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField("Titre", max_length=500)
    content = models.TextField("Contenu")
    
    def __str__(self):
        return self.title

class CustomGroup(Group):
    specific = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Groupe"
        verbose_name_plural = "Groupes"

class CustomUser(AbstractUser):
    specific = models.BooleanField(default=False)
    group = models.ForeignKey(CustomGroup, null=True, blank=True, on_delete=models.SET_NULL, related_name='users')
    groups = None
    user_permissions = None