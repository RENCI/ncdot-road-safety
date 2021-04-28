from django.urls import path
from django.contrib.auth import views as auth_views
from rs_core import views


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
    path('get_user_info/<uid>/', views.get_user_info, name='get_user_info'),
    path('get_user_annotation_info/<uid>/', views.get_user_annot_info, name='get_user_annot_info'),
    path('password_reset/', views.RequestPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('signup/', views.signup, name='signup'),
    path('accounts/update/<pk>/', views.edit_user, name='account_update'),
    path('get_image_by_name/<name>/', views.get_image_by_name, name='get_image_by_name'),
    path('get_original_image_by_name/<name>/', views.get_original_image_by_name, name='get_original_image_by_name'),
    path('get_image_names_by_loc/<long>/<lat>/<count>/', views.get_image_names_by_loc,
         name='get_image_names_by_loc'),
    path('get_image_metadata/<image_base_name>/', views.get_image_metadata, name='get_image_metadata'),
    path('get_next_images_for_annot/<annot_name>/<count>/', views.get_next_images_for_annot,
         name='get_next_images_for_annot'),
    path('get_all_routes/', views.get_all_routes, name='get_all_routes'),
    path('get_route_info/<route_id>/', views.get_route_info, name='get_route_info'),
    path('get_annotation_set/', views.get_annotation_set, name='get_annotation_set'),
    path('save_annotations/', views.save_annotations, name='save_annotations'),
    path('get_image_annotations/<image_base_name>/', views.get_image_annotations, name='get_image_annotations'),

]
