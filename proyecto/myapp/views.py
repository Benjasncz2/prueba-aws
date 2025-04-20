from django.shortcuts import render
from django.http import HttpResponse 
# Create your views here.
def hello(request):
    return HttpResponse("Funcionó la kaga lol")

def sapo(request):
    return HttpResponse("Loko sapo")