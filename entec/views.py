from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from entec.forms import GameForm

from entec.models import Game

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
    context = {'game':game}
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
