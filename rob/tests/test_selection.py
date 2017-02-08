from django.test import TestCase
from rob.modeldir.game import *
from rob.modeldir.selection import *
from rob.modeldir.player import *
from rob.modeldir.user import *
from django.contrib.auth.models import User
import mock

class SelectionTest(TestCase):

    def setUp(self):
        game = mock.Mock(spec=Game)
        Selection.objects.create(game_id=5, player_id=2)
        Selection.objects.create(game_id=6, player_id=2, colour="red")

    def test_make_loser_set_status_to_false(self):
        selection = Selection.objects.get(game_id=5)
        selection.set_loser(4)
        self.assertEqual(selection.active, False)

    def test_make_loser_set_round_lost(self):
        selection = Selection.objects.get(game_id=5)
        selection.set_loser(4)
        self.assertEqual(selection.lost_round, 4)

    def test_reset_winners(self):
        cheese = Selection.objects.get(game_id=6)
        cheese.reset_winners()
        self.assertEqual(cheese.colour, "")
        self.assertEqual(cheese.active, True)
