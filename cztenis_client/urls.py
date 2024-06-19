"""cztenis_client URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path, include

from .urls_views import searchPlayerView
from .urls_views import playerProfileView

from .urls_views import publicViews
from .urls_views import cztenisScraperView

from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

handler404 = publicViews.handler404
handler500 = publicViews.handler500

urlpatterns = [

    # path('admin/', admin.site.urls),
    # url(r'^', include('favicon.urls')),
    path('', publicViews.index, name = "index"),
    path('about', publicViews.about, name = "about"),

    
    path('turnaje/', publicViews.future_tournaments, name = "tournaments"),
    path('turnaje', publicViews.future_tournaments, name = "tournaments"),
    
    path('turnaje/<str:category>/', publicViews.future_tournaments_by_category, name = "tournaments"),
    path('turnaje/<str:category>', publicViews.future_tournaments_by_category, name = "tournaments"),
    
    path('hrac/<str:id>', playerProfileView.player_rankings, name = "player"),
    path('hrac/<str:id>/', playerProfileView.player_rankings, name = "player"),

    path('hrac/<str:id>/sezona', playerProfileView.player_season, name = "player"),
    path('hrac/<str:id>/sezona/', playerProfileView.player_season, name = "player"),

    path('hrac/<str:id>/historieZapasu', playerProfileView.player_match_history, name = "player"),
    path('hrac/<str:id>/historieZapasu/', playerProfileView.player_match_history, name = "player"),

    path('hrac/<str:id>/turnaje', playerProfileView.player_tournaments, name = "player"),
    path('hrac/<str:id>/turnaje/', playerProfileView.player_tournaments, name = "player"),

    path('hrac/<str:id>/H2H', playerProfileView.player_H2H, name = "player"),
    path('hrac/<str:id>/H2H/', playerProfileView.player_H2H, name = "player"),

    path('hrac/<str:id>/partneri', playerProfileView.player_partners, name = "player"),
    path('hrac/<str:id>/partneri/', playerProfileView.player_partners, name = "player"),

    path('hrac/<str:id>/zebricek', playerProfileView.player_rankings, name = "player"),
    path('hrac/<str:id>/zebricek/', playerProfileView.player_rankings, name = "player"),


    path('hledat/<str:name>', searchPlayerView.search_player, name = "search_player"),
    path('hledat/<str:name>/', searchPlayerView.search_player, name = "search_player"),


    
    path('getSeason/<str:id>/<str:season>', cztenisScraperView.get_one_season, name = "get_one_season"),
    path('getRankings/<str:id>', cztenisScraperView.get_rankings, name = "get_rankings"),

    path('setPlayerFullyLoaded/<str:id>/<str:bool_value>', playerProfileView.set_fully_loaded, name = "set_fully_loaded"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
