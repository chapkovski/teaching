from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .forms import PFormset
from .models import Constants, Player, Punishment as PunishmentModel
from otree.constants import timeout_happened


class FirstWP(WaitPage):

    def is_displayed(self):
        return self.subsession.round_number == 1

    group_by_arrival_time = True
class SecondWP(WaitPage):


    after_all_players_arrive = 'create_punishment_records'


class Introduction(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1


class PunishmentIntroduction(Page):
    def is_displayed(self):
        return self.subsession.round_number == Constants.punishment_rounds[0]


class Contribute(Page):
    form_model = 'player'
    form_fields = ['contribution']


class AfterContribWP(WaitPage):
    after_all_players_arrive = 'set_pd_payoffs'


class Punishment(Page):
    def is_displayed(self):
        return self.subsession.punishment

    def get_formset(self, data=None):
        return PFormset(instance=self.player,
                        data=data,
                        )

    def get_form(self, data=None, files=None, **kwargs):
        # here if this page was forced by admin to continue we just submit an empty form (with no formset data)
        # if we need this data later on that can create some problems. But that's the price we pay for autosubmission
        if data and data.get('timeout_happened'):
            return super().get_form(data, files, **kwargs)
        if not data:
            return self.get_formset()
        formset = self.get_formset(data=data)
        return formset

    def before_next_page(self):
        if self.timeout_happened:
            self.player.punishments_sent.all().update(amount=0)


class AfterPunishmentWP(WaitPage):
    after_all_players_arrive = 'set_punishments'


class Results(Page):
    def vars_for_template(self):
        myown_data = list(
            self.session.pggfg_player.filter(participant=self.participant).values_list('contribution', flat=True))
        group_data = list(self.session.pggfg_group.filter(id_in_subsession=self.group.id_in_subsession).values_list(
            'average_contribution', flat=True))
        return dict(
            highcharts_series=[
                {'name': 'Средний вклад', 'data': group_data},
                {'name': 'Мой вклад', 'data': myown_data},
            ]
        )


page_sequence = [
    FirstWP,
    SecondWP,
    Introduction,
    PunishmentIntroduction,
    Contribute,
    AfterContribWP,
    Punishment,
    AfterPunishmentWP,
    Results,
]
