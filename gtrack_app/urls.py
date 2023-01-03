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
    path("admins/batch_delete_admons", views.batch_delete_admins, name="batch_delete_admins"),
    path("all_clients", views.get_clients, name="all_clients"),
    path("all_clients/create_client", views.create_client, name="create_client"),
    path("clients/edit_client/<int:user_id>", views.edit_client, name="edit_client"),
    path("clients/client_edited/<int:user_id>", views.client_edited, name="client_edited"),
    path("clients/delete_client/<int:user_id>", views.delete_client, name="delete_client"),
    path("clients/batch_delete_clients", views.batch_delete_clients, name="batch_delete_clients"),
    path('debtors', views.debtors, name='debtors'),
    path("debtors/create_debtor", views.create_debtor, name="create_debtor"),
    path("debtors/edit_debtor/<int:user_id>", views.edit_debtor, name="edit_debtor"),
    path("debtors/debtor_edited/<int:user_id>", views.debtor_edited, name="debtor_edited"),
    path("debtors/batch_delete_debtors", views.batch_delete_debtors, name="batch_delete_debtors"),
]