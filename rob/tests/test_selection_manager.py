from django.test import TestCase
from rob.modeldir.game import *
from rob.modeldir.selection import *
from rob.modeldir.player import *
from rob.modeldir.user import *
from django.contrib.auth.models import User
import mock

class SelectionTest(TestCase):

    # def setUp(self):
    #     game = mock.Mock(spec=Game)
    #     Selection.objects.create(game_id=5, player_id=2)
    #     Selection.objects.create(game_id=6, player_id=2, colour="red")

    def test_get_winners_returns_all_winners(self):
        now = datetime.now()
        hour_from_now = now + timedelta(hours=1)
        game = Game.objects.create(colour="black", started_at=now, ends_at=hour_from_now)
        winning_selection = Selection.objects.create(game_id=game.pk, player_id=5,colour='black')
        losing_selection = Selection.objects.create(game_id=game.pk, player_id=6,colour='red')
        winners = Selection.objects.get_winners(game.id, game.colour)
        self.assertIn(winning_selection, winners)
        self.assertNotIn(losing_selection, winners)

    def test_get_losers_returns_all_winners(self):
        now = datetime.now()
        hour_from_now = now + timedelta(hours=1)
        game = Game.objects.create(colour="black", started_at=now, ends_at=hour_from_now)
        winning_selection = Selection.objects.create(game_id=game.pk, player_id=5,colour='black')
        losing_selection = Selection.objects.create(game_id=game.pk, player_id=6,colour='red')
        losers = Selection.objects.get_losers(game.id, game.colour)
        self.assertNotIn(winning_selection, losers)
        self.assertIn(losing_selection, losers)

    def test_get_reds_returns_all_red_selections(self):
        red_selection = Selection.objects.create(game_id=5, player_id=5,colour='red')
        black_selection = Selection.objects.create(game_id=5, player_id=6,colour='black')
        reds = Selection.objects.get_reds(5)
        self.assertNotIn(black_selection, reds)
        self.assertIn(red_selection,reds)

    def test_get_reds_returns_all_red_selections(self):
        red_selection = Selection.objects.create(game_id=5, player_id=5,colour='red')
        black_selection = Selection.objects.create(game_id=5, player_id=6,colour='black')
        blacks = Selection.objects.get_blacks(5)
        self.assertIn(black_selection, blacks)
        self.assertNotIn(red_selection,blacks)


    # def test_make_loser_set_round_lost(self):
    #     selection = Selection.objects.get(game_id=5)
    #     selection.set_loser(4)
    #     self.assertEqual(selection.lost_round, 4)
    #
    # def test_reset_winners(self):
    #     cheese = Selection.objects.get(game_id=6)
    #     cheese.reset_winner()
    #     self.assertEqual(cheese.colour, "")
    #     self.assertEqual(cheese.active, True)
