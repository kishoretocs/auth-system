from django.shortcuts import render, redirect
from django.contrib.auth.admin import User
from .forms import NewUserCreationForm,UserPasswordChangeForm,CustomAuthenticationForm
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required

def signup(request):
    if request.method == 'POST':
        form  = NewUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('login')
    else:
        form = NewUserCreationForm()
    return render(request, 'user/signup.html',{'form':form})


def Login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request.POST)  
        if form.is_valid():
            username_or_email = form.cleaned_data.get('username_or_email')
            password = form.cleaned_data.get('password')
            user = form.get_user()
            if user is not None:
                login(request, user)
                return redirect('dashboard')  
    else:
        form = CustomAuthenticationForm()
    return render(request, 'user/login.html', {'form': form})

def Logout(request):
    logout(request)
    return redirect('login')

@login_required
def change_password(request):
    if request.method=='POST':
        form = UserPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request,user)
            return redirect('dashboard')
    else:
        form = UserPasswordChangeForm(user=request.user)
    return render(request,'user/change_password.html',{'form':form})


@login_required
def profile_view(request):
    user = request.user
    return render(request, 'user/profile.html', {
        'username': user.username,
        'email': user.email,
        'date_joined': user.date_joined,
        'last_login': user.last_login
    })



@login_required
def dashboard_view(request):
    return render(request, 'user/dashboard.html')