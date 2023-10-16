from django.contrib import admin
from .models import Investments, Withdrawal, Deposit, Profile, Setting, Plan, Transaction, Earned, DepositAdd, ContactMessage


# Register your models here.


admin.site.register(Investments)
admin.site.register(Withdrawal)
admin.site.register(Deposit)
admin.site.register(Transaction)
admin.site.register(Earned)
admin.site.register(DepositAdd)
admin.site.register(Profile)
admin.site.register(Setting)
admin.site.register(Plan)
admin.site.register(ContactMessage)
