from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader


def index(request):
    temlate = loader.get_template('index.html')
    return HttpResponse(temlate.render({}, request))

def cafe(request):
    temlate = loader.get_template('cafe.html')
    return HttpResponse(temlate.render({}, request))

def theme(request):
    temlate = loader.get_template('theme.html')
    return HttpResponse(temlate.render({}, request))

