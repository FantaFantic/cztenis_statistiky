from django.shortcuts import render
from cztenis_client.globalVariables import tenisScraperInstance

loaded_tournaments = {} # "category" : tournaments[]


def handler404(request, *args, **argv):
    return render(request, '404.html')


def handler500(request, *args, **argv):
    return render(request, '500.html')

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def future_tournaments(request):
    return render(request, 'future_tournaments.html')


def future_tournaments_by_category(request, category):

    scraper = tenisScraperInstance
    if(not category in loaded_tournaments):
        loaded_tournaments[category] = scraper.get_future_tournaments_by_category(category)

    return render(request, 'future_tournaments.html', {"category" : category, "found_tournaments" : loaded_tournaments[category]})
