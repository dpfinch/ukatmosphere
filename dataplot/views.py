from django.shortcuts import render, redirect
from .forms import SiteSelector, SITE_CHOICES
from .models import SelectedSite
# Create your views here.


# Create a simple view for the homepage
def homepage(request):
    return render(request, 'dataplot/homepage.html')

def analysis(request):
    if request.method == 'POST':
        sites = SiteSelector(request.POST)
        # site = SelectedSite(sitechoice = request.POST['chosen_sites'])
        site = request.POST.getlist('chosen_sites')
        # site.save()
        request.session['Site'] = site


        # return redirect('site_choice')
        return render(request, 'dataplot/dataselector.html', {'form':site})
    else:
        form = SiteSelector()
        return render(request, 'dataplot/dataselector.html', {'form': form})

def site_choice(request):
    site = request.session['Site']

    return render(request,'dataplot/chosen_site.html',{'chosen_site': site})
