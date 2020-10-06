from django.urls import path
from django.contrib.auth import views as auth_views
from rs_core import views


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
    path('password_reset/', views.RequestPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('signup/', views.signup, name='signup'),
    path('accounts/update/<pk>/', views.edit_user, name='account_update'),
    path('get_image_by_name/<name>', views.get_image_by_name, name='get_image_by_name'),
    path('get_image_names_by_loc/<long>/<lat>/<direction>/<count>', views.get_image_names_by_loc,
         name='get_image_names_by_loc'),
    path('get_all_routes/', views.get_all_routes, name='get_all_routes'),
]
