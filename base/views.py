from .forms import *
from .models import *
from hashlib import sha256
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
# Create your views here.


def home(request):
    return render(request, 'Home.html')


def Signup(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account Registration Successfull')
            return redirect('login')

    context = {'form': form}
    return render(request, 'Signup.html', context)


def Login(request):
    if not request.session.exists(request.session.session_key):
        print(request.session.session_key)
        request.session.create()
    print(request.session.session_key)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        valid_user = authenticate(
            request, username=username, password=password)
        if valid_user is not None:
            login(request, valid_user)
            return redirect('home')
        else:
            messages.info(request, "credentials incorrect")
    context = {}
    return render(request, 'Login.html', context)


def Profile_fun(request):

    return render(request, 'Profile.html')


def Logout_fun(request):
    logout(request)
    return redirect('login')


def hasher(text):
    if text is not None:
        return sha256(text.encode('ascii')).hexdigest()


def Updateprofile(request):

    paypass_one = request.POST.get('paypass1')
    paypass_two = request.POST.get('paypass2')
    user = request.user
    var = Profile.objects.get(user=user)
    form = Profilemodelform(instance=var)
    if paypass_one == paypass_two:

        if request.method == 'POST':
            form = Profilemodelform(request.POST, instance=var)

            if form.is_valid():
                instance = form.save(commit=False)
                paypass_one = hasher(paypass_one)
                print(paypass_one, 'From Update profile')
                instance.payment_password = paypass_one
                instance.save()
                return redirect('/')

    else:
        messages.success(request, "Password didn't match")

    context = {'form': form}
    return render(request, 'Updateprofile.html', context)


def Postlist(request):
    post_list = Post.objects.all()

    paginator_object = Paginator(post_list, 5)
    page_num = request.GET.get('page', 1)
    print(page_num)

    try:
        page = paginator_object.page(page_num)
    except EmptyPage:
        page = paginator_object.page(1)
    context = {'posts': page}
    return render(request, 'Posts.html', context)


def Postcreate(request):
    form = Postcreationform()
    if request.method == 'POST':
        form = Postcreationform(request.POST)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.profile = request.user.profile
            instance.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'Postcreate.html', context)


def Viewprofile(request, user_name):

    user = User.objects.get(username=user_name)
    profile = Profile.objects.get(user=user)
    posted = profile.post_set.all()
    context = {'profile': profile, 'posted': posted}
    return render(request, 'Viewprofile.html', context)


def Walletupdate_receiver(receiver_profile, instance):
    receiver_profile.wallet = receiver_profile.wallet + \
        int(instance.cash)
    receiver_profile.save(update_fields=['wallet'])
    print(receiver_profile.wallet)
    print(instance.cash)


def Walletupdate_sender(request, instance):
    sender_profile_wallet = request.user.profile.wallet
    return
# def authenticate_payment():


def Makepayments(request, user_name):
    form = PaymentForm()
    receiver_username = User.objects.get(username=user_name)
    receiver_profile = Profile.objects.get(user=receiver_username)
    # payment pass hash value finding
    paypass_from_form = request.POST.get('paypass')
    hasher_paypass = hasher(paypass_from_form)
    sender_payment_password = request.user.profile.payment_password
    # entry check
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if sender_payment_password == hasher_paypass:
            if form.is_valid():

                instance = form.save(commit=False)
                instance.sender_profile = request.user.profile
                instance.receiver_profile = receiver_profile
                if instance.sender_profile != instance.receiver_profile:
                    Walletupdate_receiver(receiver_profile, instance)
                    sender_profile = request.user.profile
                    sender_profile.wallet = sender_profile.wallet - \
                        int(instance.cash)
                    sender_profile.save(update_fields=['wallet'])
                    instance.save()
                    messages.success(request, 'Payment Successfull')
                    return redirect("viewprofile", receiver_username)
                else:
                    messages.error(request, 'Transaction Prohibited')
        else:
            messages.error(request, "Password didn't match")

    context = {'form': form, 'profile': receiver_profile}
    return render(request, 'Makepayments.html', context)
