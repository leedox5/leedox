from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from entec.forms import GameForm

from entec.models import Game, Match, Player

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

def game_modify(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    if request.method == "POST":
        form = GameForm(request.POST, instance=game)
        if form.is_valid():
            game =  form.save(commit=False)
            game.save()
            return redirect("entec:detail", game_id=game.id)
    else:
        form = GameForm(instance=game)
    context = { 'form' : form }
    return render(request, "entec/game_form.html", context)

def game_delete(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    game.delete()
    return redirect("entec:index")     

def player_create(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    cnt = game.player_set.all().count()
    game.player_set.create(name=request.POST.get('name'), create_date=timezone.now(), seq=cnt + 1)
    return redirect("entec:detail", game_id=game.id)

def player_delete(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    player.delete()
    return redirect("entec:detail", game_id=player.game_id)

def match_create(request, game_id):
    game = get_object_or_404(Game, pk=game_id)

    player_count = game.player_set.all().count()
    if player_count == 4:
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

    if player_count == 5:
        player1 = game.player_set.all()[0]
        player2 = game.player_set.all()[1]
        player3 = game.player_set.all()[2]
        player4 = game.player_set.all()[3]
        player5 = game.player_set.all()[4]

        # 1 2 : 3 4
        # 1 3 : 2 5
        # 1 4 : 3 5
        # 1 5 : 2 4
        # 2 3 : 4 5
        match_create_one(game, 1, player1, player2, player3, player4)
        match_create_one(game, 2, player1, player3, player2, player5)
        match_create_one(game, 3, player1, player4, player3, player5)
        match_create_one(game, 4, player1, player5, player2, player4)
        match_create_one(game, 5, player2, player3, player4, player5)

    return redirect("entec:detail", game_id=game.id)

def match_create_one(g, seq, p1, p2, p3, p4):
    desc = str(p1.seq) + p1.name + "," + str(p2.seq) + p2.name + ":" + str(p3.seq) + p3.name + "," + str(p4.seq) + p4.name
    match = Match(game = g, seq = seq, player1 = p1, player2 = p2, player3 = p3, player4 = p4, desc = desc, create_date = timezone.now())
    match.save()

def match_delete(request, game_id):
    game = get_object_or_404(Game, pk=game_id)

    for player in game.player_set.all():
        player.score_01 = 0
        player.score_11 = 0
        player.score_02 = 0
        player.score_12 = 0
        player.score_03 = 0
        player.score_13 = 0
        player.score_04 = 0
        player.score_14 = 0
        player.win_ma = 0
        player.los_ma = 0
        player.win_ga = 0
        player.los_ga = 0
        player.sum_ga = 0
        player.game_rank = 0
        player.save()

    for match in game.match_set.all():
        match.delete()
    return redirect("entec:detail", game_id=game.id)

def match_save(request, match_id):
    match = get_object_or_404(Match, pk=match_id)
    match.score = request.POST.get("no1") + ":" + request.POST.get("no2")
    match.save()
    
    score1 = request.POST.get("no1")
    score2 = request.POST.get("no2")

    save_player_score_4(match.player1, int(score1), int(score2))
    save_player_score_4(match.player2, int(score1), int(score2))
    save_player_score_4(match.player3, int(score2), int(score1))
    save_player_score_4(match.player4, int(score2), int(score1))

    players = Player.objects.filter(game_id=match.game_id)
    players_sorted = sorted(players, key=lambda p : (p.win_ma, p.win_ga), reverse=True)

    scores = []
    for row in players_sorted:
        scores.append(row.sum_ga)
    
    ranks = []
    for score in scores:
        ranks.append(scores.index(score) + 1)

    cnt = 0
    for player in players_sorted:
        player.game_rank = ranks[cnt];
        player.save()
        cnt = cnt + 1

    return redirect("entec:detail", game_id=match.game.id)

def get_win_ma(player):
    win_ma = 0
    if player.score_01 > player.score_11:
        win_ma  = 1
    if player.score_02 is not None and player.score_02 > 0:        
        if player.score_02 > player.score_12:
            win_ma += 1
    if player.score_03 is not None and player.score_03 > 0:            
        if player.score_03 > player.score_13:
            win_ma += 1
    if player.score_04 is not None and player.score_04 > 0:            
        if player.score_04 > player.score_14:
            win_ma += 1
    return win_ma

def get_los_ma(player):
    los_ma = 0
    if player.score_01 < player.score_11:
        los_ma  = 1
    if player.score_02 is not None and player.score_02 > 0:
        if player.score_02 < player.score_12:
            los_ma += 1
    if player.score_03 is not None and player.score_03 > 0:            
        if player.score_03 < player.score_13:
            los_ma += 1
    if player.score_04 is not None and player.score_04 > 0:            
        if player.score_04 < player.score_14:
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

def save_player_score_4(player, score1, score2):
    if player.score_01 is None or player.score_01 == 0:
        player.score_01 = score1
        player.score_11 = score2
        player.win_ga = player.score_01
        player.los_ga = player.score_11
    elif player.score_02 is None or player.score_02 == 0:
        player.score_02 = score1
        player.score_12 = score2
        player.win_ga = player.score_01 + player.score_02
        player.los_ga = player.score_11 + player.score_12
    elif player.score_03 is None or player.score_03 == 0:
        player.score_03 = score1
        player.score_13 = score2
        player.win_ga = player.score_01 + player.score_02 + player.score_03
        player.los_ga = player.score_11 + player.score_12 + player.score_13
    elif player.score_04 is None or player.score_04 == 0:
        player.score_04 = score1
        player.score_14 = score2
        player.win_ga = player.score_01 + player.score_02 + player.score_03 + player.score_04
        player.los_ga = player.score_11 + player.score_12 + player.score_13 + player.score_14

    player.sum_ga = player.win_ga - player.los_ga
    player.win_ma = get_win_ma(player)
    player.los_ma = get_los_ma(player)
    player.save()

def t(request):
    context = {
        "data" : [1, 2, 3, 4],
    }
    return render(request, "entec/t.html", context)
