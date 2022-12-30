from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('admins', views.admins, name='admins'),
    path("admins/create_admin", views.create_admin, name="create_admin"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("profile/edit/<int:user_id>", views.profile_update, name="profile_update"),
    path("admins/edit_admin/<int:user_id>", views.edit_admin, name="edit_admin"),
    path("admins/admin_edited/<int:user_id>", views.admin_edited, name="admin_edited"),
    path("admins/delete_admin/<int:user_id>", views.delete_admin, name="delete_admin"),
    path("admins/batch_delete", views.batch_delete, name="batch_delete"),
]