from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext

import requests
import json

TWFY_KEY = 'GWLD65EufaCzDMwrRyGYmsE7'

def index(request):
    return render_to_response('core/index.html', {}, context_instance=RequestContext(request))


def mp(request, mp_id):
    data = {
        'mp' : mp_api(mp_id)
    }
    
    return render_to_response('core/mp.html', data, context_instance=RequestContext(request))


def return_json(data):
    return HttpResponse(json.dumps(data), mimetype='application/javascript')


def lookup(request):
    search = request.GET.get('search', '').lower()
    if len(search) < 2:
        return return_json([])

    json_data=open('core/mps.json').read()
    data = json.loads(json_data)

    result = []
    for mp in data:
        if search in mp['name'].lower():
            result.append(mp)

    return return_json(result)


def distance_meaning(score):
    score = float(score)
    desc = "unknown about";
    if score > 0.95 and score <= 1.0:
        desc = "very strongly against"
    elif score > 0.85:
        desc = "strongly against"
    elif score > 0.6:
        desc = "moderately against"
    elif score > 0.4:
        desc = "a mixture of for and against"
    elif score > 0.15:
        desc = "moderately for"
    elif score > 0.05:
        desc = "strongly for"
    elif score >= 0.0:
        desc = "very strongly for"
    
    return desc

def mp_api_hack(request, mp_id):
    return return_json( mp_api(mp_id) )


def mp_api(mp_id):
    url = 'http://www.theyworkforyou.com/api/getMPInfo?id=%s&output=js&key=%s' % (mp_id, TWFY_KEY)
    r = requests.get(url)
    j = r.json()

    import re
    from collections import defaultdict

    policies = {
        996 : "a transparent Parliament",
        811 : "a smoking ban",
        1051 : "introducing ID cards",
        363 : "introducing foundation hospitals",
        1052 : "university tuition fees",
        1053 : "Labour's anti-terrorism laws",
        1049 : "the Iraq war",
        984 : "replacing Trident",
        1050 : "the hunting ban",
        826 : "equal gay rights",
        1030 : "laws to stop climate change",
        1074 : "greater autonomy for schools",
        1071 : "allowing ministers to intervene in inquests",
        1079 : "removing hereditary peers from the House of Lords",
        1087 : "a stricter asylum system",
        1065 : "more EU integration",
        1110 : "increasing the rate of VAT",
        1084 : "a more proportional system for electing MPs",
        1124 : "automatic enrolment in occupational pensions",
        837 : "a wholly elected House of Lords",
        975 : "an investigation into the Iraq war",
        1132 : "raising England's undergraduate tuition fee cap to 9,000 per year",
        1109 : "encouraging occupational pensions",
    }

    votes = {}

    for item in j:
        if item.startswith('public_whip_dreammp'):

            key = item.replace('public_whip_dreammp', '')
            vote_id = re.findall(r'\d+', key)[0]

            key = key.replace(vote_id + '_', '')

            if vote_id not in votes:
                votes[vote_id] = {}
            votes[vote_id][key] = j[item]

            if int(vote_id) in policies:
                votes[vote_id]['name'] = policies[int(vote_id)]
            # else:
            #     print vote_id

    for vote in votes:
        v = distance_meaning(votes[vote]['distance'])
        votes[vote]['vote'] = v

    photo = None
    import os.path
    if os.path.exists('core/static/images/%s.jpg' % mp_id):
        photo = '%s.jpg' % mp_id
    if os.path.exists('core/static/images/%s.jpeg' % mp_id):
        photo = '%s.jpeg' % mp_id
    if os.path.exists('core/static/images/%s.png' % mp_id):
        photo = '%s.png' % mp_id

    return {
        'name': j['name'] if 'name' in j else "?",
        'party': j['party'] if 'party' in j else "Unknown party",
        'photo': photo,
        'votes': votes
    }