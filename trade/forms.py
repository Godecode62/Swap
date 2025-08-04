# trade/forms.py
from django import forms
from .models import TradeOffer, TradeMessage
from items.models import Item

class TradeOfferForm(forms.ModelForm):
    # Ajout d'un champ de texte pour le message initial
    message = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Ajouter un message pour le propriétaire (optionnel)...'}),
        required=False,
        label='Message pour le propriétaire'
    )
    
    # Le champ 'item_offered' est un ModelChoiceField qui sera filtré dans la vue
    item_offered = forms.ModelChoiceField(
        queryset=Item.objects.all(),
        empty_label="--- Choisissez un objet ---",
        label="Mon objet à proposer"
    )

    class Meta:
        model = TradeOffer
        fields = ['item_offered']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['item_offered'].queryset = Item.objects.filter(owner=user, is_available=True)
            self.fields['item_offered'].empty_label = "--- Choisissez un objet ---"
            
class TradeMessageForm(forms.ModelForm):
    class Meta:
        model = TradeMessage
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Écrivez votre réponse ici...'}),
        }
        labels = {
            'message': ''
        }