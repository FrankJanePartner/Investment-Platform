from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Transaction, Profile, Investments #Earned
# from core.views import earning


@receiver(post_save, sender=Transaction)
def handle_User_transactions(sender, instance, created, **Kwargs):
    user = instance.user
    profile = Profile.objects.get(user=user)
    if instance.status == 'Approved':
        if instance.transaction_type == "Deposit": 
            profile.total_deposited_balance += instance.amount
            profile.total_balance += instance.amount
            profile.save()

# @receiver(post_save, sender=Investments)
# def investment_created(sender, instance, created, **kwargs):
#     if created:
#         earning(instance.user, instance.amount)
