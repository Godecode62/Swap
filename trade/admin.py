from django.contrib import admin
from trade.models import TradeOffer, TradeMessage

# Register your models here.

@admin.register(TradeOffer)
class TradeAdmin(admin.ModelAdmin):
    list_display = ['STATUS_CHOICES', 'item_offered', 'item_requested', 'offered_by', 'status', 'created_at']
    list_filter = ['status', 'offered_by']
    
    
@admin.register(TradeMessage)
class TradeItemAdmin(admin.ModelAdmin):
    list_display    = ['trade_offer', 'sender', 'message', 'created_at']