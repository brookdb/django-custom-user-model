from django.urls import path
from .import views
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    path('signup/', views.signup_view, name="signup"), #signup page
    path('login/', views.login_view, name="login"), #login page
    path('logout/', views.logout_view, name="logout"), #logout
    path('dashboard/<user_id>', views.dashboard_view, name="dashboard"),
    path('activate/<ID>/<encID>/',views.activate, name='activate'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='passwords/password_reset_done.html'), name='password_reset_done'),
    #path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="passwords/password_reset_confirm.html"), name='password_reset_confirm'),
    #path('change_password/<uid>', views.passwordChangeView, name='password_change'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView, name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='passwords/password_reset_complete.html'), name='password_reset_complete'),
    path("password_reset", views.password_reset_request, name="password_reset")

]
