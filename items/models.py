import pathlib
from django.db import models
from users.models import User, compress_image
import uuid 

def item_photo_path(instance, filename):
    item_id = instance.pk if instance.pk else str(uuid.uuid4())
    return f'trade_items/{instance.owner.username}/{item_id}/main_photo.jpg'

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
        # Récupére l'ancienne photo de l'objet avant de sauvegarder les modifications
        # Cela permet de la supprimer si une nouvelle photo est téléchargée.
        try:
            old_item = Item.objects.get(pk=self.pk)
            old_photo = old_item.photo
        except Item.DoesNotExist:
            old_photo = None 

        # Si une nouvelle photo est fournie ET qu'elle est différente de l'ancienne
        if self.photo and old_photo and self.photo.name != old_photo.name:
            # Supprimez l'ancienne photo du stockage Cloudflare R2
            old_photo.delete(save=False)

        if self.photo and (not old_photo or self.photo.name != old_photo.name):
            self.photo = compress_image(self.photo, quality_setting=70)
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Objet à troquer"
        verbose_name_plural = "Objets à troquer"
        ordering = ['-created_at']
