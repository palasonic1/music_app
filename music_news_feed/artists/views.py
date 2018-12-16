# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings

from django.shortcuts import render, render_to_response, redirect, reverse
from spotify_client import scripts

def index(r):
    return render(r, 'artists/artists.html')


def search_artists(r):
    form = {
        'artist_name': r.GET.get('artist_name', '')
    }

    search_result = scripts.search_artist(r.user, form['artist_name'])

    return render(r, 'artists/search_artists.html', {'form': form, 'search_result': search_result})

