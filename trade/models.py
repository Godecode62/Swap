from django.db import models
from django.conf import settings
from items.models import Item

# Create your models here.

class TradeOffer(models.Model):
    STATUS_CHOICES = (
        ('pending', 'En attente'),
        ('accepted', 'Acceptée'),
        ('rejected', 'Refusée'),
    )

    item_offered = models.ForeignKey(
        Item, 
        on_delete=models.CASCADE, 
        related_name='offered_for_trade',
        verbose_name='Objet proposé'
    )
    item_requested = models.ForeignKey(
        Item, 
        on_delete=models.CASCADE, 
        related_name='requested_for_trade',
        verbose_name='Objet demandé'
    )
    offered_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='trade_offers_made',
        verbose_name='Proposé par'
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending',
        verbose_name='Statut de la proposition'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Offre de {self.item_offered.title} pour {self.item_requested.title}"

class TradeMessage(models.Model):
    trade_offer = models.ForeignKey(
        TradeOffer,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name='Proposition de troc'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_trade_messages',
        verbose_name='Expéditeur'
    )
    message = models.TextField(verbose_name='Message')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message de {self.sender.username} pour l'offre {self.trade_offer.id}"