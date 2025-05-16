from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField("Titre", max_length=500)
    content = models.TextField("Contenu")