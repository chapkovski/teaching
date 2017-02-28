from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import random
from otree.common import safe_json
# import copy
import pprint
# ======TO DELETE
from otree.api import widgets
# from django import forms
from otree.views.abstract import PlayerUpdateView
import otree.forms

import floppyforms as fforms

import floppyforms.__future__ as ffforms
from django.forms import modelform_factory

from django.forms import ModelForm as mmm

from django.template.defaulttags import register


def MyFormWrapper(model_to_pass, fields_to_pass, *args, **kwargs):
    class MyForm(mmm):
        class Meta:
            model = model_to_pass
            fields = fields_to_pass

        def __init__(self, *args, **kwargs):
            # kwargs.update({'label_suffix': ':'})
            print((kwargs))
            super(MyForm, self).__init__(*args, **kwargs)

    return MyForm()


class Introduction(Page):
    pass


class MyPage(Page):
    form_model = models.Player
    template_name = 'dictatorMU/Offer.html'
    title = ''
    form_fields = ['ns6_1']
    active1, active2 = ['']*2

    def vars_for_template(self):
        fields_to_pass = self.form_fields
        model_to_pass = self.form_model
        myform = MyFormWrapper(model_to_pass, fields_to_pass)

        vs = {'form': myform,
              'title': self.title,
              }
        vs.update(self.extra_vars())
        return vs

    def extra_vars(self):
        return {}
# registering tag filter to refer to participant.var label


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


def guessing_payoff(x, y):
    diff = abs(x-y)
    if diff <= Constants.GuessThreshold:
        return Constants.GuessPayoff
    else:
        return 0


def assign_results(player,partner):
    # part one
    sender = random.choice([True, False])
    if sender:
        player.myrole = 'Sender'
        player.profit1 = Constants.endowment-player.ns6_4
    else:
        player.myrole = 'Receiver'
        player.profit1 = partner.ns6_4

    # normative expectations guesing
    player.profit2 = guessing_payoff(partner.ns6_2, player.ns6_1)
    player.profit3 = guessing_payoff(partner.ns6_4, player.ns6_3)
    profit = player.profit1 + player.profit2 + player.profit3
    return profit


class ResultsWaitPage(WaitPage):
    wait_for_all_groups = True

    def after_all_players_arrive(self):
        players = self.subsession.get_players()
        if len(players) > 1:
            for p in self.subsession.get_players():
                randomplayer = random.choice([o for o
                                              in p.get_others_in_subsession()])
                p.payoff = assign_results(p, randomplayer)
        else:
            myself = self.subsession.get_players()[0]
            myself.payoff = assign_results(myself, myself)


class Results(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds



    # def offer(self):
    #     return Constants.endowment - self.player.kept
    #
    def vars_for_template(self):

        allplayers = self.subsession.get_players()
        alldata = []
        descriptions = Constants.descriptions
        for i in range(1,5):
            tempdict = {}
            tempdict['name']='ns6_{}'.format(i)
            tempdict['description']=descriptions[i-1]
            tempdict['data'] = [getattr(p, tempdict['name']) for p in allplayers]
            tempdict['average'] = round(sum(tempdict['data'])/len(tempdict['data']),1)
            tempdict['you'] = int(getattr( self.player,tempdict['name']))
            tempdict['data'] = safe_json(tempdict['data'])
            alldata.append(tempdict)
        return{'data': alldata}


li = [Introduction]
for x in range(1, 5):
    globals()['X%i' % x] = type('X%i' % x, (MyPage,),
                                dict(title="Question {}".format(x),
                                form_fields=['ns6_{}'.format(x)]))
    temp = globals()['X%i' % x]
    li.append(temp)

page_sequence = [
    ResultsWaitPage,
    Results,
]
page_sequence = li +page_sequence
