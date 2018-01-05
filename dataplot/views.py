from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import SiteSelector, SITE_CHOICES, SiteCombine
from .models import SelectedSite
from UKAsite.format_tools import PrettyWordList

from dataplot.dash_driver import dispatcher

# Create your views here.

# Create a simple view for the homepage
def homepage(request):
    return render(request, 'dataplot/homepage.html')

def analysis(request):
    if request.method == 'POST':
        # sites = SiteSelector(request.POST)
        # site = SelectedSite(sitechoice = request.POST['chosen_sites'])
        sites = request.POST.getlist('Site_Choice')
        combined = request.POST.getlist('Site_Combine')

        # site.save()
        request.session['Site'] = sites
        siteform = SiteSelector(request.POST)
        combineform = SiteCombine(request.POST)
        plots = ["//plot.ly/~dfinch/158.embed","//plot.ly/~dfinch/160.embed",
            "//plot.ly/~dfinch/150.embed","//plot.ly/~dfinch/146.embed"]

        if len(sites) == 0:
            return render(request, 'dataplot/dataselector.html', {'siteform': siteform, 'graph_preset': False, 'combineform':combineform})

        if len(sites) > 1 :
            sites = PrettyWordList(sites)

        # return redirect('site_choice')
        return render(request, 'dataplot/dataselector.html', {'siteform':siteform, 'plots':plots, 'graph_preset':True, 'sites':sites, 'combineform':combineform})
    else:
        siteform = SiteSelector()
        combineform = SiteCombine()
        return render(request, 'dataplot/dataselector.html', {'siteform': siteform, 'graph_preset': False, 'combineform':combineform})

def site_choice(request):
    site = request.session['Site']

    return render(request,'dataplot/chosen_site.html',{'chosen_site': site})

def dash(request, **kwargs):
    return HttpResponse(dispatcher(request))

@csrf_exempt
def dash_ajax(request):
    ''' '''
    return HttpResponse(dispatcher(request), content_type='application/json')
