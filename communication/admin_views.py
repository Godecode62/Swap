from django.urls import reverse_lazy
from users.views import  AdminRequiredMixin
from django.views.generic import ListView, DetailView,DeleteView, TemplateView, UpdateView
from communication.models import Report, SupportTicket 




class AdminTicketListView(AdminRequiredMixin, ListView):
    model = SupportTicket
    template_name = 'communication/admin/ticket_list.html'
    context_object_name = 'tickets'
    queryset = SupportTicket.objects.all().order_by('-created_at')

class AdminTicketDetailView(AdminRequiredMixin, DetailView):
    model = SupportTicket
    template_name = 'communication/admin/ticket_detail.html'
    context_object_name = 'ticket'

class AdminTicketUpdateView(AdminRequiredMixin, UpdateView):
    model = SupportTicket
    template_name = 'communication/admin/ticket_update.html'
    fields = ['status']
    
    def get_success_url(self):
        return reverse_lazy('admin_ticket_detail', kwargs={'pk': self.object.pk})

class AdminTicketDeleteView(AdminRequiredMixin, DeleteView):
    model = SupportTicket
    template_name = 'communication/admin/ticket_confirm_delete.html'
    success_url = reverse_lazy('admin_ticket_list')


class AdminReportListView(AdminRequiredMixin, ListView):
    model = Report
    template_name = 'communication/admin/report_list.html'
    context_object_name = 'reports'
    queryset = Report.objects.all().order_by('-created_at')

class AdminReportDetailView(AdminRequiredMixin, DetailView):
    model = Report
    template_name = 'communication/admin/report_detail.html'
    context_object_name = 'report'

class AdminReportDeleteView(AdminRequiredMixin, DeleteView):
    model = Report
    template_name = 'communication/admin/report_confirm_delete.html'
    success_url = reverse_lazy('admin_report_list')

class TicketSuccessView(TemplateView):
    template_name = 'communication/ticket_success.html'

class ReportSuccessView(TemplateView):
    template_name = 'communication/report_success.html'

class ReportErrorView(TemplateView):
    template_name = 'communication/report_error.html'