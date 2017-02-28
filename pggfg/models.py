from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
# from settings import SESSION_CONFIGS
from django.contrib.postgres.fields import ArrayField


doc = """
public good game with some variations depending on session configs:
- punishment stage (for session 4)
- collective sanctions (for session 7)
"""


class Constants(BaseConstants):
    name_in_url = 'pggfg'
    players_per_group = 3
    num_rounds = 10

    instructions_template = 'pggfg/Instructions.html'

    endowment = c(100)
    efficiency_factor = 2


class Subsession(BaseSubsession):
    def before_session_starts(self):
        for g in self.get_groups():
            g.punishmentmatrix = [[0 for i in self.get_players()]
                                  for i in self.get_players()]

    def vars_for_admin_report(self):
        contributions = [p.contribution for p in self.get_players()
                         if p.contribution is not None]
        return {
            'avg_contribution': sum(contributions)/len(contributions),
            'min_contribution': min(contributions),
            'max_contribution': max(contributions),
        }


class Group(BaseGroup):
    total_contribution = models.IntegerField()
    average_contribution = models.FloatField()
    individual_share = models.CurrencyField()
    punishmentmatrix = ArrayField(
        ArrayField(
            models.IntegerField(),
            size=Constants.players_per_group,
            null=True,
        ),
        size=Constants.players_per_group,
        null=True,
    )

    def set_payoffs(self):
        self.total_contribution = sum([p.contribution for p in self.get_players()])
        self.average_contribution = self.total_contribution/ Constants.players_per_group
        self.individual_share = self.total_contribution * Constants.efficiency_factor / Constants.players_per_group
        for p in self.get_players():
            p.payoff = (Constants.endowment - p.contribution) + self.individual_share




class Player(BasePlayer):
    punishment_sent = models.IntegerField()
    punishment_received = models.IntegerField()
    contribution = models.PositiveIntegerField(
        min=0, max=Constants.endowment,
        doc="""The amount contributed by the player""",
    )
for i in range(Constants.players_per_group):
    Player.add_to_class("punishP{}".format(i+1),
        models.IntegerField(
            verbose_name="Participant {}".format(i+1),
            min=0,
            max=Constants.endowment,
        ))
