from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files import File
import os

# Fonction pour compresser les images
def compress_image(image, quality_setting=70):
    img = Image.open(image)
    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')
    
    img_io = BytesIO()
    img.save(img_io, format='JPEG', quality=quality_setting)
    
    new_image = File(img_io, name=image.name)
    return new_image

# Utilise un nom de fichier prévisible pour permettre l'écrasement
def profile_picture_path(instance, filename):
    return f'profile_pictures/{instance.username}/profile.jpg'


class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="Numéro de téléphone")
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name="Ville")
    profile_picture = models.ImageField(upload_to=profile_picture_path, blank=True, null=True, verbose_name="Photo de profil")
    bio = models.TextField(blank=True, verbose_name="Biographie")

    def save(self, *args, **kwargs):
        # Vérifie si l'utilisateur a déjà une photo de profil et si elle est mise à jour
        # Le 'try...except' gère le cas où l'objet n'existe pas encore
        try:
            old_profile_picture = User.objects.get(id=self.id).profile_picture
        except User.DoesNotExist:
            old_profile_picture = None

        # Si l'utilisateur est nouveau ou si une nouvelle image est téléchargée
        if self.profile_picture and old_profile_picture != self.profile_picture:
            # Supprime l'ancienne image si elle existe
            if old_profile_picture:
                old_profile_picture.delete(save=False)

            self.profile_picture = compress_image(self.profile_picture, quality_setting=50)

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Utilisateur Personnalisé"
        verbose_name_plural = "Utilisateurs Personnalisés"

    def __str__(self):
        return self.username
