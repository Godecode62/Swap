from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView

from .models import SupportTicket, Notification, Report
from .forms import SupportTicketForm, ReportForm

# VUE DE CLASSE (CreateView) pour créer un ticket de support
class SupportTicketCreateView(LoginRequiredMixin, CreateView):
    model = SupportTicket
    form_class = SupportTicketForm
    template_name = 'communication/contact.html'
    success_url = reverse_lazy('my_tickets') 

    def form_valid(self, form):
        # Associe le ticket à l'utilisateur connecté
        form.instance.user = self.request.user
        messages.success(self.request, "Votre ticket de support a été envoyé avec succès.")
        return super().form_valid(form)

# VUE DE CLASSE (ListView) pour lister les tickets de l'utilisateur
class MyTicketsListView(LoginRequiredMixin, ListView):
    model = SupportTicket
    template_name = 'communication/my_tickets.html'
    context_object_name = 'tickets' 

    def get_queryset(self):
        # Récupère uniquement les tickets de l'utilisateur connecté
        return SupportTicket.objects.filter(user=self.request.user)

# VUE DE CLASSE (ListView) pour lister les notifications de l'utilisateur
class MyNotificationsListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'communication/my_notifications.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        # Récupère uniquement les notifications de l'utilisateur connecté
        notifications = Notification.objects.filter(user=self.request.user)
        # Marque toutes les notifications comme lues
        notifications.update(is_read=True)
        return notifications

# VUE DE FONCTION (FBV) pour créer un signalement
@login_required
def report_create(request, report_type, pk):
    # report_type peut être 'user' ou 'item'
    reported_content = None
    if report_type == 'user':
        from django.contrib.auth import get_user_model
        User = get_user_model()
        reported_content = get_object_or_404(User, pk=pk)
    elif report_type == 'item':
        from items.models import Item
        reported_content = get_object_or_404(Item, pk=pk)
    else:
        messages.error(request, "Type de signalement invalide.")
        return redirect('home')

    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.reported_by = request.user
            report.report_type = report_type
            if report_type == 'user':
                report.reported_user = reported_content
            else:
                report.reported_item_id = reported_content.id
            report.save()
            messages.success(request, "Votre signalement a été envoyé.")
            return redirect('home')
    else:
        form = ReportForm()

    context = {
        'form': form,
        'report_type': report_type,
        'reported_content': reported_content
    }
    return render(request, 'communication/report.html', context)



class CommunicationDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'communication/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Tickets de support
        all_tickets = SupportTicket.objects.filter(user=user)
        context['all_tickets_count'] = all_tickets.count()
        context['open_tickets_count'] = all_tickets.filter(status='open').count()
        context['in_progress_tickets_count'] = all_tickets.filter(status='in_progress').count()
        context['resolved_tickets_count'] = all_tickets.filter(status='resolved').count()
        
        # Le calcul corrigé pour les tickets fermés
        closed_tickets_count = all_tickets.exclude(
            status__in=['open', 'in_progress', 'resolved']
        ).count()
        context['closed_tickets_count'] = closed_tickets_count
        
        # Notifications
        context['all_notifications_count'] = Notification.objects.filter(user=user).count()
        context['unread_notifications_count'] = Notification.objects.filter(user=user, is_read=False).count()
        
        # Signalements
        context['reports_sent_count'] = Report.objects.filter(reported_by=user).count()
        
        return context