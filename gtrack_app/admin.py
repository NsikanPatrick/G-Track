from django.contrib import admin
from .models import UserProfile, Debtor, Payment, Notification

# Register your models here.
admin.site.register(UserProfile)

class DebtorAdmin(admin.ModelAdmin):
    list_display = ['id', 'client_id', 'firstname', 'surname', 'address', 'phone', 'email', 'amount_owed', 'due_date'	]

admin.site.register(Debtor, DebtorAdmin)

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'debtor_id', 'client_id', 'medium_of_payment', 'amount_payed', 'status', 'balance_left', 'date_payed'	]

admin.site.register(Payment, PaymentAdmin)

class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'email_subject', 'email_message', 'recipient', 'time_sent', 'attachment']

admin.site.register(Notification, NotificationAdmin)