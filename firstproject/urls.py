from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from myapp import views

urlpatterns = [
    path('callback', views.callback),
    path('admin/',admin.site.urls),
    path('view', views.view),
    path('update', views.update),
    path('end', views.end),
]
