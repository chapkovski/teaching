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

See: Kahneman, Daniel, Jack L. Knetsch, and Richard H. Thaler. "Fairness
and the assumptions of economics." Journal of business (1986):
S285-S300.

"""

# from django.db import models as m

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
    def __init__(self,active1=False,active2=False,*args, **kwargs):
        self.active1=active1
        self.active2=active2
        super(MyFormField, self).__init__(*args,  **kwargs)
        self.widget = forms.NumberInput(attrs={'class':'form-control ',
        'required' : 'required',
        'min':0,'max':Constants.endowment,
        'autofocus' : 'autofocus',})

class MyOwnField(models.IntegerField):
    def __init__(self,*args, **kwargs):
        self.active1=kwargs.pop('active1', None)
        self.active2=kwargs.pop('active2', None)
        kwargs['max'] = Constants.endowment
        kwargs['min'] = 0
        super(MyOwnField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {'form_class': MyFormField,
                    'active1': self.active1,
                    'active2': self.active2}
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
        verbose_name="A sender should give the following share",
        doc="""Personal normative belief"""
    )
    ns6_2 = MyOwnField(
        verbose_name="The receiver expects the following share",
        doc="""Normative expectation"""
    )
    ns6_3 = MyOwnField(
        verbose_name="Most senders give the following share",
        doc="""Empirical expectation"""
    )
    ns6_4 = MyOwnField(
        verbose_name="I give the following share",
        doc="""Normative behaviour""",
    )
