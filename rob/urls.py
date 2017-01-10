from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

# Additional imports for users:
from django.conf.urls import include
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^register/$',views.register, name='register'),
]
