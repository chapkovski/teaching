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
    name_in_url = 'dictatorMU'
    players_per_group = None
    num_rounds = 1

    instructions_template = 'dictatorMU/Instructions.html'

    # Initial amount allocated to the dictator
    endowment = 10


class Subsession(BaseSubsession):
    def vars_for_admin_report(self):
        payoffs = sorted([p.payoff for p in self.get_players()])
        return {'payoffs': payoffs}


class Group(BaseGroup):
    pass

class Player(BasePlayer):
    kept = models.PositiveIntegerField(
        doc="""Amount dictator decided to keep for himself""",
        min=0, max=Constants.endowment,
        verbose_name='I will keep (from 0 to %i)' % Constants.endowment
    )
    belief = models.PositiveIntegerField(
    doc="""Amount dictator beliefs others would keep for themselves""",
    min=0, max=Constants.endowment,
    verbose_name='How much  you believe all other participants will keep for themselves on average? (from 0 to %i)' % Constants.endowment
    )
    norm = models.PositiveIntegerField(
    doc="""Amount dictator thinks people should keep for themselves""",
    min=0, max=Constants.endowment,
    verbose_name='In your opinion what amount should a person keep for him/herself? (from 0 to %i)' % Constants.endowment
    )
    others_belief = models.PositiveIntegerField(
        doc="""Amount that dictator belives others expect from him to keep""",
        min=0, max=Constants.endowment,
        verbose_name='What amount you think other participants expect from you? (from 0 to %i)' % Constants.endowment
    )
    def set_payoffs(self):
        print('setting payoffs...')
        # p1 = self.get_player_by_id(1)
        # p2 = self.get_player_by_id(2)
        self.payoff = (self.kept)
        # self.payoff=str(self.payoff)
        # p2.payoff = Constants.endowment - self.kept
