from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader


def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render({}, request))

def cafe(request):
    template = loader.get_template('cafe.html')
    return HttpResponse(template.render({}, request))

def theme(request):
    template = loader.get_template('theme.html')
    return HttpResponse(template.render({}, request))

