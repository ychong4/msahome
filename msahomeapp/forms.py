from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from allauth.account.signals import user_signed_up
from django.dispatch import receiver

from .models import *


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('referee_id', 'username', 'last_name', 'first_name', 'address', 'city', 'state', 'zip', 'email', 'phone')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('referee_id', 'username', 'last_name', 'first_name', 'address', 'city', 'state', 'zip', 'email', 'phone')

class MatchForm(forms.ModelForm):
   class Meta:
       model = Match
       fields = ('home_team_score', 'guest_team_score', 'referee_comment', 'match_detail')


class PlayerForm(forms.ModelForm):
   class Meta:
       model = Player
       fields = ('player_ID', 'player_last_name', 'player_first_name', 'player_address', 'player_city', 'player_state', 'player_zip', 'player_email', 'player_phone', 'player_school_ID', 'player_team_ID', 'eligibility_status')

class ScoresForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = ['email']
