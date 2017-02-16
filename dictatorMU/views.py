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

def MyFormWrapper(model_to_pass,fields_to_pass, *args, **kwargs):
    class MyForm(otree.forms.ModelForm):
        class Meta:
            model = model_to_pass
            fields = fields_to_pass

        def __init__(self):
            kwargs.setdefault('label_suffix', '<->')
            super(MyForm, self).__init__(*args, **kwargs)

    return MyForm()





class MyPage(Page):
    form_model = models.Player
    template_name = 'dictatorMU/Offer.html'
    def vars_for_template(self):
        fields_to_pass = self.form_fields
        model_to_pass = self.form_model
        myform = MyFormWrapper(model_to_pass,fields_to_pass)
        return {'form':myform,
                 'title':self.title,
                 'instructions':self.instructions,}



class Introduction(MyPage):
    form_model = models.Player
    form_fields = ['kept','others_belief','norm']

# class ResultsWaitPage(WaitPage):
#     def after_all_players_arrive(self):
#         self.group.set_payoffs()
#
#     def vars_for_template(self):
#         if self.player.id_in_group == 2:
#             body_text = "You are participant 2. Waiting for participant 1 to decide."
#         else:
#             body_text = 'Please wait'
#         return {'body_text': body_text}
# class MyPage(Page):
#     form_model = models.Player
#     template_name = 'dictatorMU/Offer.html'
#     title = ''
#     instructions = ''
#     def vars_for_template(self):
#         vs = {
#             'title': self.title,
#             'instructions': self.instructions,
#         }
#         vs.update(self.extra_vars())
#         return vs
#
#     def extra_vars(self):
#         return {}

class Kept(MyPage):
    form_fields = ['kept']
    title = 'Decision'
    instructions = 'dictatorMU/InstructionsDecision.html'

class Belief(MyPage):
    form_fields = ['belief']
    title = 'Belief'
    instructions = 'dictatorMU/InstructionsBelief.html'

class Norm(MyPage):
    form_fields = ['norm']
    title = 'Norm'
    instructions = 'dictatorMU/InstructionsBelief.html'

class Others_belief(MyPage):
    form_fields = ['others_belief']
    title = "Others' beliefs"
    instructions = 'dictatorMU/InstructionsOtherBelief.html'

class Results(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds
    def offer(self):
        return Constants.endowment - self.player.kept

    def vars_for_template(self):
        print('PLAYER KEPT: {}'.format(self.player.kept))
        all_decisions = [random.randint(0,Constants.endowment) for r in range(25)]
        all_beliefs = [random.randint(0,Constants.endowment) for r in range(25)]
        all_norms = [random.randint(0,Constants.endowment) for r in range(25)]
        all_others_beliefs = [random.randint(0,Constants.endowment) for r in range(25)]

        return {
            'all_decisions':safe_json(all_decisions),
            'all_beliefs':safe_json(all_beliefs),
            'all_norms':safe_json(all_norms),
            'all_others_beliefs':safe_json(all_others_beliefs),
            'average_decision':sum(all_decisions)/len(all_decisions),
            'average_belief':sum(all_beliefs)/len(all_beliefs),
            'average_norm':sum(all_norms)/len(all_norms),
            'average_others_belief':sum(all_others_beliefs)/len(all_others_beliefs),
        }


page_sequence = [
    Introduction,
    Kept,
    Belief,
    Norm,
    Others_belief,
    # ResultsWaitPage,
    Results
]
