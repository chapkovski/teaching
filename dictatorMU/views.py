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
# class MyForm(otree.forms.ModelForm):
#     # pass
#     def __init__(self,model=None, fields=None,*args,**kwargs):
#         self.model=model
#         self.fields=fields
#         # print("FEILDS"+str(fields))
#         return super(MyForm,self).__init__(*args,**kwargs)
from django.forms import ModelForm as mmm
def MyFormWrapper(model_to_pass,fields_to_pass, *args, **kwargs):
    class MyForm(mmm):
        class Meta:
            model = model_to_pass
            fields = fields_to_pass

        def __init__(self):
            kwargs.update({'label_suffix': '<->'})
            super(MyForm, self).__init__(*args, **kwargs)
            kwargs.update({'label_suffix': '<->'})
    return MyForm()





class MyPage(Page):
    # def __init__(self, classtype):
    #     self._type = classtype
    #     self.__name__ ='pidor'

    form_model = models.Player
    template_name = 'dictatorMU/Offer.html'
    title = ''
    form_fields = ['ns6_1']
    # instructions = ''
    active1,active2 = ['']*2
    def vars_for_template(self):
        fields_to_pass = self.form_fields
        model_to_pass = self.form_model
        myform = MyFormWrapper(model_to_pass,fields_to_pass)

        vs = {'form':myform,
            'title': self.title,
            # 'instructions': self.instructions,
            # 'active1':self.active1,
            # 'active2':self.active2,
        }
        vs.update(self.extra_vars())
        return vs

    def extra_vars(self):
        return {}
# registering tag filter to refer to participant.var label
from django.template.defaulttags import register
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


def guessing_payoff(x,y):
    diff = abs(x-y)
    if diff<=Constants.GuessThreshold:
        return Constants.GuessPayoff
    else: return 0

def assign_results(player,partner):
    # part one

    profit1 = random.choice([player.ns6_4, partner.ns6_4])
    profit2 = guessing_payoff(partner.ns6_2, player.ns6_3)
    profit3 = guessing_payoff(partner.ns6_5, player.ns6_6)
    profit = profit1 + profit2 + profit3
    return profit

class ResultsWaitPage(WaitPage):
    wait_for_all_groups = True
    def after_all_players_arrive(self):
        players = self.subsession.get_players()
        if len(players)>1:
            for p in self.subsession.get_players():
                randomplayer = random.choice([o for o in p.get_others_in_subsession()])
                p.payoff = assign_results(p,randomplayer)
        else:
            myself = self.subsession.get_players()[0]
            myself.payoff = assign_results(myself,myself)


class Results(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds



    # def offer(self):
    #     return Constants.endowment - self.player.kept
    #
    def vars_for_template(self):

        allplayers = self.subsession.get_players()
        alldata=[]
        descriptions=['Moral norm: what Sender should do?',
                      'Moral norm: what Receiver should expect?',
                      'Normative expectations: what others expect you to do',
                      'Your decision as Sender',
                      'Empirical expectations regarding Sender',
                      'Empirical expectations regarding Receiver',
        ]
        for i in range(1,7):
            tempdict = {}
            tempdict['name']='ns6_{}'.format(i)
            tempdict['description']=descriptions[i-1]
            tempdict['data'] = [getattr(p, tempdict['name']) for p in allplayers]
            tempdict['average'] = round(sum(tempdict['data'])/len(tempdict['data']),1)
            tempdict['you'] = int(getattr( self.player,tempdict['name']))
            tempdict['data'] = safe_json(tempdict['data'])
            alldata.append(tempdict)
        #  role 
         #
        #  payoff1
        #  normguess
         #
        #  normvalue
        #  payoff2
         #
        #  normguess
        #  normvalue
         #
        #  payoff2

        return{'data':alldata}



li=[]
for x in range(1, 7):
    # print(models.Player._meta.get_field('ns6_%i' % x).verbose_name)

    globals()['X%i'% x] = type('X%i'% x, (MyPage,), dict(title="Question {}".format(x),
    form_fields = ['ns6_{}'.format(x)]))
    temp = globals()['X%i'% x]
    li.append(temp)

page_sequence = [
    ResultsWaitPage,
    Results,
]
page_sequence = li +page_sequence
