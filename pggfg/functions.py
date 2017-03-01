from .models import *
from otree.common import safe_json
import json


def preparing_charts(me=None, final=False,isSubsession=False):

    series = []
    if me and not isSubsession:
        mygroupaverage = [[p.round_number,round(p.group.average_contribution),] for p in me.in_all_rounds()]
        mygroupcontribs = [[r.round_number,(a.contribution or 0)] for r in me.group.in_all_rounds() for a in r.get_players()]
        personcontribs = [[p.round_number,p.contribution,] for p in me.in_all_rounds()]
        empty_rounds = range(me.subsession.round_number +1, Constants.num_rounds + 1)
        making_add = list(zip(list(empty_rounds),['']*len(empty_rounds)))
        mygroupcontribs += making_add
        personcontribs += making_add
        series.append({
            'name': 'Your group average',
            'type': 'line',
            'data': mygroupaverage})

        series.append({
            'name': 'Your group members',
            'type': 'scatter',
            'data': mygroupcontribs,
            'marker': {
                    'fillColor': '#FFFFFF',
                    'lineWidth': 1,
                    'lineColor': 'red',
                    'radius': 7,
                    'symbol': 'circle'},
                    })

        series.append({
            'name': 'Your contributions',
            'type': 'line',
            'data': personcontribs,
            'marker': {
                        'radius': 5,
                        }})
    if isSubsession:
        mysubsession = me
    else:
        mysubsession = me.subsession
    if final:
        all_contribs = [[r.round_number,(a.contribution or 0)] for r in mysubsession.in_all_rounds() for a in r.get_players()]
        popsize =len(mysubsession.get_players())
        all_contribs_average = [[r.round_number, round(sum([(p.contribution or 0) for p in r.get_players()])/popsize)] for r in mysubsession.in_all_rounds()]

        series.append({
            'name': 'All participants',
            'type': 'scatter',
            'data': all_contribs,
                        'marker': {
                'fillColor': '#FFFFFF',
                'lineWidth': 1,
                'lineColor':'blue',
                'radius':7,
            } })
        series.append({
            'name': 'Overall average',
            'type': 'line',
            'color': 'rgba(0, 0, 0, 0.2)',
            'lineWidth': 15,
            'data': all_contribs_average,
                        'marker': {
                'enabled':False,
                'fillColor': '#FFFFFF',
                'lineWidth': 1,
                'lineColor':'blue',
                'radius':1,
                'symbol': 'circle',
            } })

    highcharts_series = safe_json(series)
    return highcharts_series