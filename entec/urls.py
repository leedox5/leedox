from django.urls import path

from . import views

app_name = "entec"

urlpatterns = [
    path('', views.index, name="index"),
    path('<int:game_id>/', views.detail, name="detail"),
    path('game/create', views.game_create, name="game_create"),
    path('game/modify/<int:game_id>', views.game_modify, name="game_modify"),
    path('game/delete/<int:game_id>', views.game_delete, name="game_delete"),
    path('player/create/<int:game_id>', views.player_create, name="player_create"),
    path('player/delete/<int:player_id>', views.player_delete, name="player_delete"),
    path('match/create/<int:game_id>', views.match_create, name="match_create"),
    path('match/delete/<int:game_id>', views.match_delete, name="match_delete"),
    path('match/save/<int:match_id>', views.match_save, name="match_save"),
    path('t', views.t, name="t"),
]