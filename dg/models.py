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
    descriptions = dict(norm_belief='Лично думаю, сколько надо дать другому',
                        norm_expectation='Думаю, сколько люди ожидают получить',
                        empirical_expectation='Думаю, сколько люди фактически дают',
                        decision='Собственное решение')


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
        verbose_name="""Я считаю, что <span class="alert alert-danger">Отправитель</span> 
        должен отдать Получателю такую долю из 
        {} токенов:""".format((Constants.endowment)),
        doc="""Personal normative belief"""
    )
    norm_expectation = MyOwnField(
        image='2',
        verbose_name="""
        Я полагаю, что в среднем <span class="alert alert-danger">Получатель</span>  ожидает 
         получить от Отправителя следующее число из {} токенов:""".format((Constants.endowment)),
        doc="""Normative expectation"""
    )
    empirical_expectation = MyOwnField(
        image='1',
        verbose_name="""Я думаю, что в среднем <span class="alert alert-danger">Получатель</span> передаст Отправителю
         следующее число из {} токенов:""".format((Constants.endowment)),
        doc="""Empirical expectation"""
    )
    decision = MyOwnField(
        image='1',
        verbose_name="""Я передаю отправителю из числа имеющихся у меня {} токенов
        :""".format((Constants.endowment)),
        doc="""Normative behaviour""",
    )
