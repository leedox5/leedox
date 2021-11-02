from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "entec/game_list.html")

def detail(request):
    return render(request, "entec/game_detail.html")

def game_create(request):
    return render(request, "entec/game_form.html")

def player_create(request):
    return render(request, "entec/player_form.html")
