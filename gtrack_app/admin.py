from django.contrib import admin
from .models import UserProfile, Debtor, Payment, Notification

# Register your models here.
admin.site.register(UserProfile)

class DebtorAdmin(admin.ModelAdmin):
    list_display = ['client_id', 'firstname', 'surname', 'address', 'phone', 'email', 'amount_owed', 'due_date'	]

admin.site.register(Debtor)

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['debtor_id', 'client_id', 'medium_of_payment', 'amount_payed', 'amount_owed', 'amount_left', 'date_payed'	]

admin.site.register(Payment)

class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'email_subject', 'email_message', 'recipient', 'time_sent', 'attachment']

admin.site.register(Notification)