from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, View
from django.urls import reverse_lazy, reverse
from .models import Category, Item
from users.views import LoginRequiredMixin
from .forms import ItemForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Q

# Create your views here.


def home(request):
    return render(request, 'items/home.html', )


#Vu qui sera vu par tout le monde
class ItemListView(ListView):
    model = Item
    template_name = 'items/item_list.html'
    context_object_name = 'items'
    paginate_by = 12

    def get_queryset(self):
        # On commence la requête en filtrant par les objets disponibles
        queryset = super().get_queryset().filter(is_available=True).order_by('-created_at')
        category_slug = self.kwargs.get('category_slug')
        query = self.request.GET.get('query')
        
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=category)

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            context['category_selected'] = get_object_or_404(Category, slug=category_slug)
        
        context['query'] = self.request.GET.get('query', '')
        return context
    

class UserItemsDashboardView(LoginRequiredMixin, ListView):
    model = Item
    template_name = 'items/user_items_dashboard.html'
    context_object_name = 'items'
    
    def get_queryset(self):
        return Item.objects.filter(owner=self.request.user).order_by('-created_at')

# Vue pour créer un nouvel objet
class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    form_class = ItemForm
    template_name = 'items/item_form.html'
    success_url = reverse_lazy('user_items_dashboard')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

# Vue pour modifier un objet
class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Item
    form_class = ItemForm
    template_name = 'items/item_form.html'
    success_url = reverse_lazy('user_items_dashboard')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        item = self.get_object()
        return self.request.user == item.owner

# Vue pour supprimer un objet
class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Item
    template_name = 'items/item_confirm_delete.html'
    success_url = reverse_lazy('user_items_dashboard')

    def test_func(self):
        item = self.get_object()
        return self.request.user == item.owner

    def form_valid(self, form):
        item = self.get_object()
        
        item.photo.delete(save=False)
        
        return super().form_valid(form)
    
class ItemDetailView(DetailView):
    model = Item
    template_name = 'items/item_detail.html'
    context_object_name = 'item'
    

class RelistItemView(LoginRequiredMixin, View):
    def post(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        
        if request.user != item.owner:
            # Redirige simplement si l'utilisateur n'est pas le propriétaire
            return redirect(reverse('item_detail', args=[pk]))
        
        # S'assure que l'objet est bien indisponible avant de le reposter
        if not item.is_available:
            item.is_available = True
            item.save()
            
        return redirect(reverse('item_detail', args=[pk]))



class ToggleItemAvailabilityView(LoginRequiredMixin, View):
    def post(self, request, pk):
        item = get_object_or_404(Item, pk=pk)

        # Vérifie que l'utilisateur est bien le propriétaire de l'objet
        if request.user != item.owner:
            return redirect(reverse('item_detail', args=[pk]))
        
        # Bascule simplement la valeur du champ is_available et sauvegarde
        item.is_available = not item.is_available
        item.save()

        return redirect(reverse('item_detail', args=[pk]))


def about(request):
    return render(request,'items/about.html')

def conditions(request):
    return render(request,'items/conditions.html')

def confidentiality(request):
    return render(request,'items/confidentiality.html')

def pas_encore_sur_les_reseaux(request):
    return render(request,'items/pas_encore_sur_les_reseaux.html')