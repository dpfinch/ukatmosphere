from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import mimetypes

# from .forms import SiteSelector, VariableChoices, VarCombine

from UKAsite.format_tools import PrettyWordList
# from dataplot.dash_driver import dispatcher
import random,string

# Create your views here.

from .server import server

def dispatcher(request):
    '''
    Main function
    @param request: Request object
    '''

    params = {
        'data': request.body,
        'method': request.method,
        'content_type': request.content_type
    }
    with server.test_request_context(request.path, **params):
        server.preprocess_request()
        try:
            response = server.full_dispatch_request()
        except Exception as e:
            response = server.make_response(server.handle_exception(e))
        response.direct_passthrough = False
        return response.get_data()

# Create a simple view for the homepage
def homepage(request):
    # return render(request, 'dataplot/under_construction.html')
    return render(request, 'dataplot/homepage.html')

def about(request):
    return render(request,'dataplot/about.html')

def dash(request, **kwargs):
    return HttpResponse(dispatcher(request))

@csrf_exempt
def dash_json(request):
    return HttpResponse(dispatcher(request), content_type='application/json')

def dash_index(request, **kwargs):
    """Handle Dash CSS requests"""
    return HttpResponse(dispatcher(request), content_type='text/html')


def dash_guess_mimetype(request, **kwargs):
    """Handle Dash requests and guess the mimetype. Needed for static files."""
    # print('Guessing Mimetype')
    url = request.get_full_path().split('?')[0]
    content_type, _encoding = mimetypes.guess_type(url)
    return HttpResponse(dispatcher(request), content_type=content_type)
