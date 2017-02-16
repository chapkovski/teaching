from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
from settings import SESSION_CONFIGS
import json

doc = """
    demo PGG for one player only with randomly generated contributions of others.
    Just for checking how HighCharts work.
"""


class Constants(BaseConstants):
    name_in_url = 'pggfg_demo'
    players_per_group =  None
    group_size = 4
    session_size =20
    num_rounds = 10

    instructions_template = 'pggfg_demo/Instructions.html'

    # """Amount allocated to each player"""
    endowment = 100
    efficiency_factor = 2

class Subsession(BaseSubsession):
    def before_session_starts(self):
        print("ROUND: {}".format(self.round_number))
        session_contribs=[random.randrange(1,Constants.endowment*(1-4*self.round_number/100),1) for _ in range (Constants.session_size-1)]
        group_contribs=random.sample(session_contribs,Constants.group_size-1)
        for p in self.get_players():
            p.all_others_contrib=  (session_contribs)
            p.your_group_contrib= (group_contribs)



class Group(BaseGroup):
    pass


class Player(BasePlayer):
    contribution = models.PositiveIntegerField(
        min=0, max=Constants.endowment,
        doc="""The amount contributed by the player""",
    )
    all_others_contrib = models.CharField(
            doc="""JSON set of random numbers generated to imitate the multi-user behaviour - DEMO ONLY""",
    )
    your_group_contrib= models.CharField(
            doc="""JSON set of random numbers around the user's choice - DEMO ONLY""",
    )

    average_group_contrib = models.PositiveIntegerField(
            doc="""An 'average' number of contributions in a 'group' - DEMO ONLY""",
    )
    total_contribution = models.PositiveIntegerField(
                doc="""An 'sum' number of contributions in a group - DEMO ONLY""",
        )

    individual_share = models.PositiveIntegerField(
                doc="""your earnings from the group project""",
        )

    def set_payoffs(self):
        self.total_contribution = sum(json.loads(self.your_group_contrib))+self.contribution
        self.average_group_contrib = self.total_contribution/ Constants.group_size
        self.individual_share = self.total_contribution * Constants.efficiency_factor / Constants.group_size
        self.payoff = (Constants.endowment - self.contribution) + self.individual_share
