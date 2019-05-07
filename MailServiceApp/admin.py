from django.contrib import admin

# Register your models here
from MailServiceApp.models import Mail, Account


class MailManager(admin.ModelAdmin):
    list_display = ('subject', 'text')

admin.site.register(Mail, MailManager)
admin.site.register(Account)