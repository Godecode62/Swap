
from django.db import models
from django.conf import settings

from trade.models import TradeOffer

# Modèle pour les tickets de support
class SupportTicket(models.Model):
    STATUS_CHOICES = [
        ('open', 'Ouvert'),
        ('in_progress', 'En cours'),
        ('resolved', 'Résolu'),
        ('closed', 'Fermé'),
    ]

    subject = models.CharField(max_length=200, verbose_name='Sujet')
    message = models.TextField(verbose_name='Message')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='support_tickets',
        verbose_name='Utilisateur'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='open',
        verbose_name='Statut'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ticket #{self.id} - {self.subject}"

    class Meta:
        verbose_name = 'Ticket de Support'
        verbose_name_plural = 'Tickets de Support'
        ordering = ['-created_at']

# Modèle pour les notifications
class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name='Utilisateur'
    )
    message = models.TextField(verbose_name='Message')
    is_read = models.BooleanField(default=False, verbose_name='Lu')
    created_at = models.DateTimeField(auto_now_add=True)
    
    trade_offer = models.ForeignKey(
        TradeOffer,
        on_delete=models.CASCADE,
        related_name='notifications',
        null=True, blank=True,
        verbose_name='Offre de troc associée'
    )

    def __str__(self):
        return f"Notification pour {self.user.username}"

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_at']
        
        
        
# Modèle pour les signalements
class Report(models.Model):
    REPORT_TYPE_CHOICES = [
        ('item', 'Annonce'),
        ('user', 'Utilisateur'),
    ]

    reported_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reports_made',
        verbose_name='Signalé par'
    )
    report_type = models.CharField(
        max_length=10,
        choices=REPORT_TYPE_CHOICES,
        verbose_name='Type de signalement'
    )
    reported_item_id = models.IntegerField(
        null=True, blank=True, verbose_name='ID de l\'annonce signalée'
    )
    reported_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reports_received',
        null=True, blank=True,
        verbose_name='Utilisateur signalé'
    )
    reason = models.TextField(verbose_name='Raison')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Signalement #{self.id} - {self.report_type} par {self.reported_by.username}"

    class Meta:
        verbose_name = 'Signalement'
        verbose_name_plural = 'Signalements'
        ordering = ['-created_at']
