from django.db import models
from users.models import User, compress_image
import os
import uuid

def item_photo_path(instance, filename):
    extension = os.path.splitext(filename)[1]
    unique_filename = f'{uuid.uuid4()}{extension}'
    return f'trade_items/{instance.owner.username}/{unique_filename}'

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nom de la catégorie")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Slug")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        
        
class Item(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items')
    title = models.CharField(max_length=200, verbose_name="Nom de l'objet")
    description = models.TextField(verbose_name="Description détaillée")
    photo = models.ImageField(upload_to=item_photo_path, verbose_name="Photo de l'objet")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='items')
    created_at = models.DateTimeField(auto_now_add=True)
    is_available = models.BooleanField(default=True, verbose_name="Disponible pour troc")

    def save(self, *args, **kwargs):
        # Je ne compresse l'image que si elle est nouvelle ou a été modifiée
        try:
            current_photo = Item.objects.get(pk=self.pk).photo
        except Item.DoesNotExist:
            current_photo = None

        if self.photo and self.photo != current_photo:
            self.photo = compress_image(self.photo, quality_setting=70)
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Objet à troquer"
        verbose_name_plural = "Objets à troquer"
        ordering = ['-created_at']