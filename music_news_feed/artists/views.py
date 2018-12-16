# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings

from django.shortcuts import render, render_to_response, redirect, reverse

def index(r):
    return render(r, 'artists/artists.html')

