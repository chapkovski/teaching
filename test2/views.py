from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants
from otree.common import safe_json

from otree.api import widgets
from django.forms import modelform_factory
from django import forms


class WP(WaitPage):
    def  after_all_players_arrive(self):
        if self.round_number==1:
            matrix = self.subsession.get_group_matrix()
            newmatrix = []
            for g in matrix:
                activeplayers = []
                passiveplayers = []
                for i in g:
                    if i.participant.vars['loser'] == False :
                        activeplayers.append(i.id_in_subsession)
                    else:
                        passiveplayers.append([i.id_in_subsession])
                newmatrix.append(activeplayers)
                newmatrix.extend(passiveplayers)
                newmatrix=[i for i in newmatrix if i]
            if newmatrix and len(self.group.get_players())>1:
                self.subsession.set_group_matrix(newmatrix)
        else:
            self.subsession.set_group_matrix(self.subsession.in_round(1).get_group_matrix())




class Contribute(Page):



    """Player: Choose how much to contribute"""

    form_model = models.Player
    form_fields = ['contribution']

    timeout_submission = {'contribution': c(Constants.endowment / 2)}



class Results(Page):
    """Players payoff: How much each has earned in this round"""

    def vars_for_template(self):
        pass

page_sequence = [
    WP,
    Contribute,

    WaitPage,
    Results,
]
