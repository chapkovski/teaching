from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

from django.db import models as djmodels
from django.db.models import Sum, Avg

author = "Philip Chapkovski, HSE-Moscow, chapkovski@gmail.com"

doc = """
Public Good Game with Punishment (Fehr and Gaechter).
Fehr, E. and Gachter, S., 2000.
 Cooperation and punishment in public goods experiments. American Economic Review, 90(4), pp.980-994.
"""


class Constants(BaseConstants):
    name_in_url = 'pggfg'
    players_per_group = 3
    num_others_per_group = players_per_group - 1
    num_rounds = 2
    instructions_template = 'pggfg/Instructions.html'
    endowment = 20
    efficiency_factor = 2
    punishment_endowment = 10
    punishment_factor = 3
    punishment_rounds = [2]


class Subsession(BaseSubsession):
    punishment = models.BooleanField()

    def vars_for_admin_report(self):
        subsession_data = list(
            self.session.pggfg_group.all().values(
                'round_number').annotate(s=Avg('average_contribution')).values_list('s', flat=True))
        subsession_data = [round(i, 2) if i else None for i in subsession_data]

        return dict(
            highcharts_series=[
                {'name': 'Average contribution', 'data': subsession_data},

            ]
        )

    def round_numbers(self):
        return list(self.session.pggfg_subsession.all().values_list('round_number', flat=True))

    def creating_session(self):
        self.punishment = self.round_number in Constants.punishment_rounds


class Group(BaseGroup):
    total_contribution = models.IntegerField()
    average_contribution = models.FloatField()
    individual_share = models.CurrencyField()

    def create_punishment_records(self):
        ps = []
        for p in self.get_players():
            for o in p.get_others_in_group():
                ps.append(Punishment(sender=p, receiver=o, ))
        Punishment.objects.bulk_create(ps)

    def set_pd_payoffs(self):
        self.total_contribution = sum([p.contribution for p in self.get_players()])
        self.average_contribution = self.total_contribution / Constants.players_per_group
        self.individual_share = self.total_contribution * Constants.efficiency_factor / Constants.players_per_group
        for p in self.get_players():
            p.pd_payoff = sum([+ Constants.endowment,
                               - p.contribution,
                               + self.individual_share,
                               ])
            p.set_punishment_endowment()

    def set_punishments(self):
        for p in self.get_players():
            p.set_punishment()
        for p in self.get_players():
            p.set_payoff()


class Player(BasePlayer):
    contribution = models.PositiveIntegerField(
        min=0, max=Constants.endowment,
        doc="""The amount contributed by the player""",
        label="Сколько вы хотите вложить в общий проект (от 0 до {})?".format(Constants.endowment)
    )
    punishment_sent = models.IntegerField()
    punishment_received = models.IntegerField()
    pd_payoff = models.CurrencyField(doc='to store payoff from contribution stage')
    punishment_endowment = models.IntegerField(initial=0, doc='punishment endowment')

    def set_payoff(self):
        self.payoff = self.pd_payoff - self.punishment_sent - self.punishment_received

    def set_punishment_endowment(self):
        assert self.pd_payoff is not None, 'You have to set pd_payoff before setting punishment endowment'
        self.punishment_endowment = min(self.pd_payoff, Constants.punishment_endowment)

    def set_punishment(self):
        self.punishment_sent = self.punishments_sent.all().aggregate(s=Sum('amount')).get('s') or 0
        self.punishment_received = (self.punishments_received.all().aggregate(s=Sum('amount')).get(
            's') or 0) * Constants.punishment_factor


class Punishment(djmodels.Model):
    sender = djmodels.ForeignKey(to=Player, related_name='punishments_sent', on_delete=djmodels.CASCADE)
    receiver = djmodels.ForeignKey(to=Player, related_name='punishments_received', on_delete=djmodels.CASCADE)
    amount = models.IntegerField(min=0)
