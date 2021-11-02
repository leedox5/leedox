from django.urls import path

from . import views

app_name = "entec"

urlpatterns = [
    path('', views.index, name="index"),
    path('detail', views.detail, name="detail"),
    path('game/create', views.game_create, name="game_create"),
    path('player/create', views.player_create, name="player_create"),
]