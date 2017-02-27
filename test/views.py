from . import models
from ._builtin import Page as p, WaitPage
from otree.api import Currency as c, currency_range
# from otree.api import models as m
from .models import Constants
from otree.common import safe_json

from otree.api import widgets
from django.forms import modelform_factory
from django import forms

class Page(p):
    def is_displayed(self):
        mycondition = True
        if self.is_displayed:
            return self.is_displayed and mycondition
        return mycondition


class Page1(Page):
    def is_displayed(self):
        mysecondcondition = True
        return mysecondcondition
    def vars_for_template(self):
        self.template_name='test/Contribute'+str(1)+'.html'

    template_name='test/Contribute.html'
    form_model = models.Player
    form_fields = ['patiendID']
    def before_next_page(self):
        # self.player._meta.get_field('decision1_id')._verbose_name ='asdf'
        self.player._meta.get_field('decision1_id').verbose_name =self.player.patiendID

class Page2(Page):
    template_name='test/Contribute.html'
    form_model = models.Player
    form_fields = ['decision1_id']
    def vars_for_template(self):
          print(self.player._meta.get_field('decision1_id')._verbose_name)
    # def  before_next_page(self):
    #     matrix = self.subsession.get_group_matrix()
    #     print(matrix)
    # def before_session_starts(self):
    #     matrix = self.get_group_matrix()
    #     # print(matrix)
    #     print('next round MAZAFAKA')
    #     # matrix=[[matrix[0][1],matrix[0][0]][matrix[0][2]]]
    #     matrix=[[1,2], [3]]
    #     for row in matrix:
    #         row.reverse()
    #     self.set_group_matrix(matrix)
        # print(matrix)




class PartnerChoiceForm(forms.Form):
    def __init__(self,choices,  *args, **kwargs):
        super(PartnerChoiceForm, self).__init__(*args, **kwargs)
        self.fields['partnerchoice'] =forms.CharField(widget=forms.RadioSelect(choices=choices),)


class Results(Page):
    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds
    form_model = models.Player
    form_fields = ['partnerchoice']
    def vars_for_template(self):
        others = self.player.get_others_in_group()
        choices= [(p.id_in_group,"Player {}".format(p.id_in_group)) for p in others]
        print(tuple(choices))
        partnerchoiceform = PartnerChoiceForm(tuple(choices))
        return {'myform':partnerchoiceform,}

class WP(WaitPage):
    def  after_all_players_arrive(self):
        if self.subsession.round_number == Constants.num_rounds:
            for p in self.group.get_players():
                p.participant.vars['loser'] = not p.group.get_player_by_id(p.partnerchoice).partnerchoice==p.id_in_group



page_sequence = [
    Page1,
    Page2,
    # # Contribute,
    # Results,
    # WP,
]
