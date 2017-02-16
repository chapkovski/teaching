from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
from settings import SESSION_CONFIGS

doc = """
This is a one-period public goods game with 4 players.
Plus treatments:
-  for detection of the smallest contributor(s) in a group
-  for collective sanctins of non-detectors
"""


class Constants(BaseConstants):
    name_in_url = 'colsan'
    players_per_group = 4#SESSION_CONFIGS[0]['num_demo_participants']
    num_rounds = 1

    instructions_template = 'colsan/Instructions.html'

    # """Amount allocated to each player"""
    endowment = c(100)
    efficiency_factor = 2
    mydict = {1: 0.25, 2: 0.5, 3: 0.75, 4: 1, 5:1.1, 6:1.2, }
    # mydict =   [0.25,0.5,0.76,1, 1.1, 2] #[1,2,3]#

class Subsession(BaseSubsession):
    def vars_for_admin_report(self):
        contributions = [p.contribution for p in self.get_players() if p.contribution is not None]
        return {
            'avg_contribution': sum(contributions)/len(contributions),
            'min_contribution': min(contributions),
            'max_contribution': max(contributions),
        }


class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    numTLCs = models.PositiveIntegerField()
    individual_share = models.CurrencyField()
    def detect_TLC(self):
        self.numTLCs = 0
        # all_players_ids = [p.id for p in self.get_players()]
        # minconrib = min([p.contribution for p in self.get_players()])
        # m = min(all_contribs)
        # tlcs =[i for i, j in enumerate(a) if j == m]
        # c = [all_players_ids[index] for index in tlcs]
        mincontrib = min([p.contribution for p in self.get_players()])
        for p in self.get_players():
            if p.contribution==mincontrib and mincontrib!=Constants.endowment:
                p.isTLC = True
                self.numTLCs+=1
            else:
                p.isTLC = False
#
# def set_payoffs(self):
#         self.total_contribution = sum([p.contribution for p in self.get_players()])
#         self.individual_share = self.total_contribution * Constants.efficiency_factor / Constants.players_per_group
#         for p in self.get_players():
#             p.payoff = (Constants.endowment - p.contribution) + self.individual_share




class Player(BasePlayer):

    isTLC = models.BooleanField(
        doc = """is a participant the smallest contributor (TLS) in this round """
    )
    detect = models.BooleanField(
        doc = """Binary decision about detecting the TLS in this group in this round"""
    # if there are more than one TLS one is randomly chosen as TLS.
    )
    contribution = models.PositiveIntegerField(
        min=0, max=Constants.endowment,
        doc="""The amount contributed by the player""",
    )
for i in range(Constants.players_per_group):
    Player.add_to_class("detectP{}".format(i+1),
        models.BooleanField(
            verbose_name="Participant {}".format(i+1)
        ))

# for key in Constants.mydict:
#
#         verbose_name="Player {}".format(i+1))
