from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('admins', views.admins, name='admins'),
    path("admins/create_admin", views.create_admin, name="create_admin"),
    path("profile", views.profile, name="profile"),
    path("profile/edit", views.profile_update, name="profile_update"),
]