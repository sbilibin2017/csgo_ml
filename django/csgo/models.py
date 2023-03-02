"""Django models."""

import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from psqlextra.indexes import UniqueIndex

MAX_LENGTH = 512
SCHEMA = "content"

DEFAULT_PARAMETERS = {"blank": True, "null": True}
BLANK_NULL_STR = {}
BLANK_NULL_STR.update(DEFAULT_PARAMETERS)
BLANK_NULL_STR["default"] = ""
BLANK_NULL_NONE = {}
BLANK_NULL_NONE.update(DEFAULT_PARAMETERS)
BLANK_NULL_NONE["default"] = None

# --------------------------------------------


class Map(models.Model):
    """Class for map model."""

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=MAX_LENGTH, **BLANK_NULL_STR)

    def __str__(self):
        return self.name

    class Meta:
        db_table = f'{SCHEMA}"."map'
        verbose_name = "Map"
        verbose_name_plural = "Maps"


class Team(models.Model):
    """Class for team model."""

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=MAX_LENGTH, **BLANK_NULL_STR)
    location = models.CharField(max_length=MAX_LENGTH, **BLANK_NULL_STR)

    def __str__(self):
        return self.name

    class Meta:
        db_table = f'{SCHEMA}"."team'
        verbose_name = "Team"
        verbose_name_plural = "Teams"


class Player(models.Model):
    """Class for player model."""

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=MAX_LENGTH, **BLANK_NULL_STR)
    birthday = models.DateField(null=True, blank=True)
    hometown = models.CharField(max_length=MAX_LENGTH, **BLANK_NULL_STR)
    nationality = models.CharField(max_length=MAX_LENGTH, **BLANK_NULL_STR)

    def __str__(self):
        return self.name

    class Meta:
        db_table = f'{SCHEMA}"."player'
        verbose_name = "Player"
        verbose_name_plural = "Players"    


class League(models.Model):
    """Class for league model."""

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=MAX_LENGTH, **BLANK_NULL_STR)

    def __str__(self):
        return self.name

    class Meta:
        db_table = f'{SCHEMA}"."league'
        verbose_name = "League"
        verbose_name_plural = "Leagues"


class Serie(models.Model):
    """Class for serie model."""

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=MAX_LENGTH, **BLANK_NULL_STR)
    tier = models.CharField(max_length=MAX_LENGTH, **BLANK_NULL_STR)

    def __str__(self):
        return self.name

    class Meta:
        db_table = f'{SCHEMA}"."serie'
        verbose_name = "Serie"
        verbose_name_plural = "Series"


class Tournament(models.Model):
    """Class for serie model."""

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=MAX_LENGTH, **BLANK_NULL_STR)
    prizepool = models.CharField(max_length=MAX_LENGTH, **BLANK_NULL_STR)

    def __str__(self):
        return self.name

    class Meta:
        db_table = f'{SCHEMA}"."tournament'
        verbose_name = "Tournament"
        verbose_name_plural = "Tournaments"


class Game(models.Model):
    """Class for game model."""

    id = models.IntegerField(primary_key=True)
    match_id = models.IntegerField()
    begin_at = models.DateTimeField()    
    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    team1 = models.ForeignKey(Team, related_name="team1_id", on_delete=models.CASCADE)
    team2 = models.ForeignKey(Team, related_name="team2_id", on_delete=models.CASCADE)

    players = models.ManyToManyField(Player, related_name='players', through="Team4Player")


    def __str__(self):
        return f'{self.team1} <-> {self.team2}'

    class Meta:
        db_table = f'{SCHEMA}"."game'
        verbose_name = "Game"
        verbose_name_plural = "Game"


class Round(models.Model):
    """Class for round model."""

    game = models.ForeignKey(Map, on_delete=models.CASCADE)
    ct = models.ForeignKey(Team, related_name="ct_id", on_delete=models.CASCADE)
    outcome = models.CharField(max_length=MAX_LENGTH, **BLANK_NULL_STR)
    round = models.IntegerField()
    t = models.ForeignKey(Team, related_name="t_id", on_delete=models.CASCADE)
    winner_team = models.ForeignKey(Team, related_name="winner_id", on_delete=models.CASCADE)


    def __str__(self):
        return f'round:{self.round} | ct:{self.ct} | t:{self.t}'

    class Meta:
        db_table = f'{SCHEMA}"."round'
        verbose_name = "Round"
        verbose_name_plural = "Rounds"


class Stat(models.Model):
    """Class for round model."""

    game = models.ForeignKey(Map, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    adr = models.FloatField()
    kills = models.IntegerField()
    assists = models.IntegerField()
    deaths = models.IntegerField()
    first_kills_diff = models.IntegerField()
    flash_assists = models.IntegerField()
    headshots = models.IntegerField()
    k_d_diff = models.IntegerField()
    kast =  models.FloatField()
    rating = models.FloatField()

    def __str__(self):
        return f'round:{self.round} | ct:{self.ct} | t:{self.t}'

    class Meta:
        db_table = f'{SCHEMA}"."stat'
        verbose_name = "Stat"
        verbose_name_plural = "Stats"


class Team4Player(models.Model):
    """Класс для описания жанров кинопроизведения."""

    game_id = models.ForeignKey(Game, related_name="game_id", on_delete=models.CASCADE)
    team = models.ForeignKey(Team, related_name="team_id", on_delete=models.CASCADE)
    player = models.ForeignKey(Player, related_name="player_id", on_delete=models.CASCADE)

    def __str__(self):
        return "Жанры кинопроизведения"

    class Meta:
        db_table = f'{SCHEMA}"."team4player'
        verbose_name = 'Team4Player'
        verbose_name_plural = 'Team4Players'
