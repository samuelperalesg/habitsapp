from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

# Welcome View
def welcome(request):
	return render(request, 'welcome.html')
