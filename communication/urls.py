from django.urls import path
from . import admin_views
from . import views

urlpatterns = [
    path('contact/', views.SupportTicketCreateView.as_view(), name='contact'),
    path('mes-tickets/', views.MyTicketsListView.as_view(), name='my_tickets'),
    path('mes-notifications/', views.MyNotificationsListView.as_view(), name='my_notifications'),
    path('signaler/<str:report_type>/<int:pk>/', views.report_create, name='report_create'),
    path('dashboard/', views.CommunicationDashboardView.as_view(), name='communication_dashboard'),
    
    #Admiins views
    path('report/success/', admin_views.ReportSuccessView.as_view(), name='report_sent_success'),
    path('report/error/', admin_views.ReportErrorView.as_view(), name='report_error'), 
    # URLs d'administration
    path('admin/tickets/', admin_views.AdminTicketListView.as_view(), name='admin_ticket_list'),
    path('admin/tickets/<int:pk>/', admin_views.AdminTicketDetailView.as_view(), name='admin_ticket_detail'),
    path('admin/tickets/<int:pk>/update/', admin_views.AdminTicketUpdateView.as_view(), name='admin_ticket_update'),
    path('admin/tickets/<int:pk>/delete/', admin_views.AdminTicketDeleteView.as_view(), name='admin_ticket_delete'),
    path('admin/reports/', admin_views.AdminReportListView.as_view(), name='admin_report_list'),
    path('admin/reports/<int:pk>/', admin_views.AdminReportDetailView.as_view(), name='admin_report_detail'),
    path('admin/reports/<int:pk>/delete/', admin_views.AdminReportDeleteView.as_view(), name='admin_report_delete'),
]
