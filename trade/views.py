from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, View, TemplateView, ListView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.db import transaction
from django.contrib.auth import get_user_model

from items.models import Item
from communication.models import Notification
from .models import TradeOffer, TradeMessage
from .forms import TradeOfferForm, TradeMessageForm


User = get_user_model()


class TradeOfferCreateView(LoginRequiredMixin, CreateView):
    model = TradeOffer
    form_class = TradeOfferForm
    template_name = 'trade/trade_offer_form.html'

    def dispatch(self, request, *args, **kwargs):
        item_requested = get_object_or_404(Item, pk=self.kwargs['pk'])
        if item_requested.owner == request.user:
            return redirect(reverse('no_permission'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item_requested = get_object_or_404(Item, pk=self.kwargs['pk'])
        context['item_requested'] = item_requested
        context['user_items'] = Item.objects.filter(owner=self.request.user, is_available=True).exclude(pk=item_requested.pk)
        return context

    def form_valid(self, form):
        item_requested = get_object_or_404(Item, pk=self.kwargs['pk'])
        user = self.request.user
        item_offered = form.cleaned_data.get('item_offered')

        existing_offer = TradeOffer.objects.filter(
            (Q(offered_by=user, item_requested=item_requested, item_offered=item_offered) |
            Q(offered_by=item_requested.owner, item_requested=item_offered, item_offered=item_requested))
        ).first()

        if existing_offer:
            return redirect(reverse('trade_messages', kwargs={'pk': existing_offer.pk}))
        
        form.instance.offered_by = user
        form.instance.item_requested = item_requested
        response = super().form_valid(form)
        
        message_text = form.cleaned_data.get('message')
        if message_text:
            TradeMessage.objects.create(
                trade_offer=self.object,
                sender=user,
                message=message_text
            )

        Notification.objects.create(
            user=item_requested.owner,
            message=f"{user.username} a fait une nouvelle proposition d'échange pour votre objet '{item_requested.title}'.",
            trade_offer=self.object
        )
        
        return response
    
    def get_success_url(self):
        return reverse('trade_success')


class TradeMessagesView(LoginRequiredMixin, View):
    def get(self, request, pk):
        trade_offer = get_object_or_404(TradeOffer, pk=pk)
        if request.user not in [trade_offer.offered_by, trade_offer.item_requested.owner]:
            return redirect('home')

        messages = trade_offer.messages.order_by('created_at')
        form = TradeMessageForm()
        
        return render(request, 'trade/trade_messages.html', {
            'trade_offer': trade_offer,
            'messages': messages,
            'form': form,
        })
    
    def post(self, request, pk):
        trade_offer = get_object_or_404(TradeOffer, pk=pk)
        if request.user not in [trade_offer.offered_by, trade_offer.item_requested.owner]:
            return redirect('home')

        form = TradeMessageForm(request.POST)
        if form.is_valid():
            TradeMessage.objects.create(
                trade_offer=trade_offer,
                sender=request.user,
                message=form.cleaned_data['message']
            )
        
        return redirect('trade_messages', pk=trade_offer.pk)


class TradeSuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'trade/trade_success.html'


class MyTradesView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        query = request.GET.get('q', '')
        trade_filter = request.GET.get('filter', '')

        queryset = TradeOffer.objects.filter(
            Q(offered_by=user) | Q(item_requested__owner=user)
        ).select_related('item_offered', 'item_requested', 'offered_by', 'item_requested__owner').order_by('-created_at')

        if trade_filter == 'sent':
            queryset = queryset.filter(offered_by=user)
        elif trade_filter == 'received':
            queryset = queryset.filter(item_requested__owner=user)

        if query:
            queryset = queryset.filter(
                Q(item_offered__title__icontains=query) |
                Q(item_requested__title__icontains=query)
            )
        
        return render(request, 'trade/my_trades.html', {
            'trade_offers': queryset,
            'query': query,
            'trade_filter': trade_filter,
        })
        

class MyTradeHistoryView(LoginRequiredMixin, ListView):
    model = TradeOffer
    context_object_name = 'trade_offers'
    template_name = 'trade/my_trade_history.html'

    def get_queryset(self):
        status_filter = self.kwargs.get('status', 'accepted')
        queryset = TradeOffer.objects.filter(
            Q(offered_by=self.request.user) | Q(item_requested__owner=self.request.user)
        ).filter(status=status_filter).distinct().select_related(
            'item_offered', 'item_requested', 'offered_by', 'item_requested__owner'
        ).order_by('-created_at')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(item_offered__title__icontains=query) |
                Q(item_requested__title__icontains=query) |
                Q(item_offered__description__icontains=query) |
                Q(item_requested__description__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_filter'] = self.kwargs.get('status', 'accepted')
        context['query'] = self.request.GET.get('q', '')
        return context


class TradeDetailsView(LoginRequiredMixin, View):
    def get(self, request, pk):
        trade_offer = get_object_or_404(TradeOffer, pk=pk)
        if request.user not in [trade_offer.offered_by, trade_offer.item_requested.owner]:
            return redirect(reverse('no_permission'))
        context = {
            'trade_offer': trade_offer
        }
        return render(request, 'trade/trade_details.html', context)

    def post(self, request, pk):
        trade_offer = get_object_or_404(TradeOffer, pk=pk)
        action = request.POST.get('action')

        if trade_offer.status == 'pending':
            with transaction.atomic():
                if action == 'accept':
                    if request.user == trade_offer.item_requested.owner:
                        trade_offer.status = 'accepted'
                        
                        offered_item = trade_offer.item_offered
                        requested_item = trade_offer.item_requested

                        offered_item.owner = trade_offer.item_requested.owner
                        requested_item.owner = trade_offer.offered_by
                        
                        offered_item.is_available = False
                        requested_item.is_available = False
                        
                        offered_item.save()
                        requested_item.save()
                        trade_offer.save()
                        
                        Notification.objects.create(
                            user=trade_offer.offered_by,
                            message=f"Votre proposition d'échange pour '{requested_item.title}' a été ACCEPTÉE !",
                            trade_offer=trade_offer
                        )

                        return redirect('trade_accepted')
                    else:
                        return redirect(reverse('no_permission'))
                elif action == 'reject':
                    if request.user == trade_offer.item_requested.owner:
                        trade_offer.status = 'rejected'
                        trade_offer.save()
                        
                        Notification.objects.create(
                            user=trade_offer.offered_by,
                            message=f"Votre proposition d'échange pour '{trade_offer.item_requested.title}' a été REFUSÉE.",
                            trade_offer=trade_offer
                        )

                        return redirect('my_trades')
                    else:
                        return redirect(reverse('no_permission'))
        
        return redirect('my_trades')


class TradeAcceptedView(LoginRequiredMixin, TemplateView):
    template_name = 'trade/trade_accepted.html'
    
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
    


class StartConversationView(LoginRequiredMixin, View):
    def get(self, request, user_pk):
        current_user = request.user
        other_user = get_object_or_404(User, pk=user_pk)

        if current_user == other_user:
            return redirect(reverse('no_permission'))

        other_user_items = Item.objects.filter(owner=other_user, is_available=True)
        if not other_user_items.exists():
            return redirect(reverse('no_trade_items', kwargs={'pk': other_user.pk}))

        existing_offer = TradeOffer.objects.filter(
            Q(offered_by=current_user, item_requested__owner=other_user) |
            Q(offered_by=other_user, item_requested__owner=current_user)
        ).first()

        if existing_offer:
            return redirect(reverse('trade_messages', kwargs={'pk': existing_offer.pk}))
        
        return redirect(reverse('trade_offer_create', kwargs={'pk': other_user.pk}))


class NoTradeItemsView(LoginRequiredMixin, TemplateView):
    template_name = 'trade/no_trade_items.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['other_user'] = get_object_or_404(User, pk=self.kwargs['pk'])
        return context
