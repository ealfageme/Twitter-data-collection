# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .forms import hastag
import neo4j as n
import thread


def index(request):
    form = hastag()
    hastag_valid = hastag(request.POST or None)
    if hastag_valid.is_valid():
        data = hastag_valid.cleaned_data
        has = data.get("has")
        time = data.get("time")
        print has,": ", time," minutes"
        x = n.neo4j()
        thread.start_new(x.main, (has, time))
        return redirect('go_search')
    return render(request, "index.html", {"form": form})


def go_search(request):
    return render(request, "search.html")
