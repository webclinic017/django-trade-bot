from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

from .models import Member ,Team, User
from .forms import RegistrationForm, AuthenticationForm, ProfileForm, TeamForm, DeleteTeamForm
from .managers import TeamManager

from crypto.managers import BinanceManager

binanceManager = BinanceManager()

#https://api.binance.com/api/v1/exchangeInfo

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  
            user.save()

            # load the profile instance created by the signal
            raw_password = form.cleaned_data.get('password1')
 
            # login user after signing up
            user = authenticate(username=user.username, password=raw_password)
            auth_login(request, user)
 
            return redirect('index')
    else:
        form = RegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def login(request):
    if request.method == 'POST':
    
        username = request.POST['username']
        password = request.POST['password']

        # login
        user = authenticate(username=username, password=password)
        auth_login(request, user)
        return redirect('index')

    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})

@login_required(login_url='/login/')
def logout(request):
    auth_logout(request)
    return redirect('index')



@login_required(login_url='/login/')
def withdraws(request):
    
    user = request.user
    withdraws = binanceManager.get_subaccount_withdraws(email=user.email)

    return render(request, 'accounts/withdraws.html', {'withdraws': withdraws})


@login_required(login_url='/login/')
def orders(request):

    user = request.user
    orders = binanceManager.get_subaccount_deposits(email=user.email)

    return render(request, 'accounts/orders.html', {'orders': orders})

@login_required(login_url='/login/')
def profile(request):
    user = request.user

    if request.method == "POST":
        profileForm = ProfileForm(request.POST, instance=request.user)

        if profileForm.is_valid():
            user = profileForm.save()
            user.save()
            # redirect user
            return redirect('profile')
    else:
        profileForm = ProfileForm(instance=user)
        teamForm    = TeamForm(instance=user.team)
        deleteTeamForm = {}
        deleteTeamForm = DeleteTeamForm(instance=user.team)
    return render(request, 'accounts/profile.html', {'profileForm': profileForm, 'teamForm': teamForm, 'deleteTeamForm': deleteTeamForm})

# POST request to create team
@login_required(login_url='/login/')
def create_team(request):
    user = request.user
    teamManager = TeamManager()

    if request.method == "POST":
        teamForm    = TeamForm(request.POST, request.FILES)

        if teamForm.is_valid():
            team = Team()
            team = teamForm.save(commit=False)
            teamManager.create_team(user, team)
            print(team, user)

            return redirect('profile')
        else:

            for field in teamForm:
                for error in field.errors:
                    messages.error(request, error)

            return redirect('profile')
    else:
        return redirect('profile')

@login_required(login_url='/login/')
def delete_team(request):
    user = request.user
    if request.method == "POST":

        deleteTeamForm    = TeamForm(request.POST, instance=user.team)
        if deleteTeamForm.is_valid():
            if user.team.owner == user:
                team = user.team
                team.delete()
            else:
                # remove from team
                pass
        return redirect('profile')
    else:
        return redirect('profile')

@login_required(login_url='/login/')
def join_team(request, pk):
    user = request.user
    team = get_object_or_404(Team, pk=pk)
    if team.public:

        print("adding user to team")
        teamManager = TeamManager()
        teamManager.add_member(user, team)
        
    return redirect('profile')

@login_required(login_url='/login/')
def abandon_team(request, pk):
    user = request.user
    team = get_object_or_404(Team, pk=pk)
    if user != team.owner and get_object_or_404(Member, user=user):

        teamManager = TeamManager()
        teamManager.remove_member(user, team)
        
    return redirect('profile')



