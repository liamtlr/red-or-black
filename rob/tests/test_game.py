from django.test import TestCase, RequestFactory
from rob.modeldir.game import *
from rob.modeldir.selection import *
from rob.modeldir.player import *
from rob.modeldir.user import *
from django.contrib.auth.models import User
import mock
import random


class GameTest(TestCase):

    @mock.patch('random.choice')
    def test_select_colour_selects_a_colour(self, random_call):
        now = datetime.now()
        hour_ago = now - timedelta(hours=1)
        two_hours_ago = now - timedelta(hours=2)
        new_game = Game.objects.create(started_at = two_hours_ago, ends_at=hour_ago)
        random_call.return_value = 'black'
        new_game.select_colour()
        self.assertEqual(new_game.colour, 'black')
        self.assertEqual(new_game.previous_colours[-1], 'black')

    def test_increment_round_increments_round(self):
        now = datetime.now()
        hour_ago = now - timedelta(hours=1)
        two_hours_ago = now - timedelta(hours=2)
        game = Game.objects.create(started_at = two_hours_ago, ends_at=hour_ago, round_no = 3)
        game.increment_round()
        self.assertEqual(game.round_no, 4)

    def test_end_game_sets_In_progress_to_false(self):
        now = datetime.now()
        hour_ago = now - timedelta(hours=1)
        two_hours_ago = now - timedelta(hours=2)
        game = Game.objects.create(started_at = two_hours_ago, ends_at=hour_ago, round_no = 3)
        game.end_game()
        self.assertEqual(game.in_progress, False)
