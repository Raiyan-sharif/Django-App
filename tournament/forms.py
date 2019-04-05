from django import forms
from django.forms import ModelForm
from .models import Tournament


class TournamentForm(ModelForm):
    class Meta:
        model = Tournament
        fields = ['tornament_name', 'start_date', 'end_date', 'poster', 'is_accepted', 'capacity', 'host_id', 'enrty_fee_with_per_hour_charge', 'zone_location', 'category_type', 'tournament_type', 'prize_worth']

