from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum  # Import the Sum aggregation function
from core.models import Profile, Earned

class Command(BaseCommand):
    help = "Updates the user's total balance and earning balance daily"

    def handle(self, *args, **kwargs):
        # Get all user profiles
        profiles = Profile.objects.all()

        for profile in profiles:
            # Calculate the total earning amount for the day
            earned_today = Earned.objects.filter(user=profile.user, timestamp__date=timezone.now().date()).aggregate(sum_earned_today=Sum('amount'))['sum_earned_today']
            earned_today = earned_today or 0

            # Update the total earning balance
            profile.total_earning_balance += earned_today
            profile.save()

            # Update the total balance (total balance = total deposited - total withdrawn + total earning)
            total_balance = profile.total_deposited_balance - profile.total_withdrawn_balance + profile.total_earning_balance
            profile.total_balance = total_balance
            profile.save()
