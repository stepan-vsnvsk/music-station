from django.urls import path, include 
from django.contrib.auth import views as auth_views
from . import views


app_name = 'accounts'
urlpatterns = [
    path('home/', views.HomePageTemplateView.as_view(), name='home'),

    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(
        template_name = "accounts/registration/login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name = "accounts/registration/reset_password.html"),\
        name ='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name = "accounts/registration/password_reset_done.html"),\
        name ='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(
        template_name = "accounts/registration/password_reset_form.html"),\
        name ='password_reset_confirm'),
    path('reset/done', auth_views.PasswordResetCompleteView.as_view(
        template_name = "accounts/registration/password_reset_complete.html"),\
        name ='password_reset_complete'),

    path('profile/<int:pk>', views.ProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/edit', views.EditProfileView.as_view(),\
     name='edit_profile'),    
    path('profile/<int:pk>/send_message', views.MessageCreateView.as_view(),\
     name='send_message'),
    path('profile/<int:pk>/messages', views.MessageListView.as_view(),\
     name='messages'),
]