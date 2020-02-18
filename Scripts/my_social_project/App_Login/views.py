from django.shortcuts import render,HttpResponseRedirect
from App_Login.forms import CreateNewUser,UserLogin, EditProfile
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse,reverse_lazy
from.models import UserProfile
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages

# Create your views here.

def sign_up(request):
    form = CreateNewUser()
    registered = False
    if request.method == 'POST' :
        form = CreateNewUser(data=request.POST)
        if form.is_valid():
            user =form.save()
            registered = True
            user_profile = UserProfile(user=user)
            user_profile.save()
            return redirect('app_login:login')
    return render(request, 'signup.html', context={'title':'Sign up.Social', 'form':form})


def login_page(request):
    form = UserLogin()
    if request.method == 'POST':
        form = UserLogin(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user=authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('App_posts:home')
    return render(request, 'login.html', context={'title':'login', 'form':form} )


@login_required
def edit_profile(request):
    current_user = UserProfile.objects.get(user=request.user)
    form = EditProfile(instance=current_user)
    if request.method == 'POST':
        form = EditProfile(request.POST, request.FILES, instance=current_user)
        if form.is_valid():
            form.save(commit=True)
            form =EditProfile(instance=current_user)
            return redirect('app_login:profile')
    return render(request, 'profile.html', context={'form':form})

@login_required
def Logout_user(request):
    logout(request)
    return redirect('app_login:login')

@login_required
def profile(request):
    return render(request, "user.html")

