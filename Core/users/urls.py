from django.urls import path
from .import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.signup_view, name="signup"), #signup page
    path('login/', views.login_view, name="login"), #login page
    path('logout/', views.logout_view, name="logout"), #logout
    path('dashboard/<user_id>', views.dashboard_view, name="dashboard"),
    path('activate/<ID>/<encID>/',views.activate, name='activate'),
]
