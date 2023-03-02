"""Django admin panel."""

from csgo.models import (Game, League, Map, Player, Round, Serie, Stat, Team,
                         Team4Player, Tournament)
from django.contrib import admin


@admin.register(Map)
class MapAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


@admin.register(Serie)
class SerieAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'tier',)


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'prizepool',)


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'birthday', 'hometown',)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location',)


@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    list_display = ('ct', 't', 'round', 'outcome', 'winner_team',)


@admin.register(Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ('player', 'adr', 'kills', 'assists', 'deaths', 'first_kills_diff', 'flash_assists', 'headshots', 'k_d_diff', 'kast', 'rating',) 

# Кинопроизведение
class Team4PlayerInline(admin.TabularInline):
    model = Team4Player

# отображение жанров и персона в кинопроизведении
    

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    inlines = (Team4PlayerInline,)
    list_display = ('id', 'match_id', 'begin_at', 'map', 'league', 'serie', 'tournament', 'team1', 'team2', ) 

