from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime
import uuid

# Create your models here.

User = get_user_model()

class Plan(models.Model):
    plan_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    investment_range_min = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    investment_range_max = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    earning_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    id_user = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    Withdrawal_address = models.CharField(max_length=100, default='', blank=True)
    selected_plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.PositiveIntegerField(blank=True, null=True)
    total_balance = models.PositiveIntegerField(blank=True, null=True)
    total_invested_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_withdrawn_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_deposited_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_earning_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    referral_link = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.user.username
      
class Setting(models.Model):
    pass
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='setting')
    # password = models.CharField(max_length=100)
    # Withdrawal_address = models.CharField(max_length=100)
    # username = models.CharField(max_length=100)

    # def __str__(self):
    #     return self.user.username


class Transaction(models.Model):
    PAYMENT_STATUS = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transaction')
    transaction_type = models.CharField(max_length=100)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS, default='Pending')
    timestamp = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"

class Deposit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deposit')
    proofOfPayment = models.ImageField(upload_to='proofs/')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    timestamp = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"Deposited {self.pk} - User {self.user.username}"

class DepositAdd(models.Model):
    deposit_address = models.TextField(default='hcbgfvjyhvcazgcjbvgfcgBNCFGv')
    

    def __str__(self):
        return self.deposit_address
    
class Earned(models.Model):
    PAYMENT_STATUS = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='earned')
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS, default='Approved')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    timestamp = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"Earned {self.pk} - User {self.user.username}"

class Withdrawal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='withdrawal')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    timestamp = models.DateTimeField(default=datetime.now)

    def approve(self):
        self.status = 'approved'
        self.save()

    def __str__(self):
        return f"Withdrawal by {self.user.username} - {self.amount}"

class Investments(models.Model):
    PAYMENT_STATUS = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Investments')
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS, default='Approved')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    timestamp = models.DateTimeField(default=datetime.now)
    
    def __str__(self):
        return f"Investment {self.pk} - User {self.user.username}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.subject}"
