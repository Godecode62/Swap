from django.urls import path
from users import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('admin/dashboard/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('login_required/',views.LoginRequiredPageView.as_view(),name='login_required'),
    path('no_permission',views.NoPermissionView.as_view(), name='no_permission'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/update/', views.ProfileUpdateView.as_view(), name='profile_update'),
    path('password/change/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    path('password/change/done/', views.password_change_done, name='password_change_done'),
    path('dashboard/', views.UserDashboardView.as_view(), name='user_dashboard'),
    path('<int:pk>/', views.PublicProfileView.as_view(), name='public_profile'),
]