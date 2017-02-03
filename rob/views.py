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

from .models import Game



def home(request):
    games = Game.objects.all()
    print(games)
    for game in games:
        print(game.started_at)
    return render(request, 'home.html', {'games': games})

def view_game(request, pk):
    game = get_object_or_404(Game, pk=pk)
    return render(request, 'game/view.html', {'game': game})


def games(request):
    games = Game.objects.all()
    hawwo = "CUNTS"
    print(games)
    for game in games:
        print(game.started_at)
    return render(request, 'games.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)
            return HttpResponseRedirect('/')

    else:
        form = RegistrationForm()

    token = {}
    token.update(csrf(request))
    token['form'] = form

    return render_to_response('registration/registration_form.html', token)


def registration_complete(request):
    return render_to_response('registration/registration_complete.html')

def game_new(request):
    new_game = Game()
    new_game.create_game()
    print('HAWWOOOO')
    return HttpResponseRedirect('/')


# Create your views here.
