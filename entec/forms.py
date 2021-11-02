from django import forms
from entec.models import Game

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['subject']

