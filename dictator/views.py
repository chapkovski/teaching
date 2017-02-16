from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import random
from otree.common import safe_json

class Introduction(Page):
    pass


class Offer(Page):
    form_model = models.Player
    form_fields = ['kept']
    def vars_for_template(self):
        numLow = 0
        numHigh = 10
        n = 10
        listOfNumbers = []
        for p in self.player.in_all_rounds():
            if p.kept is not None:
                listOfNumbers.append(int(p.kept))
        toadd = ['']*(Constants.num_rounds-len(listOfNumbers))
        listOfNumbers += toadd
        round_numbers = safe_json(list(range(1, Constants.num_rounds+1)))
        # print("LIST OF rounds: {}".format(round_numbers))
        myseries = []
        myseries.append({
        'name': 'decisions',
        'data': listOfNumbers})
        series_to_pass = safe_json(myseries)
        # print("jsonied series: {} =============".format(series_to_pass))
        return {
            'series_to_pass':series_to_pass,
            'round_numbers':round_numbers,
        }
    # def is_displayed(self):
    #     return self.player.id_in_group == 1


# class ResultsWaitPage(WaitPage):
#     def after_all_players_arrive(self):
#         self.group.set_payoffs()
#
#     def vars_for_template(self):
#         if self.player.id_in_group == 2:
#             body_text = "You are participant 2. Waiting for participant 1 to decide."
#         else:
#             body_text = 'Please wait'
#         return {'body_text': body_text}


class Results(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds
    def offer(self):
        return Constants.endowment - self.player.kept

    def vars_for_template(self):
        self.player.set_payoffs()
        return {
            'offer': self.player.payoff
        }


page_sequence = [
    # Introduction,
    Offer,
    # ResultsWaitPage,
    Results
]
