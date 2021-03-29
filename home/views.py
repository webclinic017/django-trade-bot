from django.conf import settings
from django.utils import timezone

from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import Http404

from .models import Poll
from accounts import models as accounts

from datetime import date, timedelta, datetime

from crypto.managers import BinanceManager
binanceManager = BinanceManager()

def slice_per(source, step):
    return [source[i::step] for i in range(step)]


def index(request):
    top_daily = accounts.User.objects.all()

    info = binanceManager.get_exchange_info()
    symbols = binanceManager.get_tradeable_symbols()

    return render(request, 'home/index.html', {
        'info': info,
        'symbols': symbols,
        'top_daily': top_daily
    })


def markets(request):
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    teams_a = accounts.Team.get_daily_global()
    teams_b = accounts.Team.get_weekly_global()
    teams_c = accounts.Team.get_monthly_global()
       
        
    data = {
        "market_objects": {
            "data": [],     
            "pages": None,    
            "page": page,   
        },
        'teams': teams,
        
        'top_daily': teams_a ,
        'top_weekly': teams_b,
        'top_monthly': teams_c,
        
    }
    print(data)

    p = Paginator(data["market_objects"]["data"], 20)
    data["paginator"] = p

    return render(request, 'home/markets.html', data)


def teams(request):
    per_page = 10
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 0

    #setup teams
    teams_a = accounts.Team.objects.all()

    paginator = Paginator(teams_a, per_page)
    pages = paginator.page(page)

    data = {
        "teams": [pages.object_list],
        "top_daily": [],
        "top_weekly": [],
        "top_monthly": [],
    }

    print(data)
    return render(request, 'home/teams.html', data)

def detail(request, poll_id):
    try:
        p = Poll.objects.get(pk=poll_id)
    except Poll.DoesNotExist:
        raise Http404("Poll does not exist")
    return render(request, 'home/detail.html', {'poll': p})

