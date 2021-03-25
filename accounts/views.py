from django.shortcuts import render, redirect
from django.http import Http404

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

from .models import Member, Team
from .forms import RegistrationForm, ProfileForm, TeamForm, DeleteTeamForm

from crypto.managers import BinanceManager
binanceManager = BinanceManager()

#https://api.binance.com/api/v1/exchangeInfo

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(user)
            user.refresh_from_db()  
            # load the profile instance created by the signal
            user.save()
            raw_password = form.cleaned_data.get('password1')
 
            # login user after signing up
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
 
            # redirect user to home page
            return redirect('index')
    else:
        form = RegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def withdraws(request):
    #temporary, use sub-accounts instead
    withdraws = binanceManager.get_withdrawal_history()

    return render(request, 'accounts/withdraws.html', {'withdraws': withdraws})


def orders(request):
    user = request.user
    #temporary, use sub accounts instead

    orders = binanceManager.get_subaccount_deposits(email=user.email)

    return render(request, 'accounts/orders.html', {'orders': orders})

@login_required(login_url='/login')
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
        teamForm    = TeamForm()
        deleteTeamForm = {}
        try:
            deleteTeamForm = DeleteTeamForm(instance=user.team)
        except:
            deleteTeamForm = None
            pass
    return render(request, 'accounts/profile.html', {'profileForm': profileForm, 'teamForm': teamForm, 'deleteTeamForm': deleteTeamForm})

# POST request to create team
@login_required(login_url='/login')
def create_team(request):
    user = request.user
    if request.method == "POST":
        teamForm    = TeamForm(request.POST, request.FILES)

        if teamForm.is_valid():
            team = Team()            
            team = teamForm.save()

            #TODO: fix this portion
            # team.objects.create_team(user, team) 
            #
            # we add our user as owner of this team
            team.owner = user
            
            # next we set the team members to the owner only, people get added later on if they join.
            team.members.add(user)
            team.save()

            #redirect user
            return redirect('profile')
        else:
            for field in teamForm:
                for error in field.errors:
                    messages.error(request, error)

            return redirect('profile')
    else:
        return redirect('profile')

# POST request to delete team if the owner, or leave
@login_required(login_url='/login')
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



