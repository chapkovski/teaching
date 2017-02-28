from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
# from otree.api import models as m
from .models import Constants
from otree.common import safe_json

from otree.api import widgets
from django.forms import modelform_factory
from django import forms


class PunishmentForm(forms.Form):

    def __init__(self, fields_to_add, *args, **kwargs):
        super(PunishmentForm, self).__init__(*args, **kwargs)

        # CHOICES = (("True", True), ("False", False))
        for f in fields_to_add:
            self.fields[f] = forms.IntegerField()


class Introduction(Page):
    """Description of the game: How to play and returns expected"""
    def before_next_page(self):
        self.group.testmatrix = [[1,2,3],[1,2,3],[1,2,3]]


class Contribute(Page):
    """Player: Choose how much to contribute"""

    form_model = models.Player
    form_fields = ['contribution']

    timeout_submission = {'contribution': c(Constants.endowment / 2)}




class ContributionWaitPage(WaitPage):
    """Waiting till all players make their decisions about the contribution"""
    # def after_all_players_arrive(self):
        # self.group.detect_TLC()
        # self.group.set_payoffs()

    body_text = "Waiting for other participants to contribute."


class Punishment(Page):
    """here the decision to punish the peers is taken"""
    form_model = models.Player

    def vars_for_template(self):

        others = self.player.get_others_in_group()
        contribs_to_show = [p.contribution for p in others]
        verbose_names = ['Participant {}'.format(p.id_in_group)
                         for p in others]
        fields_to_show = self.get_form_fields()
        punishmentform = PunishmentForm(fields_to_show)
        return {'abclist': zip(punishmentform,
                               contribs_to_show,
                               verbose_names)}

    def get_form_fields(self):
        others = self.player.get_others_in_group()
        fields_to_show = ['punishP{}'.format(p.id_in_group) for p in others]
        return fields_to_show

    """Participants take decision whether to detect the smallest contributor"""
    def before_next_page(self):
        punishmentvector = []
        for i in range(Constants.players_per_group):
            f = self.player._meta.get_field("punishP{}".format(i+1))
            punishmentvector.append(getattr(self.player, f.name) or 0)

        curpunishmentmatrix = list(self.group.punishmentmatrix)
        curpunishmentmatrix[self.player.id_in_group-1] = punishmentvector
        self.group.punishmentmatrix = curpunishmentmatrix


class PunishmentWaitPage(WaitPage):
    """Waiting for the group to finish the punishment stage before
    showing them results"""
    def after_all_players_arrive(self):
        for p in self.group.get_players():
            p.punishment_sent = sum(self.group.punishmentmatrix[p.id_in_group-1])
            p.punishment_received = sum(row[p.id_in_group-1]
                                        for row in self.group.punishmentmatrix)


class Results(Page):
    """Players payoff: How much each has earned in this round"""

    def vars_for_template(self):
        pass


class FinalWaitPage(WaitPage):
    wait_for_all_groups = True

    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds


class FinalResults(Page):
    """Final earnings are shown"""
    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

    def vars_for_template(self):
        s = self.subsession
        mygroupcontribs = [[g.round_number, g.average_contribution, ]
                           for g in self.group.in_all_rounds()]
        personcontribs = [[p.round_number, p.contribution, ]
                          for p in self.player.in_all_rounds()]

        contribs = []
        contribscatter = []
        group_ids = []
        round_nums = []

        for g in s.get_groups():
            for ags in g.in_all_rounds():
                for p in ags.get_players():
                    contribs.append(p.contribution)
                    group_ids.append(g.id)
                    round_nums.append(p.subsession.round_number)
                    contribscatter.append([p.subsession.round_number,
                                           p.contribution])
        allcontribstable = zip(group_ids, round_nums, contribs)
        round_numbers = safe_json(list(range(1, Constants.num_rounds + 1)))
        series = []

        series.append({
            'name': 'Your contributions',
            'type': 'line',
            'data': personcontribs})

        series.append({
            'name': 'Your group contributions',
            'type': 'line',
            'data': mygroupcontribs})

        series.append({
            'name': 'all players',
            'type': 'scatter',
            'data': [list(a) for a in zip(round_nums, contribs)]})

        highcharts_series = safe_json(series)

        return {'allcontribstable': llcontribstable,
                'groupcontribs': mygroupcontribs,
                'personcontribs': personcontribs,
                'round_numbers': round_numbers,
                'highcharts_series': highcharts_series,
                }


page_sequence = [
    Introduction,
    Contribute,
    ContributionWaitPage,
    Punishment,
    PunishmentWaitPage,
    Results,
    FinalWaitPage,
    FinalResults,
]