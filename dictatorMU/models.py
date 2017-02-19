from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
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
    endowment = 10
    GuessThreshold = 3
    GuessPayoff = 20

class MyFormField(forms.IntegerField):
    def __init__(self,active1=False,active2=False,*args, **kwargs):
        self.active1=active1
        self.active2=active2
        super(MyFormField, self).__init__(*args,  **kwargs)
        self.widget = forms.NumberInput(attrs={'class':'form-control ','required' : 'required',})

class MyOwnField(models.IntegerField):
    def __init__(self,*args, **kwargs):
        self.active1=kwargs.pop('active1', None)
        self.active2=kwargs.pop('active2', None)
        kwargs['max'] = Constants.endowment
        kwargs['min'] = 0
        super(MyOwnField, self).__init__(*args, **kwargs)


    def formfield(self, **kwargs):
        defaults = {'form_class': MyFormField,'active1':self.active1, 'active2':self.active2}
        defaults.update(kwargs)
        return super().formfield(**defaults)


class Subsession(BaseSubsession):
    def vars_for_admin_report(self):
        payoffs = sorted([p.payoff for p in self.get_players()])
        return {'payoffs': payoffs}


class Group(BaseGroup):
    pass

class Player(BasePlayer):
    ns6_1 = MyOwnField(
    active1=True,
    active2=False,
        verbose_name="""What do you believe a sender should give? <br>
        <b>I believe it is morally appropriate to give the following share of the %i points to receiver B: </b>"""% Constants.endowment
    )
    ns6_2 = MyOwnField(
        active1=True,
        # active2=False,
        verbose_name="""Imagine you are the receiver: what would you morally expect from the sender? <br>
        <b>I believe it is morally appropriate to receive the following share of the %i points to sender A: </b>"""% Constants.endowment

    )
    ns6_3 = MyOwnField(
        active1=True,
        # active2=False,
        verbose_name="""Now put yourself in the shoes of the other receiver: what do you think the receiver morally expects from you? <br>
        If you hit receiver B's actual answer to Questin2 by +/- {} points, you will receive {} points. <br>
        <b>I think receiver B believes it is morally appropriate to receive the following share of the {} points from me: </b>""".format(Constants.GuessThreshold,Constants.GuessPayoff, Constants.endowment)
    )
    ns6_4 = MyOwnField(
        active1=True,
        # active2=False,
        verbose_name="""What is your decision as a sender? <br>
        <b>I will give the following share of the %i points to receiver B: </b>"""% Constants.endowment
    )
    ns6_5 = MyOwnField(
        active1=True,
        # active2=False,
        verbose_name="""Imagine you are the receiver: what would you actually expect the sender to decide?<br>
        If you hit sender A's actual answer by +/- {} points, you will recieve {}points.<br>
        <b>I believe sender A will give the following share of the {} points to me: </b>""".format(Constants.GuessThreshold,Constants.GuessPayoff, Constants.endowment)
    )
    ns6_6 = MyOwnField(
        active1=True,
        # active2=False,
        verbose_name="""Now put yourself in the showes of the other receiver: how do you think the receiver expects you actually to decide?<br>
        If you hit receiver B's actual answer by +/- {} points, you will receive {} points.<br>
        <b>I believe receiver B blieves he/she will receive the following share of the {} points from me: </b>""".format(Constants.GuessThreshold,Constants.GuessPayoff, Constants.endowment)
    )
    def set_payoffs(self):
        self.payoff = (self.kept)
