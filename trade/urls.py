from django.urls import path
from trade import views
urlpatterns = [
    path('offer/<int:pk>/', views.TradeOfferCreateView.as_view(), name='create_trade_offer'),
    path('offer/success/', views.TradeSuccessView.as_view(), name='trade_success'), 
    path('messages/<int:pk>/', views.TradeMessagesView.as_view(), name='trade_messages'),
    path('my_trades/', views.MyTradesView.as_view(), name='my_trades'),
    path('trade/details/<int:pk>/', views.TradeDetailsView.as_view(), name='trade_details'),
    path('history/<str:status>/', views.MyTradeHistoryView.as_view(), name='trade_history'),
    path('trade-accepted/', views.TradeAcceptedView.as_view(), name='trade_accepted'),
    path('start/<int:user_pk>/', views.StartConversationView.as_view(), name='start_conversation'),
    path('no/items/<int:pk>/', views.NoTradeItemsView.as_view(), name='no_trade_items'),
]
