
from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description', 'photo', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full py-3 px-4 text-white leading-tight focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-gray-700 bg-opacity-50 border-gray-600 placeholder-gray-400 rounded-lg text-lg transition duration-200'}),
            'description': forms.Textarea(attrs={'class': 'w-full py-3 px-4 text-white leading-tight focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-gray-700 bg-opacity-50 border-gray-600 placeholder-gray-400 rounded-lg text-lg transition duration-200', 'rows': 4}),
            'photo': forms.FileInput(attrs={'class': 'w-full text-white bg-gray-700 bg-opacity-50 border-gray-600 rounded-lg py-3 px-4 transition duration-200'}),
            'category': forms.Select(attrs={'class': 'w-full py-3 px-4 text-white leading-tight focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-gray-700 bg-opacity-50 border-gray-600 placeholder-gray-400 rounded-lg text-lg transition duration-200'}),
        }