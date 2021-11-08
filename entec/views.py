from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from entec.forms import GameForm

from entec.models import Game, Match

# Create your views here.
def index(request):
    """
    매치 목록 출력
    """
    game_list = Game.objects.order_by("-create_date")
    context = {'game_list':game_list}
    return render(request, "entec/game_list.html", context)

def detail(request, game_id):
    game = Game.objects.get(id=game_id)
    """
    match_list = [
        ['1', 'AB:CD', '6:3'],
        ['2', '13:24', '3:6'],
    ]
    """
    context = {'game': game }
    return render(request, "entec/game_detail.html", context)

def game_create(request):
    if request.method == "POST":
        form = GameForm(request.POST)
        if form.is_valid():
            game = form.save(commit=False)
            game.create_date = timezone.now()
            game.save()
            return redirect("entec:index")
    else:
        form = GameForm()
    context = {'form': form}
    return render(request, "entec/game_form.html", context)

def player_create(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    game.player_set.create(name=request.POST.get('name'), create_date=timezone.now())
    return redirect("entec:detail", game_id=game.id)

def match_create(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    player1 = game.player_set.all()[0]
    player2 = game.player_set.all()[1]
    player3 = game.player_set.all()[2]
    player4 = game.player_set.all()[3]

    desc  = player1.name + "," + player2.name + ":" + player3.name + "," + player4.name
    match = Match(game=game, seq=1, player1=player1, player2=player2, player3=player3, player4=player4, desc=desc, create_date=timezone.now())
    match.save()

    desc  = player1.name + "," + player3.name + ":" + player2.name + "," + player4.name
    match = Match(game=game, seq=2, player1=player1, player2=player3, player3=player2, player4=player4, desc=desc, create_date=timezone.now())
    match.save()

    desc  = player1.name + "," + player4.name + ":" + player2.name + "," + player3.name
    match = Match(game=game, seq=3, player1=player1, player2=player4, player3=player2, player4=player3, desc=desc, create_date=timezone.now())
    match.save()

    return redirect("entec:detail", game_id=game.id)

def match_save(request, match_id):
    match = get_object_or_404(Match, pk=match_id)
    match.score = request.POST.get("no1") + ":" + request.POST.get("no2")
    match.save()
    
    score1 = request.POST.get("no1")
    score2 = request.POST.get("no2")

    if match.seq == 1:
        save_player_score_1(match.player1, int(score1), int(score2))
        save_player_score_1(match.player2, int(score1), int(score2))
        save_player_score_1(match.player3, int(score2), int(score1))
        save_player_score_1(match.player4, int(score2), int(score1))

    if match.seq == 2:
        save_player_score_2(match.player1, int(score1), int(score2))
        save_player_score_2(match.player2, int(score1), int(score2))
        save_player_score_2(match.player3, int(score2), int(score1))
        save_player_score_2(match.player4, int(score2), int(score1))

    if match.seq == 3:
        save_player_score_3(match.player1, int(score1), int(score2))
        save_player_score_3(match.player2, int(score1), int(score2))
        save_player_score_3(match.player3, int(score2), int(score1))
        save_player_score_3(match.player4, int(score2), int(score1))

        players = []
        players.append(match.player1)
        players.append(match.player2)
        players.append(match.player3)
        players.append(match.player4)

        players_sorted = sorted(players, key=lambda p : (p.win_ma, p.win_ga), reverse=True)

        scores = []
        for row in players_sorted:
            scores.append(row.sum_ga)
        
        ranks = []
        for score in scores:
            ranks.append(scores.index(score) + 1)

        players_sorted[0].game_rank = ranks[0];
        players_sorted[0].save()

        players_sorted[1].game_rank = ranks[1];
        players_sorted[1].save()

        players_sorted[2].game_rank = ranks[2];
        players_sorted[2].save()

        players_sorted[3].game_rank = ranks[3];
        players_sorted[3].save()


    return redirect("entec:detail", game_id=match.game.id)

def get_win_ma(player):
    win_ma = 0
    if player.score_01 > player.score_11:
        win_ma  = 1
    if player.score_02 is not None:        
        if player.score_02 > player.score_12:
            win_ma += 1
    if player.score_03 is not None:            
        if player.score_03 > player.score_13:
            win_ma += 1
    return win_ma

def get_los_ma(player):
    los_ma = 0
    if player.score_01 < player.score_11:
        los_ma  = 1
    if player.score_02 is not None:
        if player.score_02 < player.score_12:
            los_ma += 1
    if player.score_03 is not None:            
        if player.score_03 < player.score_13:
            los_ma += 1
    return los_ma

def save_player_score_1(player, score1, score2):
    player.score_01 = score1
    player.score_11 = score2
    player.win_ga = (player.score_01 or 0) + (player.score_02 or 0) + (player.score_03 or 0)
    player.los_ga = (player.score_11 or 0) + (player.score_12 or 0) + (player.score_13 or 0)
    player.sum_ga = player.win_ga - player.los_ga
    
    player.win_ma = get_win_ma(player)
    player.los_ma = get_los_ma(player)

    player.save() 

def save_player_score_2(player, score1, score2):
    player.score_02 = score1
    player.score_12 = score2
    player.win_ga = (player.score_01 or 0) + (player.score_02 or 0) + (player.score_03 or 0)
    player.los_ga = (player.score_11 or 0) + (player.score_12 or 0) + (player.score_13 or 0)
    player.sum_ga = player.win_ga - player.los_ga

    player.win_ma = get_win_ma(player)
    player.los_ma = get_los_ma(player)

    player.save() 

def save_player_score_3(player, score1, score2):
    player.score_03 = score1
    player.score_13 = score2
    player.win_ga = (player.score_01 or 0) + (player.score_02 or 0) + (player.score_03 or 0)
    player.los_ga = (player.score_11 or 0) + (player.score_12 or 0) + (player.score_13 or 0)
    player.sum_ga = player.win_ga - player.los_ga

    player.win_ma = get_win_ma(player)
    player.los_ma = get_los_ma(player)

    player.save() 

def t(request):
    context = {
        "data" : [1, 2, 3, 4],
    }
    return render(request, "entec/t.html", context)
