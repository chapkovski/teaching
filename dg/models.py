from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from django.db.models import Avg
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
    name_in_url = 'dg'
    players_per_group = None
    num_rounds = 1
    endowment = 100
    colors = ['orange', 'blue', 'red', 'green']
    descriptions = dict(norm_belief='Personally, I think how much should I give to another person',
                        norm_expectation='I think how much people expect to get',
                        empirical_expectation='I think how much people actually give',
                        decision='My personal decision')


class MyFormField(forms.IntegerField):
    def __init__(self, image=None, *args, **kwargs):
        self.image = image

        super(MyFormField, self).__init__(*args, **kwargs)
        self.widget = forms.NumberInput(attrs={'class': 'form-control ',
                                               'required': 'required',
                                               'min': 0, 'max': Constants.endowment,
                                               'autofocus': 'autofocus', })


class MyOwnField(models.IntegerField):
    def __init__(self, *args, **kwargs):
        self.image = kwargs.pop('image', None)

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

    def get_data(self):
        r = []
        for j, (field, desc) in enumerate(Constants.descriptions.items()):
            i = {}
            i['name'] = desc
            i['field'] = field
            i['color'] = Constants.colors[j]
            i['data'] = list(self.player_set.values_list(field, flat=True))
            r.append(i)

        return r

    def get_avg_data(self):
        q = {}
        for f in Constants.descriptions.keys():
            q[f] = Avg(f)
        r = self.player_set.aggregate(**q)
        return r

    def get_desc_data(self):
        r = []
        avgs = self.get_avg_data()

        for f in Constants.descriptions.keys():
            i = {}
            i['average'] = avgs[f]
            i['description'] = Constants.descriptions[f]
            r.append(i)
        return r

    def clearing_decisions(self):
        print('CLEARING DECISIONS')

    def vars_for_admin_report(self):
        pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    def get_data_for_chart(self):
        r = self.subsession.get_data()
        for i in r:
            i['my_own'] = getattr(self, i['field'])
        return r

    def get_full_data(self):
        r = []
        avgs = self.subsession.get_avg_data()

        for f in Constants.descriptions.keys():
            i = {}
            i['you'] = getattr(self, f)
            i['average'] = avgs[f]
            i['description'] = Constants.descriptions[f]
            r.append(i)
        return r

    norm_belief = MyOwnField(
        image='1',
        verbose_name="""I think that <span class="alert alert-danger">Sender</span> 
        must give Receiver  such a share of 
        {} tokens:""".format((Constants.endowment)),
        doc="""Personal normative belief"""
    )
    norm_expectation = MyOwnField(
        image='2',
        verbose_name="""
        I believe that on average <span class="alert alert-danger">Receiver</span>  expects to get such amount of {} tokens from Sender:""".format((Constants.endowment)),
        doc="""Normative expectation"""
    )
    empirical_expectation = MyOwnField(
        image='1',
        verbose_name="""I think that on average <span class="alert alert-danger">Receiver</span> will transfer to Sender
         such amount of {} tokens:""".format((Constants.endowment)),
        doc="""Empirical expectation"""
    )
    decision = MyOwnField(
        image='1',
        verbose_name="""I transfer {} tokens from among the available ones to Sender
        :""".format((Constants.endowment)),
        doc="""Normative behaviour""",
    )
