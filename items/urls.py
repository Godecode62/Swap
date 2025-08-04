from django.urls import path
from items import views

urlpatterns = [
    path('',views.home, name='home'),
    path('dashboard/', views.UserItemsDashboardView.as_view(), name='user_items_dashboard'),
    path('create/', views.ItemCreateView.as_view(), name='item_create'),
    path('update/items/<int:pk>/', views.ItemUpdateView.as_view(), name='item_update'),
    path('delete/<int:pk>/', views.ItemDeleteView.as_view(), name='item_delete'),
    path('<int:pk>/', views.ItemDetailView.as_view(), name='item_detail'),
    path('items/all/',views.ItemListView.as_view(), name='item_list'),
    path('<slug:category_slug>/', views.ItemListView.as_view(), name='item_list_by_category'),
    path('item/<int:pk>/relist/', views.RelistItemView.as_view(), name='relist_item'),
    path('item/<int:pk>/toggle_availability/', views.ToggleItemAvailabilityView.as_view(), name='toggle_item_availability'),
    path('about/SwapIt/',views.about,name='about'),
    path('conditions/SwapIt/',views.conditions,name='conditions'),
    path('confidentality/SwapIt/',views.confidentiality,name='confidentiality'),
    path('pas/encore/sur/les/reseaux/', views.pas_encore_sur_les_reseaux, name='pas_encore_sur_les_reseaux'),
]
