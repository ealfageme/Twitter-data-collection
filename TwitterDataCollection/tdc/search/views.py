# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .forms import hastag
import Main


def index(request):
    form = hastag()
    hastag_valid = hastag(request.POST or None)
    if hastag_valid.is_valid():
        data = hastag_valid.cleaned_data
        has = data.get("has")
        print has
        Main.main(has)
        return redirect('go_search')
    return render(request, "index.html", {"form": form})


def go_search(request):
    return render(request, "search.html")
