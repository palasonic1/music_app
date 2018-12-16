# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings

from django.shortcuts import render, render_to_response, redirect, reverse, redirect
from spotify_client import scripts
from django.urls import reverse


def feed(r):
    form = {
        'album_to_change': r.GET.get('album_to_change', ''),
    }

    if form['album_to_change']:
        scripts.change_updates_status(form['album_to_change'], r.user)
        return redirect(reverse('albums:feed'))

    albums = scripts.feed_of_user(r.user)
    return render(r, 'albums/feed.html', {'feed': albums})

