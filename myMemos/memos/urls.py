from django.urls import path
from . import views

app_name = "memos"
urlpatterns = [
    path("", views.homePageView, name="front"),
    path('add/', views.addMemo,name="add"),
    path("changepassword/", views.changePassword, name="accept"),
    path('remove_oldest_memo/', views.removeOldestMemo, name='remove_oldest_memo'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
]