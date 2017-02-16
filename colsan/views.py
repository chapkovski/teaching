from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
# from otree.api import models as m
from .models import Constants
from otree.common import safe_json

from otree.api import widgets
from django.forms import modelform_factory
from django import forms

class NameForm(forms.Form):
    # your_name = forms.CharField(label='Your name', max_length=100)
    def __init__(self, fields_to_add, *args, **kwargs):
        super(NameForm, self).__init__(*args, **kwargs)
        CHOICES = (("True", True), ("False",False) )

        for f in fields_to_add:
            self.fields[f] =forms.CharField(widget=forms.Select(attrs={'class':'selector', },choices=CHOICES),
            )
        # self.fields['state'] = State.GetTicketStateField(ticket.Type)
class Introduction(Page):


    """Description of the game: How to play and returns expected"""
    pass


class Contribute(Page):
    """Player: Choose how much to contribute"""

    form_model = models.Player
    form_fields = ['contribution']

    timeout_submission = {'contribution': c(Constants.endowment / 2)}


class ContributionWaitPage(WaitPage):
    """Waiting till all players make their decisions about the contribution"""
    def after_all_players_arrive(self):
        self.group.detect_TLC()

    body_text = "Waiting for other participants to contribute."

class Detection(Page): #here the decision to detect the TLS is taken
    form_model = models.Player
    def vars_for_template(self):
        fields_to_show=[]
        others = self.player.get_others_in_group()
        contribs_to_show = [p.contribution for p in others if p.isTLC]
        verbose_names = ['Participant {}'.format(p.id_in_group) for p in others if p.isTLC]
        fields_to_show = self.get_form_fields()
        myform = NameForm(fields_to_show)
        return {'abclist':zip(myform,contribs_to_show,verbose_names),}

    def get_form_fields(self):
        others = self.player.get_others_in_group()
        fields_to_show = ['detectP{}'.format(p.id_in_group) for p in others if p.isTLC]
        return fields_to_show

    def is_displayed(self):
        ps = self.group.get_players()
        howmanyTLC = self.group.numTLCs
        print("AND HOW JE MANY? {}".format(howmanyTLC))
        if howmanyTLC == 0:
            toshow = False
        elif howmanyTLC == 1 and self.player.isTLC:
            toshow = False
        else:
            toshow = True
        return toshow
        # return not self.player.isTLC
    """Participants take decision whether to detect the smallest contributor"""
    pass

class DetectionWaitPage(WaitPage):
    """Waiting for the group to finish the detection stage before showing them results"""
    pass

class Results(Page):
    """Players payoff: How much each has earned in this round"""

    def vars_for_template(self):
        pass
class FinalResults(Page):
    """Final earnings are shown"""
    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds


page_sequence = [
    # Introduction,
    Contribute,
    ContributionWaitPage,
    Detection,
    DetectionWaitPage,
    Results
]
