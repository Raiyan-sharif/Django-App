from django.db import models
from datetime import date
from django.utils import timezone
import datetime
from accounts.models import (
 PlayerModel, ClubModel, GoverningBody,UserModel)


class Tournament(models.Model):
    tornament_name = models.CharField(max_length=200)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    poster = models.ImageField(upload_to='tournament_poster/', null=True, blank=True)
    creation_date = models.DateField(default=date.today, editable=False)
    is_accepted = models.BooleanField(default=False, choices=[(True, 'Yes'), (False, 'No')])
    capacity = models.PositiveIntegerField()
    host_id = models.ForeignKey(
        UserModel,
        related_name='host',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    enrty_fee_with_per_hour_charge = models.PositiveIntegerField()
    zone_location = models.CharField(max_length=100)
    category_type = models.CharField(max_length=100)
    tournament_type = models.CharField(max_length=100)
    prize_worth = models.CharField(max_length=255)

    def __str__(self):
        return self.tornament_name

    @property
    def upcomming_tournament(self):
        # print(datetime.datetime.utcnow())
        # print(timezone.now())
        now = datetime.datetime.now()
        # ou = now.strftime("%Y-%m-%d %H:%M:%S")
        # print(datetime.datetime.strptime(str(datetime.datetime.utcnow()), '%Y-%m-%d %H:%M:%S'))
        # print(self.tornament_name)

        if self.start_date is not None:
            # print(self.start_date)
            if self.start_date.strftime("%Y-%m-%d %H:%M:%S") > now.strftime("%Y-%m-%d %H:%M:%S"):
                return True
            return False

        else:
            return False

    @property
    def ongoing_tournament(self):
        now = datetime.datetime.now()

        if self.start_date is not None:
            # print(self.start_date)
            if (self.start_date.strftime("%Y-%m-%d %H:%M:%S") <= now.strftime("%Y-%m-%d %H:%M:%S")) and \
                    (self.end_date.strftime("%Y-%m-%d %H:%M:%S") >= now.strftime("%Y-%m-%d %H:%M:%S")):
                return True
            return False

        else:
            return False

    @property
    def past_tournament(self):
        now = datetime.datetime.now()

        if self.start_date is not None:
            # print(self.start_date)
            if self.end_date.strftime("%Y-%m-%d %H:%M:%S") < now.strftime("%Y-%m-%d %H:%M:%S"):
                return True
            return False

        else:
            return False


class GamePlayer(models.Model):
    player = models.OneToOneField(PlayerModel, on_delete=models.CASCADE)
    is_invited = models.BooleanField(default=False)
    match_accepted = models.BooleanField(default=False)
    match_ended = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.player.user.username


class Score(models.Model):
    player = models.ForeignKey(PlayerModel, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    game = models.ForeignKey(GamePlayer, on_delete=models.CASCADE)
    is_winner = models.BooleanField(default=False)

    def __str__(self):
        return str(self.score)


class Match(models.Model):
    match_date = models.DateTimeField(auto_now_add=True)
    venue = models.ForeignKey(ClubModel, on_delete=models.CASCADE)
    playing_with = models.ManyToManyField('tournament.GamePlayer')
    race_to = models.IntegerField()
    scoring = models.ForeignKey(Score, on_delete=models.CASCADE)
    game_type = models.CharField(max_length=20, choices=[('Yes', 'Yes'), ('No', 'No')])
    game_mode = models.CharField(max_length=20, choices=[('Yes', 'Yes'), ('No', 'No')])




