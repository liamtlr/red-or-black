from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.template.context_processors import csrf
from django.shortcuts import render_to_response
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from .modeldir.models import *
from django.core.exceptions import ObjectDoesNotExist
import random
from django.db.models import Count
from .forms import SelectionForm
from django import template


def home(request):
    expired_rounds = Game.objects.get_expired_games()
    for game in expired_rounds:
        game.select_colour()
        winners = Selection.objects.get_winners(game.id, game.colour)
        current_user_winner = winners.filter(player_id=request.user.id)
        losers = Selection.objects.get_losers(game.id, game.colour)
        current_user_loser = losers.filter(player_id=request.user.id)
        if current_user_loser:
            messages.info(request, 'You have been eliminated from game ' + str(current_user_loser.first().game_id))
        if current_user_winner:
            game = get_object_or_404(Game, pk=current_user_winner.first().game_id)
            if winners.count() == 1:
                messages.info(request, 'You have won game ' + str(game.pk))
            else:
                messages.info(request, 'You are through to the next round in game ' + str(game.pk))
        for loser in losers:
            loser.set_loser(game.round_no)
        for winner in winners:
            winner.reset_winner()
        if winners.count() > 1:
            game.increment_round()
        else:
            game.end_game()
    first_round_games = Game.objects.get_first_round_games(request.user.id)
    pending_games = Game.objects.get_pending_games(request.user.id)
    print("!!!")
    print(pending_games)
    print(pending_games.first())
    gammme = Game.objects.get(pk=121)
    print(gammme.members)
    lost_games = Game.objects.get_lost_games(request.user.id)
    won_games = Game.objects.get_won_games(request.user.id)
    live_games = Game.objects.get_live_games(request.user.id)
    return render(request, 'home.html', { 'first_round_games': first_round_games, 'pending_games': pending_games, 'live_games': live_games, 'lost_games': lost_games, 'won_games': won_games })


def game_new(request):
    new_game = Game()
    player = get_object_or_404(Player, pk=request.user.id)
    new_game.create_game(player)
    return HttpResponseRedirect('/')

def view_game(request, pk):
    game = get_object_or_404(Game, pk=pk)
    end_time_string = game.return_end_time
    reds = Selection.objects.get_reds(game.id)
    blacks = Selection.objects.get_blacks(game.id)
    if game.round_no > 1:
        game = get_object_or_404(Game, pk=pk)
        game_data = game.get_game_data()
    else:
        game_data = zip([], [])
    try:
        selection = Selection.objects.get(player_id=request.user.id, game_id=pk, active=True)
    except Selection.DoesNotExist:
        selection = None
    return render(request, 'game/view.html', {'game': game, 'end_time_string': end_time_string, 'selection': selection, 'blacks': blacks, 'reds': reds, 'game_data': game_data})

def remove_game(request, pk):
    selection = get_object_or_404(Selection, game_id=pk, player_id=request.user.id)
    selection.hide_game()
    return HttpResponseRedirect('/')

def set_stake(request, pk):
    if request.method == "POST":
        selection_form = SelectionForm(request.POST)
        if selection_form.is_valid():
            selection = Selection()
            selection.create_selection(selection_form, request.user.id, pk)
            return redirect(view_game, pk = pk)
    else:
        game = get_object_or_404(Game, pk=pk)
        selection_form = SelectionForm()
        end_time_string = game.return_end_time
        reds = Selection.objects.get_reds(game.id)
        blacks = Selection.objects.get_blacks(game.id)
        selection = None
    return render(request, 'game/set_stake.html', {'game': game, 'end_time_string': end_time_string, 'selection': selection, 'blacks': blacks, 'reds': reds, 'selection_form': selection_form })

def join_game(request, pk, choice):
    game = get_object_or_404(Game, pk=pk)
    player = get_object_or_404(Player, pk=request.user.id)
    try:
        selection = Selection.objects.get(player_id=request.user.id, game_id=pk, active=True)
        selection.colour = choice
    except Selection.DoesNotExist:
        selection = Selection(game=game, player=player ,colour=choice)
    selection.save()
    print(selection)
    end_time_string = game.return_end_time
    return redirect(view_game, pk = pk)

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)
            player = Player.objects.create(user=new_user)
            return HttpResponseRedirect('/')

    else:
        form = RegistrationForm()

    token = {}
    token.update(csrf(request))
    token['form'] = form
    return render_to_response('registration/registration_form.html', token)

def registration_complete(request):
    return render_to_response('registration/registration_complete.html')
