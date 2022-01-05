from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .import views

urlpatterns = [
    path('', views.landing, name="landing"),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls'))

]

urlpatterns += staticfiles_urlpatterns()
