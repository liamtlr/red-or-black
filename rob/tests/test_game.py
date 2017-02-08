from django.test import TestCase, RequestFactory
from rob.modeldir.game import *
from rob.modeldir.selection import *
from rob.modeldir.player import *
from rob.modeldir.user import *
from django.contrib.auth.models import User
import mock

class GameTest(TestCase):

    def test_first_round_games_returns_only_games_in_round_one(self):
        now = datetime.now()
        hour_from_now = now + timedelta(hours=1)
        game_first_round_open_to_join = Game.objects.create(pk=1, round_no=1, started_at = now, ends_at=hour_from_now)
        game_second_round = Game.objects.create(pk=2,round_no=2, started_at = now, ends_at=hour_from_now)
        games = Game.objects.first_round_games(7)
        self.assertNotIn(game_second_round, games)

    def test_first_round_games_returns_only_which_do_not_have_selections_from_current_user(self):
        now = datetime.now()
        hour_from_now = now + timedelta(hours=1)
        game_first_round_with_user_selection = Game.objects.create(pk=3, round_no=1, started_at = now, ends_at=hour_from_now)
        Selection.objects.create(game_id=3, player_id=4)
        games = Game.objects.first_round_games(4)
        self.assertNotIn(game_first_round_with_user_selection, games)

    def test_first_round_games_returns_only_live_games(self):
        now = datetime.now()
        hour_ago = now - timedelta(hours=1)
        game_first_round_in_past = Game.objects.create(pk=4, round_no=1, started_at = now, ends_at=hour_ago)
        Selection.objects.create(game_id=3, player_id=4)
        games = Game.objects.first_round_games(4)
        self.assertNotIn(game_first_round_in_past, games)

    def test_pending_games_returns_games_where_user_has_live_selections(self):
        now = datetime.now()
        hour_from_now = now + timedelta(hours=1)
        live_game_second_round = Game.objects.create(pk=5, round_no=2, started_at = now, ends_at=hour_from_now)
        selection = Selection.objects.create(game_id=5, player_id=4, colour="red")
        games = Game.objects.pending_games(4)
        self.assertIn(live_game_second_round, games)

    def test_pending_games_returns_does_not_return_games_with_blank_colour(self):
        now = datetime.now()
        hour_from_now = now + timedelta(hours=1)
        live_game_not_chosen = Game.objects.create(pk=6, round_no=2, started_at = now, ends_at=hour_from_now)
        Selection.objects.create(game_id=6, player_id=4, colour="")
        games = Game.objects.pending_games(4)
        self.assertNotIn(live_game_not_chosen, games)
