# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.shortcuts import render, redirect
from .forms import hastag
from django.http import HttpResponse
import Main


def index(request):
    form = hastag()
    hastag_valid = hastag(request.POST or None)
    if hastag_valid.is_valid():
        data = hastag_valid.cleaned_data
        has = data.get("has")
        print has
        # Main.main(has)
        return redirect('go_search')
    return render(request, "index.html", {"form": form})


def go_search(request):
    jsn = Main.get_all_node()
    return render(request, "search.html")
