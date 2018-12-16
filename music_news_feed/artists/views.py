# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings

from django.shortcuts import render, render_to_response, redirect, reverse, redirect
from spotify_client import scripts
from django.urls import reverse

def index(r):
    return render(r, 'artists/artists.html')


def search_artists(r):
    form = {
        'artist_name': r.GET.get('artist_name', ''),
        'add_artist': r.GET.get('add_artist', ''),
        'rm_artist': r.GET.get('rm_artist', ''),
    }

    if form['add_artist']:
        scripts.add_artist_to_user(form['add_artist'], r.user)
        return redirect("%s?artist_name=%s" % (reverse('artists:search_artists'), form['artist_name']))

    if form['rm_artist']:
        #scripts.add_artist_to_user(form['rm_artist'], r.user)
        return redirect("%s?artist_name=%s" % (reverse('artists:search_artists'), form['artist_name']))

    search_result = scripts.search_artist(r.user, form['artist_name'])

    return render(r, 'artists/search_artists.html', {'form': form, 'search_result': search_result})

