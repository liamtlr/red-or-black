from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.template.context_processors import csrf
from django.shortcuts import render_to_response
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from datetime import datetime
from .modeldir.models import *
from django.core.exceptions import ObjectDoesNotExist



def home(request):
    games = Game.objects.filter(ends_at__gte=datetime.now())
    return render(request, 'home.html', {'games': games})

def game_new(request):
    new_game = Game()
    new_game.create_game()
    return HttpResponseRedirect('/')

def view_game(request, pk):
    game = get_object_or_404(Game, pk=pk)
    end_time_string = game.return_end_time
    try:
        selection = Selection.objects.filter(player_id=request.user.id, game_id=pk).first()
    except Selection.DoesNotExist:
        selection = None
    return render(request, 'game/view.html', {'game': game, 'end_time_string': end_time_string, 'selection': selection})

def join_game(request, pk, selection):
    game = get_object_or_404(Game, pk=pk)
    player = get_object_or_404(Player, pk=request.user.id)
    selection = Selection(game=game, player=player ,colour=selection)
    selection.save()
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
            player = Player()
            player.user = new_user
            player.save()
            return HttpResponseRedirect('/')

    else:
        form = RegistrationForm()

    token = {}
    token.update(csrf(request))
    token['form'] = form

    return render_to_response('registration/registration_form.html', token)


def registration_complete(request):
    return render_to_response('registration/registration_complete.html')



# Create your views here.
