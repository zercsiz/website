from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.user_registration_view, name='user_registration'),
    path('login/', views.login_view, name='user_login'),
    path('logout/', views.logout_view, name='user_logout'),
    path('details/', views.account_details_view, name='account_details'),
    path('edit/', views.account_edit_view, name='account_edit'),

    #password reset urls
    path('password_change/done/',
         views.auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'),
         name='password_change_done'),

    path('password_change/',
         views.auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html'),
         name='password_change'),

    path('password_reset/done/',
         views.auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_done.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         views.auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/', views.auth_views.PasswordResetView.as_view(), name='password_reset'),

    path('reset/done/',
         views.auth_views.PasswordResetCompleteView.as_view
         (template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete'),

]
