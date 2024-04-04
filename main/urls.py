from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('settings', views.settings, name="settings"),
    path('create', views.RSSFormView.as_view(), name="create"),
    path('<int:pk>/delete', views.delete, name="rss-delete")
]
