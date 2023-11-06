from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import authenticate,login,logout


from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage

from .form import RegisterForm
from .tokens import account_activation_token
from .models import Accounts
from datetime import datetime as dt
import json

# Create your views here.

def calc_amt(QuerySet):
    amt = 0
    for i in QuerySet.iterator():
        amt += int(i['amount'])
    return amt

def home(req):
    if req.user.is_authenticated:
        total_amt_db = Accounts.objects.filter(user=req.user).values("amount")
        total_amt = calc_amt(total_amt_db)
        
        now_month_db = Accounts.objects.filter(date__month=dt.now().month).filter(date__year=dt.now().year).values("amount")
        month_amt = calc_amt(now_month_db)
        
        now_today_db = Accounts.objects.filter(date__day=dt.now().day).filter(date__month=dt.now().month).filter(date__year=dt.now().year).values("amount")
        today_amt = calc_amt(now_today_db)

        return render(req, "index.html", {"total":total_amt,"month":month_amt,"today":today_amt})
    else:
        return redirect('signin')

def accounts(req):
    if req.user.is_authenticated:
        return render(req, "accounts.html")
    else:
        return redirect('signin')
    
def get_amt(req):
    if req.headers.get("x-requested-with") == "XMLHttpRequest":
        if req.user.is_authenticated:
            data = json.load(req)
            y,m,d = int(data['y']), int(data['m']), int(data['d'])
            date = dt(y,m,d)
            day_amt_db = Accounts.objects.filter(date__day=date.day).filter(date__month=date.month).filter(date__year=date.year).values("amount")
            day_amt = calc_amt(day_amt_db)
            print(str(date).split()[0]," : ",day_amt)
            return JsonResponse({"amt":day_amt},status=200)
        else:
            return JsonResponse({"amt":0},status=200)

def accountList(req, month, date, year):
    if req.user.is_authenticated:
        if req.method=="POST":
            reason = req.POST["reason"]
            amt = req.POST["amount"]
            period = dt(year, month, date)
            ac = Accounts(user=req.user,date=period,reason=reason,amount=amt)
            ac.save()
        acTable = Accounts.objects.filter(date=dt(year,month,date))
        return render(req, "accountList.html", {"acTable":acTable})
    else:
        return redirect('signin')

def activateEmail(req, user, mailTo):
    mail_subject = "Activate your user account"
    message = render_to_string("template_activate_account.html",{
        'user':user.username,
        'domain': get_current_site(req).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if req.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[mailTo])
    if email.send():
        messages.success(req, f'Dear <b>{user}</b>, please go to you email <b>{mailTo}</b> inbox and click on \
        received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        message.error(req, "something went wrog while attempt to send conformation mail. please try again later.")


def signup(req):
    form = RegisterForm()
    if req.method == "POST":
        form = RegisterForm(req.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activateEmail(req, user, form.cleaned_data.get("email"))
            return redirect("signin")
    return render(req, "signup.html", {"form":form})


def activate(req, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user=None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active=True
        user.save()
        messages.success(req, "Your email is verified. you can log in now")
        return redirect("signin")
    return redirect('/')

def signin(req):
    if req.user.is_authenticated:
        return redirect("/")
    else:
        if req.method == "POST":
            u = req.POST.get("username")
            p = req.POST.get("password")
            user = authenticate(req, username=u, password=p)
            if user is not None:
                login(req, user)
                messages.success(req, "Welcome "+u+" !!!")
                return redirect("/")
            else:
                messages.error(req, "Invalid Login details")
                return redirect('signin')
    return render(req, "signin.html")

def signout(req):
    if req.user.is_authenticated:
        logout(req)
        messages.success(req, "Logout sucessfully")
        return redirect("signin")
    else:
        messages.warning(req,"you must login before log out")
        return redirect("signin")
