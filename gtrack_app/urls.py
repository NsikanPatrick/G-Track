from django.urls import path

from django.contrib.auth import views as auth_views

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
    path("debtors/debtors_bulk_actions", views.debtors_bulk_actions, name="debtors_bulk_actions"),
    path("debtors/send_notification/<int:user_id>", views.single_recipient, name="single_recipient"),
    path("debtors/send_mail", views.single_recipient_send_mail, name="single_recipient_send_mail"),
    path("debtors/send_notification", views.multiple_recipients, name="multiple_recipients"),
    path("debtors/send_bulk_email", views.multiple_recipient_send_mail, name="multiple_recipient_send_mail"),
    path('payments', views.payments, name='payments'),
    path("payments/create_payment", views.create_payment, name="create_payment"),
    path("payments/approve_payment/<int:user_id>", views.approve_payment, name="approve_payment"),
    path('analytics', views.analytics, name='analytics'),

    # CLIENT DASHBOARD URLS
    path("my_debtors/<int:user_id>", views.my_debtors, name="my_debtors"),
    path("my_payments/<int:user_id>", views.my_payments, name="my_payments"),
    path("my_payments/payments_bulk_actions", views.payments_bulk_actions, name="payments_bulk_actions"),
    path("my_analytics/<int:user_id>", views.my_analytics, name="my_analytics"),

    # RESETING PASSWORD VIA MAIL
    path("reset_password/", auth_views.PasswordResetView.as_view(), name="reset_password"),
    path("reset_password_sent/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset_password_complete/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]