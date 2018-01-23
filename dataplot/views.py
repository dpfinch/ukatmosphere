from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import SiteSelector, VariableChoices, VarCombine
from .models import SelectedSite
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
        return response.get_data()

# Create a simple view for the homepage
def homepage(request):
    return render(request, 'dataplot/homepage.html')

def analysis(request):
    if request.method == 'POST':
        # sites = SiteSelector(request.POST)
        # site = SelectedSite(sitechoice = request.POST['chosen_sites'])
        sites = request.POST.getlist('Site_Choice')

        ## Check if there is anything in the 'Variable_choices' field.
        ## There shouldn't be if its the first iteration of the form.
        if request.POST.getlist('Variable_choices'):

            siteform = SiteSelector(request.POST)

            variableform = VariableChoices(request.POST, sites)
            combineform = VarCombine(request.POST)
            # Add the variables and the combined choice into the session request
            request.session['variables'] = request.POST.getlist('Variable_choices')
            request.session['combine'] = request.POST.getlist('Var_Combine')
            request.session['sites'] = sites

            # print(request.session['active_pages'])
            # if request.get_full_path()[:5] == '/dash':
            #     if request.get_full_path() not in request.session['active_pages']:
            #         print("waaaa")
            # print(request.session['active_pages'])

            ### Create a dictionary of pathnames and tool types.
            # Need to sort out inputs and adding the list of tools.
            # Need to sort out multiple iterations of the same plot
            stnd_tools = ['TimeSeries', 'Histogram'] #, 'Correlation']
            plot_paths = {}
            for tool in stnd_tools:
                random_path = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
                plot_paths['/dash-'+random_path] = tool

            request.session['plot_paths'] = plot_paths

            # Have a list of the plots to be sent to the webpage
            plots = plot_paths.keys()

            return render(request, 'dataplot/dataselector.html', {'siteform':siteform, 'plots':plots, 'graph_preset':True, 'sites':sites,
                'variableform':variableform, 'combineform':combineform, 'site_chosen': True,
                })

        else:
            #request.session['var'] works like a dictionary to save things locally
            request.session['Site'] = sites
            siteform = SiteSelector(request.POST)

            variableform = VariableChoices(request.POST,sites)
            combineform = VarCombine({'Var_Combine':'seperate'})

            return render(request, 'dataplot/dataselector.html', {'siteform':siteform, 'graph_preset':False, 'sites':sites,
                'variableform':variableform, 'combineform':combineform, 'site_chosen': True,
                })

    else:
        siteform = SiteSelector()

        return render(request, 'dataplot/dataselector.html', {'siteform': siteform,
         'graph_preset': False, 'site_chosen': False})

def site_choice(request):
    site = request.session['Site']

    return render(request,'dataplot/chosen_site.html',{'chosen_site': site})

def dash(request, **kwargs):
    return HttpResponse(dispatcher(request))

@csrf_exempt
def dash_ajax(request):
    return HttpResponse(dispatcher(request), content_type='application/json')
