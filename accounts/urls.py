from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.user_registration_view, name='user_registration'),
    path('login/', views.login_view, name='user_login'),
    path('logout/', views.logout_view, name='user_logout'),
    path('details/', views.account_details_view, name='account_details'),
    path('edit/', views.account_edit_view, name='account_edit'),

]
