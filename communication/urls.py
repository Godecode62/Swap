from django.urls import path
from . import views

urlpatterns = [
    path('contact/', views.SupportTicketCreateView.as_view(), name='contact'),
    path('mes-tickets/', views.MyTicketsListView.as_view(), name='my_tickets'),
    path('mes-notifications/', views.MyNotificationsListView.as_view(), name='my_notifications'),
    path('signaler/<str:report_type>/<int:pk>/', views.report_create, name='report_create'),
    path('dashboard/', views.CommunicationDashboardView.as_view(), name='communication_dashboard'),
]
