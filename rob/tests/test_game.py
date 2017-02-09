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
        games = Game.objects.get_first_round_games(7)
        self.assertNotIn(game_second_round, games)

    def test_first_round_games_returns_only_which_do_not_have_selections_from_current_user(self):
        now = datetime.now()
        hour_from_now = now + timedelta(hours=1)
        game_first_round_with_user_selection = Game.objects.create(pk=3, round_no=1, started_at = now, ends_at=hour_from_now)
        Selection.objects.create(game_id=3, player_id=4)
        games = Game.objects.get_first_round_games(4)
        self.assertNotIn(game_first_round_with_user_selection, games)

    def test_first_round_games_returns_only_live_games(self):
        now = datetime.now()
        hour_ago = now - timedelta(hours=1)
        game_first_round_in_past = Game.objects.create(pk=4, round_no=1, started_at = now, ends_at=hour_ago)
        Selection.objects.create(game_id=3, player_id=4)
        games = Game.objects.get_first_round_games(4)
        self.assertNotIn(game_first_round_in_past, games)

    def test_pending_games_returns_games_where_user_has_live_selections(self):
        now = datetime.now()
        hour_from_now = now + timedelta(hours=1)
        live_game_second_round = Game.objects.create(pk=5, round_no=2, started_at = now, ends_at=hour_from_now)
        selection = Selection.objects.create(game_id=5, player_id=4, colour="red")
        games = Game.objects.get_pending_games(4)
        self.assertIn(live_game_second_round, games)

    def test_pending_games_does_not_return_games_with_blank_colour(self):
        now = datetime.now()
        hour_from_now = now + timedelta(hours=1)
        live_game_not_chosen = Game.objects.create(pk=6, round_no=2, started_at = now, ends_at=hour_from_now)
        Selection.objects.create(game_id=6, player_id=4, colour="")
        games = Game.objects.get_pending_games(4)
        self.assertNotIn(live_game_not_chosen, games)

    def test_lost_games_returns_users_lost_games(self):
        now = datetime.now()
        hour_ago = now - timedelta(hours=1)
        two_hours_ago = now - timedelta(hours=2)
        lost_game = Game.objects.create(pk=7, round_no=3, started_at = two_hours_ago, ends_at=hour_ago)
        selection = Selection.objects.create(game_id=7, player_id=4, colour="black", active=False)
        games = Game.objects.get_lost_games(4)
        self.assertIn(lost_game, games)

    def test_lost_games_does_not_return_active_games(self):
        now = datetime.now()
        hour_ago = now - timedelta(hours=1)
        two_hours_ago = now - timedelta(hours=2)
        active_game = Game.objects.create(pk=8, round_no=3, started_at = two_hours_ago, ends_at=hour_ago)
        selection = Selection.objects.create(game_id=8, player_id=4, colour="black", active=True)
        games = Game.objects.get_lost_games(4)
        self.assertNotIn(active_game, games)

    def test_lost_games_does_not_other_players_lost_games(self):
        now = datetime.now()
        hour_ago = now - timedelta(hours=1)
        two_hours_ago = now - timedelta(hours=2)
        other_users_lost_game = Game.objects.create(pk=9, round_no=3, started_at = two_hours_ago, ends_at=hour_ago)
        selection = Selection.objects.create(game_id=7, player_id=5, colour="black", active=False)
        games = Game.objects.get_lost_games(4)
        self.assertNotIn(other_users_lost_game, games)

    def test_won_games_returns_users_won_games(self):
        now = datetime.now()
        hour_ago = now - timedelta(hours=1)
        two_hours_ago = now - timedelta(hours=2)
        won_game = Game.objects.create(pk=10, round_no=3, started_at = two_hours_ago, ends_at=hour_ago, in_progress=False)
        selection = Selection.objects.create(game_id=10, player_id=4, colour="black", active=True)
        games = Game.objects.get_won_games(4)
        self.assertIn(won_game, games)

    def test_won_games_does_not_return_active_games(self):
        now = datetime.now()
        hour_ago = now - timedelta(hours=1)
        two_hours_ago = now - timedelta(hours=2)
        active_game = Game.objects.create(pk=11, round_no=3, started_at = two_hours_ago, ends_at=hour_ago, in_progress=True)
        selection = Selection.objects.create(game_id=11, player_id=4, colour="black", active=True)
        games = Game.objects.get_won_games(4)
        self.assertNotIn(active_game, games)

    def test_won_games_does_not_other_players_won_games(self):
        now = datetime.now()
        hour_ago = now - timedelta(hours=1)
        two_hours_ago = now - timedelta(hours=2)
        other_users_won_game = Game.objects.create(pk=12, round_no=3, started_at = two_hours_ago, ends_at=hour_ago, in_progress=False)
        selection = Selection.objects.create(game_id=12, player_id=5, colour="black", active=True)
        games = Game.objects.get_won_games(4)
        self.assertNotIn(other_users_won_game, games)

    def test_live_games_returns_users_live_games(self):
        now = datetime.now()
        hour_ago = now - timedelta(hours=1)
        hour_from_now = now + timedelta(hours=1)
        live_game = Game.objects.create(pk=13, round_no=3, started_at = hour_ago, ends_at=hour_from_now, in_progress=True)
        selection = Selection.objects.create(game_id=13, player_id=4, colour="", active=True)
        games = Game.objects.get_live_games(4)
        self.assertIn(live_game, games)

    def test_live_games_does_not_return_inactive_games(self):
        now = datetime.now()
        hour_ago = now - timedelta(hours=1)
        two_hours_ago = now - timedelta(hours=2)
        inactive_game = Game.objects.create(pk=14, round_no=3, started_at = two_hours_ago, ends_at=hour_ago, in_progress=False)
        selection = Selection.objects.create(game_id=14, player_id=4, colour="", active=True)
        games = Game.objects.get_live_games(4)
        self.assertNotIn(inactive_game, games)

    def test_live_games_does_not_other_players_live_games(self):
        now = datetime.now()
        hour_ago = now - timedelta(hours=1)
        two_hours_ago = now - timedelta(hours=2)
        other_users_live_game = Game.objects.create(pk=15, round_no=3, started_at = two_hours_ago, ends_at=hour_ago, in_progress=False)
        selection = Selection.objects.create(game_id=15, player_id=5, colour="", active=True)
        games = Game.objects.get_live_games(4)
        self.assertNotIn(other_users_live_game, games)

    def test_live_games_does_not_return_live_games_with_colour_chosen(self):
        now = datetime.now()
        hour_ago = now - timedelta(hours=1)
        hour_from_now = now + timedelta(hours=1)
        live_game = Game.objects.create(pk=13, round_no=3, started_at = hour_ago, ends_at=hour_from_now, in_progress=True)
        selection = Selection.objects.create(game_id=13, player_id=4, colour="black", active=True)
        games = Game.objects.get_live_games(4)
        self.assertNotIn(live_game, games)
