from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from django.contrib.auth.forms import PasswordChangeForm

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label="Adresse Email", required=True, 
                             widget=forms.EmailInput(attrs={'placeholder': 'votre.email@exemple.com', 'class': 'shadow appearance-none border rounded-lg w-full py-3 px-4 text-white leading-tight focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-gray-700 border-gray-600 placeholder-gray-500 text-lg transition duration-200'}))

    city = forms.CharField(max_length=100, required=False, label="Votre Ville",
                           widget=forms.TextInput(attrs={'placeholder': 'Ex: Conakry, Paris, New York...', 'class': 'shadow appearance-none border rounded-lg w-full py-3 px-4 text-white leading-tight focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-gray-700 border-gray-600 placeholder-gray-500 text-lg transition duration-200'}))
    
    phone_number = forms.CharField(max_length=15, required=False, label="Numéro de Téléphone (Optionnel)",
                                   widget=forms.TextInput(attrs={'placeholder': 'Ex: +224 620 00 00 00', 'class': 'shadow appearance-none border rounded-lg w-full py-3 px-4 text-white leading-tight focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-gray-700 border-gray-600 placeholder-gray-500 text-lg transition duration-200'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'city', 'phone_number',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        password_attrs = {
            'class': 'shadow appearance-none border rounded-lg w-full py-3 px-4 text-white leading-tight focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-gray-700 border-gray-600 placeholder-gray-500 text-lg transition duration-200',
        }
        
        if 'password1' in self.fields:
            self.fields['password1'].widget.attrs.update(password_attrs)
            self.fields['password1'].widget.attrs['placeholder'] = 'Minimum 8 caractères'
        
        if 'password2' in self.fields:
            self.fields['password2'].widget.attrs.update(password_attrs)
            self.fields['password2'].widget.attrs['placeholder'] = 'Confirmez votre mot de passe'

        # Styles et placeholders pour le champ 'username'
        if 'username' in self.fields:
            self.fields['username'].widget.attrs.update({
                'class': 'shadow appearance-none border rounded-lg w-full py-3 px-4 text-white leading-tight focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-gray-700 border-gray-600 placeholder-gray-500 text-lg transition duration-200',
                'placeholder': 'Choisissez un nom d\'utilisateur unique'
            })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not self.instance.pk and User.objects.filter(email=email).exists():
            raise forms.ValidationError("Cette adresse email est déjà utilisée.")
        return email


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'city', 'phone_number', 'profile_picture', 'bio')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        default_attrs = {
            'class': 'pl-14 shadow appearance-none border rounded-lg w-full py-3 px-4 text-white leading-tight focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-gray-700 bg-opacity-50 border-gray-600 placeholder-gray-400 text-lg transition duration-200'
        }
        
        for field_name, field in self.fields.items():
            field.widget.attrs.update(default_attrs)
            
            if field_name == 'username':
                field.widget.attrs['placeholder'] = 'Votre nouveau nom d\'utilisateur'
            elif field_name == 'email':
                field.widget.attrs['placeholder'] = 'Votre nouvelle adresse email'
            elif field_name == 'city':
                field.widget.attrs['placeholder'] = 'Votre ville (ex: Conakry)'
            elif field_name == 'phone_number':
                field.widget.attrs['placeholder'] = 'Votre numéro de téléphone (optionnel)'
            elif field_name == 'bio':
                field.widget.attrs['placeholder'] = 'Parlez-nous un peu de vous...'
                field.widget.attrs['rows'] = 4 

        if 'profile_picture' in self.fields:
            self.fields['profile_picture'].widget.attrs.update({
                'class': 'block w-full text-sm text-gray-400 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-purple-500 file:text-white hover:file:bg-purple-600 transition duration-300 cursor-pointer',
                'accept': 'image/*'
            })
            self.fields['profile_picture'].widget.attrs.pop('class', None)


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full py-3 pl-12 pr-10 text-white leading-tight focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-gray-700 bg-opacity-50 border-gray-600 placeholder-gray-400 rounded-lg text-lg transition duration-200'
            })
