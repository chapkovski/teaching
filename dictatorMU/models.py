from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
from otree.common import safe_json
from django import forms

doc = """
One player decides how to divide a certain amount between himself and the other
player.

before that some questions are asked to reconstruct an audience's normative
and empirical expectations: see more in Bicchieri, C., 2005.
The grammar of society: The nature and dynamics of social norms.
Cambridge University Press. Chapter 1.


"""


class Constants(BaseConstants):
    name_in_url = 'dictatorMU'
    players_per_group = None
    num_rounds = 1
    endowment = 100
    GuessThreshold = 3
    GuessPayoff = 20
    descriptions = ['Personal normative belief',
                    'Normative expectation',
                    'Empirical expectation',
                    'Normative behaviour',
                    ]

class MyFormField(forms.IntegerField):
    def __init__(self,image=None,*args, **kwargs):
        self.image = image

        super(MyFormField, self).__init__(*args,  **kwargs)
        self.widget = forms.NumberInput(attrs={'class':'form-control ',
        'required' : 'required',
        'min':0,'max':Constants.endowment,
        'autofocus' : 'autofocus',})

class MyOwnField(models.IntegerField):
    def __init__(self,*args, **kwargs):
        self.image=kwargs.pop('image', None)

        kwargs['max'] = Constants.endowment
        kwargs['min'] = 0
        super(MyOwnField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'form_class': MyFormField,
                    'image': self.image,
                    }
        defaults.update(kwargs)
        return super().formfield(**defaults)


class Subsession(BaseSubsession):
    def vars_for_admin_report(self):
        allplayers = self.get_players()
        alldata = []
        descriptions = Constants.descriptions
        for i in range(1, 5):
            tempdict = {}
            tempdict['name'] = 'ns6_{}'.format(i)
            tempdict['description'] = descriptions[i-1]
            tempdict['data'] = [getattr(p, tempdict['name'])
                                for p in allplayers]
            try:
                tempdict['average'] = round(sum(tempdict['data']) /
                                            len(tempdict['data']), 1)
            except:
                tempdict['average'] = 'no data yet'
            tempdict['data'] = safe_json(tempdict['data'])
            alldata.append(tempdict)
        return{'data': alldata}


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    myrole = models.CharField()
    profit1 = models.FloatField()
    profit2 = models.FloatField()
    profit3 = models.FloatField()
    profit4 = models.FloatField()

    ns6_1 = MyOwnField(
        image='1',
        verbose_name="""I believe a <span class="alert alert-danger">sender</span> should give the following share of the
        {} to the receiver:""".format(c(Constants.endowment)),
        doc="""Personal normative belief"""
    )
    ns6_2 = MyOwnField(
        image='2',
        verbose_name="""I believe the <span class="alert alert-danger">receiver</span>  expects
         from me as a sender to give him or her the following
         share of the {}:""".format(c(Constants.endowment)),
        doc="""Normative expectation"""
    )
    ns6_3 = MyOwnField(
        image='1',
        verbose_name="""I believe most <span class="alert alert-danger">senders</span> give the following share of the
         {} to receivers:""".format(c(Constants.endowment)),
        doc="""Empirical expectation"""
    )
    ns6_4 = MyOwnField(
        image='1',
        verbose_name="""I give the following amount of the {}
        to the receiver:""".format(c(Constants.endowment)),
        doc="""Normative behaviour""",
    )
