from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants
from otree.common import safe_json

from otree.api import widgets
from django.forms import modelform_factory
from django import forms


class WP(WaitPage):
    def is_displayed(self):
        return not self.player.participant.vars['loser']
    # def  after_all_players_arrive(self):
    #     if self.round_number==1:
    #         for i in range(1,Constants.num_rounds+1):
    #             matrix = self.subsession.in_round(i).get_group_matrix()
    #             newmatrix = []
    #             for g in matrix:
    #                 activeplayers = []
    #                 passiveplayers = []
    #                 for p in g:
    #                     if p.participant.vars['loser'] == False :
    #                         activeplayers.append(p.id_in_subsession)
    #                     else:
    #                         passiveplayers.append([p.id_in_subsession])
    #                 newmatrix.append(activeplayers)
    #                 newmatrix.extend(passiveplayers)
    #                 newmatrix=[j for j in newmatrix if j]
    #             if newmatrix:
    #                 self.subsession.set_group_matrix(newmatrix)




class Contribute(Page):
    def is_displayed(self):
        return not self.player.participant.vars['loser']


    """Player: Choose how much to contribute"""

    form_model = models.Player
    form_fields = ['contribution']

    timeout_submission = {'contribution': c(Constants.endowment / 2)}

class WP2(WaitPage):
    def is_displayed(self):
        return not self.player.participant.vars['loser']
    def  after_all_players_arrive(self):
        matrix = self.subsession.get_group_matrix()
        print('MATRIX:',matrix)

class Results(Page):
    """Players payoff: How much each has earned in this round"""
    def is_displayed(self):
        return not self.player.participant.vars['loser']

    def vars_for_template(self):
        pass

page_sequence = [
    WP,
    Contribute,
    WP2,

    Results,
]
