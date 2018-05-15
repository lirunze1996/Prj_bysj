# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from webservice.models import *


# Create your views here.

def index(request):
    return render(request, 'index.html')


def detail(request):
    mid = request.GET.get("mid")
    content = {}
    if mid is not None:
        m = movie.objects.filter(mid=mid)
        content["m"] = m[0]
        print m
    movies = movie.objects.all()
    content["movies"] = movies
    return render(request, 'detail.html', content)


