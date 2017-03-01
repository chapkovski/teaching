from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
# from otree.api import models as m
from .models import Constants
from otree.common import safe_json

from otree.api import widgets
from django.forms import modelform_factory
from django import forms
import json


class PunishmentForm(forms.Form):

    def __init__(self, fields_to_add, *args, **kwargs):
        super(PunishmentForm, self).__init__(*args, **kwargs)

        # CHOICES = (("True", True), ("False", False))
        for f in fields_to_add:
            self.fields[f] = forms.IntegerField()


class Introduction(Page):
    """Description of the game: How to play and returns expected"""
    def is_displayed(self):
        return self.subsession.round_number == 1


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

    def is_displayed(self):
        return self.subsession.punishment

    def vars_for_template(self):

        others = self.player.get_others_in_group()
        contribs_to_show = [p.contribution for p in others]
        verbose_names = ['Participant {}'.format(p.id_in_group)
                         for p in others]
        fields_to_show = self.get_form_fields()
        punishmentform = PunishmentForm(fields_to_show)
        return {'abclist': zip(punishmentform,
                               contribs_to_show,
                               verbose_names),
                'form': punishmentform, }

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
    def is_displayed(self):
        return self.subsession.punishment

    def after_all_players_arrive(self):
        for p in self.group.get_players():
            p.punishment_sent = sum(
                                    self.group.punishmentmatrix
                                    [p.id_in_group-1])
            p.punishment_received = Constants.punishment_factor*sum(row[p.id_in_group-1]
                                        for row in self.group.punishmentmatrix)


class ResultsWaitPage(WaitPage):
    # not the best solution, but suitable for didactical reasons:
    # so all the players can see all others in entire population
    # wait_for_all_groups = True
    def after_all_players_arrive(self):
        self.group.set_payoffs()


def preparing_charts(me=None, final=False):
    series = []
    if me:
        mygroupaverage = [[p.round_number,round(p.group.average_contribution),] for p in me.in_all_rounds()]
        mygroupcontribs = [[r.round_number,(a.contribution or 0)] for r in me.group.in_all_rounds() for a in r.get_players()]
        personcontribs = [[p.round_number,p.contribution,] for p in me.in_all_rounds()]
        empty_rounds = range(me.subsession.round_number +1, Constants.num_rounds + 1)
        making_add = list(zip(list(empty_rounds),['']*len(empty_rounds)))
        mygroupcontribs += making_add
        personcontribs += making_add
        series.append({
            'name': 'Your group average',
            'type': 'line',
            'data': mygroupaverage})

        series.append({
            'name': 'Your group members',
            'type': 'scatter',
            'data': mygroupcontribs,
            'marker': {
                    'fillColor': '#FFFFFF',
                    'lineWidth': 1,
                    'lineColor': 'red',
                    'radius': 7,
                    'symbol': 'circle'},
                    })

        series.append({
            'name': 'Your contributions',
            'type': 'line',
            'data': personcontribs,
            'marker': {
                        'radius': 5,
                        }})

    if final:
        all_contribs = [[r.round_number,(a.contribution or 0)] for r in me.subsession.in_all_rounds() for a in r.get_players()]
        popsize =len(me.subsession.get_players())
        all_contribs_average = [[r.round_number, round(sum([p.contribution for p in r.get_players()])/popsize)] for r in me.subsession.in_all_rounds()]
        series.append({
            'name': 'All participants',
            'type': 'scatter',
            'data': all_contribs,
                        'marker': {
                'fillColor': '#FFFFFF',
                'lineWidth': 1,
                'lineColor':'blue',
                'radius':7,
            } })
        series.append({
            'name': 'Overall average',
            'type': 'line',
            'color': 'rgba(0, 0, 0, 0.2)',
            'lineWidth': 15,
            'data': all_contribs_average,
                        'marker': {
                'enabled':False,
                'fillColor': '#FFFFFF',
                'lineWidth': 1,
                'lineColor':'blue',
                'radius':1,
                'symbol': 'circle',
            } })



    highcharts_series = safe_json(series)
    return highcharts_series

class Results(Page):
    """Players payoff: How much each has earned in this round"""
    def is_displayed(self):
        return self.subsession.round_number < Constants.num_rounds

    def vars_for_template(self):
        return {'highcharts_series': preparing_charts(me=self.player),
                'total_earnings': Constants.efficiency_factor*self.group.total_contribution,
                }


class FinalWaitPage(WaitPage):
    wait_for_all_groups = True

    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds


class FinalResults(Page):
    """Final earnings are shown"""
    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

    def vars_for_template(self):
        return {'highcharts_series': preparing_charts(final=True,me=self.player),
        'total_earnings': self.group.total_contribution*Constants.efficiency_factor, }


page_sequence = [
    Introduction,
    Contribute,
    ContributionWaitPage,
    Punishment,
    PunishmentWaitPage,
    ResultsWaitPage,
    Results,
    FinalWaitPage,
    FinalResults,
]
