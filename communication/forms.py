# communication/forms.py

from django import forms
from .models import SupportTicket, Report

class SupportTicketForm(forms.ModelForm):
    class Meta:
        model = SupportTicket
        fields = ['subject', 'message']
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'w-full p-4 bg-gray-800 border border-gray-700 text-gray-50 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500',
                'placeholder': 'Sujet de votre demande'
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full p-4 bg-gray-800 border border-gray-700 text-gray-50 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500',
                'rows': 5, 
                'placeholder': 'Décrivez votre problème en détail...'
            }),
        }

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['reason']
        widgets = {
            'reason': forms.Textarea(attrs={
                'class': 'w-full p-4 bg-gray-800 border border-gray-700 text-gray-50 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500',
                'rows': 5, 
                'placeholder': 'Raison du signalement...'
            }),
        }