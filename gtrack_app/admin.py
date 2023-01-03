from django.contrib import admin
from .models import UserProfile, Debtor

# Register your models here.
admin.site.register(UserProfile)

class DebtorAdmin(admin.ModelAdmin):
    list_display = ['client_id', 'firstname', 'surname', 'address', 'phone', 'email', 'amount_owed', 'due_date'	]

admin.site.register(Debtor)