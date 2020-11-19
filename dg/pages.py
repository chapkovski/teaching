from ._builtin import Page, WaitPage
from .models import Constants

from otree.common import safe_json


class Introduction(Page):
    pass


class NormPage(Page):
    template_name = 'dg/Offer.html'
    form_model = 'player'


class NormBelief(NormPage):
    form_fields = ['norm_belief']


class NormExpectations(NormPage):
    form_fields = ['norm_expectation']


class EmpiricalExpectations(NormPage):
    form_fields = ['empirical_expectation']


class Decision(NormPage):
    form_fields = ['decision']






class ResultsWaitPage(WaitPage):
    wait_for_all_groups = True
    after_all_players_arrive = 'clearing_decisions'


class Results(Page):
   pass


page_sequence = [
    Introduction,
    NormBelief,
    NormExpectations,
    EmpiricalExpectations,
    Decision,
    ResultsWaitPage,
    Results,
]
