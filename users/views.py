from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView 
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, ListView
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import get_user_model
from communication.models import Notification
from trade.forms import TradeOfferForm
from users.models import User
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from items.models import Item
from trade.models import TradeMessage, TradeOffer
from django.db.models import Q
from datetime import timedelta
from django.utils import timezone


from .forms import CustomUserCreationForm, CustomUserChangeForm,CustomPasswordChangeForm

# --- Mixins d'Authentification ---

class UserNotAuthenticatedMixin(UserPassesTestMixin):
    def test_func(self):
        return not self.request.user.is_authenticated
    
    def handle_no_permission(self):
        return redirect(reverse_lazy('home')) 

class LoginRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated
    
    def handle_no_permission(self):
        return redirect(reverse_lazy('login_required')) 

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff and self.request.user.is_superuser
    
    def handle_no_permission(self):
        return redirect(reverse_lazy('no_permission')) 

# --- Vues d'Authentification ---

class SignUpView(UserNotAuthenticatedMixin, CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/signup.html'
    
    def form_invalid(self, form):
        print("FORM IS INVALID! Errors:")
        for field, errors in form.errors.items():
            print(f"  Field '{field}': {errors}")
        return super().form_invalid(form)
    
class CustomLoginView(UserNotAuthenticatedMixin, LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('user_dashboard')
    
    def get_success_url(self):
        if self.request.user.is_authenticated:
            return reverse('user_dashboard')
        return super().get_success_url()


class CustomLogoutView(LoginRequiredMixin, LogoutView):
    next_page = reverse_lazy('login')

# --- Vues de Page Spécifiques celle la c'est pour l'admin ---

class AdminDashboardView(AdminRequiredMixin, TemplateView):
    template_name = 'users/admin_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        User = get_user_model()
        context['total_users'] = User.objects.count()
        context['active_items'] = 78 
        context['completed_exchanges'] = 42 
        context['unread_messages'] = 5 
        return context
    
class UserDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'users/user_dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        user = self.request.user
        
        # Nombre total d'objets postés par l'utilisateur (disponibles)
        context['item_count'] = Item.objects.filter(owner=user,is_available=True).count()
        
        # Nombre d'offres de troc reçues (en attente)
        context['offers_received_count'] = TradeOffer.objects.filter(
            item_requested__owner=user,
            status='pending'
        ).count()
        
        # Nombre d'offres de troc envoyées (en attente)
        context['offers_sent_count'] = TradeOffer.objects.filter(
            offered_by=user,
            status='pending'
        ).count()

        # Compteurs pour l'historique des transactions.
        # Utilisation de .distinct() pour éviter les doublons.
        all_user_trades = TradeOffer.objects.filter(
            Q(offered_by=user) | Q(item_requested__owner=user)
        ).distinct()

        context['accepted_trades_count'] = all_user_trades.filter(status='accepted').count()
        context['refused_trades_count'] = all_user_trades.filter(status='rejected').count()
        context['cancelled_trades_count'] = all_user_trades.filter(status='cancelled').count()
        
        return context        
    
#### Ces vus permettent à l'utilisateur de gerer son compte
class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        user = self.request.user
        
        accepted_trades_count = TradeOffer.objects.filter(
            Q(offered_by=user, status='accepted') | Q(item_requested__owner=user, status='accepted')
        ).distinct().count()

        # Vérification si l'utilisateur est actif (dernière connexion dans les 30 jours)
        active_period = timezone.now() - timedelta(days=30)
        is_active = user.last_login and user.last_login > active_period

        context['accepted_trades_count'] = accepted_trades_count
        context['is_active'] = is_active
        
        return context
    
        
class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'users/profile_update.html'
    context_object_name = 'user'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user

class CustomPasswordChangeView(LoginRequiredMixin,PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'users/password_change.html'
    success_url = reverse_lazy('password_change_done')


def password_change_done(request):
    logout(request)
    return render(request, 'users/password_change_done.html')



### Vues publics pour permettre aux utilisateurs de voir les profils des autres utilisateurs
class PublicProfileView(DetailView):
    model = User
    template_name = 'users/public_profile.html'
    context_object_name = 'profile_user'

    def get_object(self, queryset=None):
        return get_object_or_404(User, pk=self.kwargs['pk'])
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_user = self.object

        accepted_trades_count = TradeOffer.objects.filter(
            Q(offered_by=profile_user, status='accepted') | Q(item_requested__owner=profile_user, status='accepted')
        ).distinct().count()

        active_period = timezone.now() - timedelta(days=30)
        is_active = profile_user.last_login and profile_user.last_login > active_period

        context['accepted_trades_count'] = accepted_trades_count
        context['is_active'] = is_active
        context['items'] = Item.objects.filter(owner=profile_user, is_available=True)
        return context


# --- Vues pour les Pages d'Erreur ---

class NoPermissionView(TemplateView):
    template_name = 'users/no_permission.html'

class LoginRequiredPageView(TemplateView):
    template_name = 'users/login_required.html'
    

