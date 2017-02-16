from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random


doc = """
One player decides how to divide a certain amount between himself and the other
player.

See: Kahneman, Daniel, Jack L. Knetsch, and Richard H. Thaler. "Fairness
and the assumptions of economics." Journal of business (1986):
S285-S300.

"""


class Constants(BaseConstants):
    name_in_url = 'dictator'
    players_per_group = None
    num_rounds = 10

    instructions_template = 'dictator/Instructions.html'

    # Initial amount allocated to the dictator
    endowment = (100)


class Subsession(BaseSubsession):
    def vars_for_admin_report(self):
        payoffs = sorted([p.payoff for p in self.get_players()])
        return {'payoffs': payoffs}


class Group(BaseGroup):
    pass

class Player(BasePlayer):
    kept = models.CharField(
        doc="""Amount dictator decided to keep for himself""",
        min=0, max=Constants.endowment,
        choices=['Football', 'Opera'],
        widget=widgets.RadioSelect(),
        verbose_name='I will keep (from 0 to %i)' % Constants.endowment
    )

    #     decision = models.CharField(
    #     choices=['Football', 'Opera'],
    #     doc="""Either football or the opera""",
    #     widget=widgets.RadioSelect()
    # )

    def set_payoffs(self):
        print('setting payoffs...')
        # p1 = self.get_player_by_id(1)
        # p2 = self.get_player_by_id(2)
        self.payoff = (self.kept)
        # self.payoff=str(self.payoff)
        # p2.payoff = Constants.endowment - self.kept
