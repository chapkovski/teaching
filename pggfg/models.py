from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
# from settings import SESSION_CONFIGS
from django.contrib.postgres.fields import ArrayField
from django import forms
# for the future implementation of matrix - jsonfield (now just postgres
# ArrayField)
# from otree.db.serializedfields import JSONField

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
    punishment_factor = 3
    punishment_limit = int(endowment/punishment_factor)


class Subsession(BaseSubsession):
    punishment = models.BooleanField()

    def before_session_starts(self):
        if 'punishment' in self.session.config:
            self.punishment = self.session.config['punishment']
        else:
            self.punishment = False
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
    # myjson = JSONField(null=True, doc="""json for saving punishment matrix.
    # for the future implementations. now i am using postgres arrayfield which
    # makes it impossible to use it with sqlite """)
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
        # doc="""not the best solution to store the punishment matrix.
        # in the future it is better to switch to database-independentJSONField
        # provided by otree."""
    )

    def set_payoffs(self):
        self.total_contribution = sum([p.contribution for p in self.get_players()])
        self.average_contribution = self.total_contribution/ Constants.players_per_group
        self.individual_share = self.total_contribution * Constants.efficiency_factor / Constants.players_per_group
        for p in self.get_players():
            # if punishment_sent or _received is not defined then use 0 -
            # for treatment without punishment
            p.payoff = sum([+ Constants.endowment,
                           - p.contribution,
                           + self.individual_share,
                           - (p.punishment_sent or 0),
                           - (p.punishment_received or 0), ])


class Player(BasePlayer):
    punishment_sent = models.IntegerField()
    punishment_received = models.IntegerField()
    contribution = models.PositiveIntegerField(
        min=0, max=Constants.endowment,
        doc="""The amount contributed by the player""",
        widget=forms.NumberInput(attrs={'class': 'form-control ',
                                        'required': 'required',
                                        'min': 0, 'max': Constants.endowment,
                                        'autofocus': 'autofocus', })
    )


for i in range(Constants.players_per_group):
    Player.add_to_class("punishP{}".format(i+1),
                        models.IntegerField(
            verbose_name="Participant {}".format(i+1),
            min=0,
            max=Constants.endowment,
            widget=forms.NumberInput(attrs={'class': 'form-control ',
                                            'required': 'required',
                                            'min': 0,
                                            'max': Constants.punishment_limit,
                                            'autofocus': 'autofocus', })
        ))
