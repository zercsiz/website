from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('register/', views.UserRegistrationView.as_view(), name='user_registration'),
    path('login/', views.LoginView.as_view(), name='user_login'),
    path('logout/', login_required(views.logout_view), name='user_logout'),
    path('details/', views.account_details_view, name='account_details'),
    path('edit/', views.account_edit_view, name='account_edit'),

    # password reset urls
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'),
         name='password_change_done'),

    path('password_change/',
         auth_views.PasswordChangeView.as_view(template_name='accounts/password_change.html'),
         name='password_change'),

    path('password_reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_done.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_pass_form.html'), name='password_reset_confirm'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset_form.html'),
         name='password_reset',),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view
         (template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete'),

]
