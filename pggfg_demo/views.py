from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
# from otree.api import models as m
from .models import Constants
from otree.common import safe_json

from otree.api import widgets
from django.forms import modelform_factory
from django import forms
import json



class Introduction(Page):


    """Description of the game: How to play and returns expected"""
    pass


class Contribute(Page):
    """Player: Choose how much to contribute"""
    form_model = models.Player
    form_fields = ['contribution']
    def vars_for_template(self):
        return{'n_other_players':Constants.group_size-1}


class Results(Page):
    """Players payoff: How much each has earned in this round"""
    def vars_for_template(self):
        self.player.set_payoffs()


        mygroupcontribs=[[p.round_number,p.average_group_contrib,] for p in self.player.in_all_rounds()]
        personcontribs = [[p.round_number,p.contribution,] for p in self.player.in_all_rounds()]
        empty_rounds=range(self.subsession.round_number +1, Constants.num_rounds + 1)
        making_add=list(zip(list(empty_rounds),['']*len(empty_rounds)))
        mygroupcontribs+=making_add
        personcontribs+=making_add
        #
        aoc_list = []
        for p in self.player.in_all_rounds():
            all_others_contrib = list(json.loads(p.all_others_contrib))
            aoc_list+=list(zip([p.round_number]*len(all_others_contrib),all_others_contrib))
        print(aoc_list)
        series = []

        series.append({
            'name': 'all players',
            'type': 'scatter',
            'data': aoc_list})
        series.append({
            'name': 'Your contributions',
            'type': 'line',
            'data': personcontribs})

        series.append({
            'name': 'Your group contributions',
            'type': 'line',
            'data': mygroupcontribs})


        highcharts_series = safe_json(series)

# *******

        return {#'round_numbers': round_numbers,
                'highcharts_series': highcharts_series,
                'your_group_contrib':list(json.loads(self.player.your_group_contrib)),
        }



        return{}




page_sequence = [
    # Introduction,
    Contribute,
    Results,

]
