from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext

import json
import api

# ========================================================
# web views
# ========================================================

def index(request):
    return render_to_response('core/index.html', {}, context_instance=RequestContext(request))


def mp(request, mp_id):
    data = {
        'mp' : api.mp_info(mp_id)
    }
    
    return render_to_response('core/mp.html', data, context_instance=RequestContext(request))


# ========================================================
# api views
# ========================================================

def json_response(data):
    return HttpResponse(json.dumps(data), mimetype='application/javascript')


def lookup(request):
    search = request.GET.get('search', '').lower()
    if len(search) < 2:
        return json_response([])

    return json_response(api.lookup(search))


def mp_info(request, mp_id):
    return json_response(api.mp_info(mp_id))

