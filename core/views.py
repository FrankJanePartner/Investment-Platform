from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Profile, Setting, Investments, Withdrawal, Deposit, Transaction, Plan, DepositAdd, Earned, ContactMessage
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse, HttpResponseBadRequest
from decimal import Decimal


# Create your views here.
def index(request):
    return render(request, 'index.html')

def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/home/')
        else:
            error_message = "Invalid Username or Password"
            return render(request, 'pages-login.html', {'error_message':error_message})
    else:
        return render(request, 'pages-login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if not username or not password or not password2:
            error_message = "please fill all required fields"
            return render (request, "pages-register.html", {'error_message':error_message})

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('/signup/')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('/signup/')
            else:
                referral_link = f'www.littinvest.com/ref/{username}'
                user = User.objects.create_user(username=username, email=email, password=password)
                new_user = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=new_user, referral_link=referral_link)
                new_investment = Investments.objects.create(user=new_user)
                new_deposit = Deposit.objects.create(user=new_user)
                new_withdrawal = Withdrawal.objects.create(user=new_user)
                new_transaction = Transaction.objects.create(user=new_user)


                user.save()
                new_profile.save()
                new_investment.save()
                new_deposit.save()
                new_withdrawal.save()
                new_transaction.save()

                return redirect('/signin/')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('/signup/')
    else:
        return render(request, 'pages-register.html')

@login_required(login_url='/signin/')
def profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    transactions = Transaction.objects.filter(user=user)
    context = {
        'profile': profile,
        'transactions': transactions,
    }
    return render(request, 'users-profile.html', context)

@login_required
def signout(request):
    logout(request)
    return redirect('/signin/')

def planview(request):
    plans = Plan.objects.all()
    plan_data = []

    for plan in plans:
        plan_data.append({
            'id': plan.id,
            'name': plan.name,
            'investment_range_min': str(plan.investment_range_min),
            'investment_range_max': str(plan.investment_range_max),
            'earning_percentage': str(plan.earning_percentage),
        })

    return JsonResponse({'plans': plan_data})
    
@login_required(login_url='/signin/')
def home(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    transactions = Transaction.objects.filter(user=user)
    deposits = Deposit.objects.filter(user=user)
    withdrawals = Withdrawal.objects.filter(user=user)
    investments = Investments.objects.filter(user=user)
    context = {
        'profile': profile,
        'transactions': transactions,
        'deposits': deposits,
        'withdrawals': withdrawals,
        'investments': investments,
    }

    return render(request, 'Dashboard.html', context)

@login_required(login_url='/signin/')
def deposit(request):
    deposit_address = DepositAdd.objects.first()  # Fetch the deposit address
    if request.method == 'POST':
        amount = int(request.POST.get('amount') or 0)
        proof_of_payment = request.FILES.get('proof_of_payment')
        
        deposit = Deposit.objects.create(user=request.user, amount=amount, proofOfPayment=proof_of_payment)
        deposit.save()

        transaction = Transaction(user=request.user, transaction_type='Deposit', amount=deposit.amount, status="pending")
        transaction.save()

        messages.info(request, 'Deposite sent! Awaiting approval.')
        return render(request, 'deposit.html', {'deposit_address': deposit_address})
    return render(request, 'deposit.html', {'deposit_address': deposit_address})

@login_required(login_url='/signin/')
def withdrawal(request):
    if request.method == 'POST':
        amount = Decimal(request.POST.get('amount'))

        profile = Profile.objects.get(user=request.user)
        if profile.total_balance >= amount:
            # Get the user's investment
            investment = Investments.objects.filter(user=request.user).order_by('-timestamp').first()
            if investment:
                # Check if the investment is at least 180 days old
                if timezone.now() >= investment.timestamp + timedelta(days=180):
                    withdrawal = Withdrawal(user=request.user, amount=amount)
                    withdrawal.save()

                    # Update profile
                    profile.total_withdrawn_balance += withdrawal.amount
                    profile.total_balance -= withdrawal.amount
                    profile.save()

                    # Create transaction
                    transaction = Transaction(user=request.user, transaction_type='Withdrawal', amount=withdrawal.amount, status="pending")
                    transaction.save()

                    messages.info(request, 'Withdrawal request successful. Your request is pending approval.')
                else:
                    messages.info(request, 'Your investment is not yet eligible for withdrawal. Please wait for at least 180 days.')
            else:
                messages.info(request, 'You have not made any investments yet.')
        else:
            messages.info(request, 'Insufficient balance.')
        return render(request, 'withdrawal.html')
    else:
        return render(request, 'withdrawal.html')

@login_required(login_url='/signin/')
def invest(request):
    plans = Plan.objects.all()
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        amount = Decimal(request.POST.get('amount'))
        user_plans = request.POST.get('user_plans')

        investment = Investments.objects.create(user=request.user, amount=amount)
        investment.save()

        # Set selected_plan based on user_plans
        selected_plan = plans.get(name=user_plans)
        profile.selected_plan = selected_plan

        # Update profile
        profile.total_invested_balance += investment.amount
        profile.total_balance -= investment.amount
        profile.save()

        # Create transaction
        transaction = Transaction(user=request.user, transaction_type='Invested', amount=investment.amount, status="approved")
        transaction.save()

        earning_percentage = selected_plan.earning_percentage / 100
        earning_amount = amount * earning_percentage

        # Create Earned object
        earned = Earned.objects.create(user=request.user, amount=earning_amount)
        earned.save()

        # Update the total earning balance
        profile.total_earning_balance += earning_amount
        profile.save()

        # Create transaction
        transaction = Transaction(user=request.user, transaction_type='Earned', amount=earning_amount, status="approved")
        transaction.save()


        context = {
            'plans': plans,
            'profile':profile,
        }
        messages.info(request, 'Investment successful')
        return render(request, 'investment.html', context)
    else:
        context = {
            'plans': plans,
            'profile':profile,
        }
        plans = Plan.objects.all()
        return render(request, 'investment.html', context)


@login_required(login_url='/signin/')
def contact_form(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Save the contact message in the ContactMessage model
        contact_message = ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message,
        )

        messages.info(request, 'sent')
        return render(request, 'pages-contact.html')
    else:
        messages.info(request, ' Not sent')
        return render(request, 'pages-contact.html')

def home_faq(request):
    return render(request, 'faq.html')

@login_required(login_url='/signin/')
def faq(request):
    return render(request, 'pages-faq.html')

