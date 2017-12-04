from django.shortcuts import render
from django.http import HttpResponse
import requests
from .models import Greeting

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    r = requests.get('http://httpbin.org/status/418')
    print(r.text)
    return HttpResponse('<prep>'+r.text+'wooooaaahhh'+'</prep>')


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

