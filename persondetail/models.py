from django.db import models
from tournament.models import Tournament
from accounts.models import PlayerModel


class PersonDetail(models.Model):
    playerinstance = models.ForeignKey(PlayerModel, on_delete=models.SET_NULL, null=True, blank=True)
    tounament_detail = models.ForeignKey(Tournament, on_delete=models.SET_NULL,  null=True, blank=True)
