#!/usr/bin/env python3
from django.shortcuts import render, redirect
from .forms import YtDownloaderForm
from pytube import YouTube
import os
from time import sleep
from django.contrib import messages
PY = ''

# Create your views here.


def home(request):
    global PY
    if request.method == 'POST':
        form = YtDownloaderForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            PY = YouTube(url)
            return redirect('/download')
    else:
        form = YtDownloaderForm()
        return render(request, 'youtube/index.html', {'form': form})


def about(request):
    return render(request, 'youtube/about.html')


def policy(request):
    return render(request, 'youtube/policy.html')


def terms(request):
    return render(request, 'youtube/terms.html')


def download(request):
    # global PY
    # MusicPath = "C:\\Users\\Sandip\\Downloads"
    # MusicPath = os.path.expanduser("~") + "/Desktop/"
    # username = os.getenv('username')
    MusicPath = "/home/{}/Downloads".format(username)
    if request.method == 'GET':

        context = {
            'videos_1080': PY.streams.get_by_itag('137'),
            'videos_720': PY.streams.get_by_itag('22'),
            'videos_normal': PY.streams.filter(progressive=True, subtype='mp4').first()
        }

        length = int(PY.length)
        minu = (length / 60)
        roumin = round(minu, 1)
        # time.sleep(200)
        return render(request, "youtube/download.html", {"ad": PY.title, "id": PY.video_id, 'quality': context, 'views': PY.views, 'length': roumin})

    if request.method == 'POST':
        amd = request.POST['type']
        if amd == '1080p':
            # time.sleep(200)
            videos_1080 = PY.streams.get_by_itag('137')
            if videos_1080 is None:
                # time.sleep(200)
                videos_1080 = PY.streams.filter(progressive=True, subtype='mp4').first()
                videos_1080.download(MusicPath)
                messages.success(request, 'Video has been successfully downloaded !')
                return redirect('home')
            else:
                # time.sleep(200)
                videos_1080.download(MusicPath)
                messages.success(request, 'Video has been successfully downloaded !')
                return redirect('home')
            return render(request, "youtube/download.html", {"ad": PY.title, "id": PY.video_id, 'views': PY.views})

        elif amd == '720p':
            videos_720 = PY.streams.get_by_itag('22')
            if videos_720 is None:
                videos_720 = PY.streams.filter(progressive=True, subtype='mp4').first()
                messages.success(request, 'Video has been successfully downloaded !')
                videos_720.download(MusicPath)
                return redirect('home')
            else:
                videos_720.download(MusicPath)
                messages.success(request, 'Video has been successfully downloaded !')
                return redirect('home')
            return render(request, "youtube/download.html", {"ad": PY.title, "id": PY.video_id, 'views': PY.views})

        else:
            # time.sleep(90)
            videos_normal = PY.streams.filter(progressive=True, subtype='mp4').first()
            # time.sleep(90)
            videos_normal.download(MusicPath)
            messages.success(request, 'Video has been successfully downloaded !')
            return redirect('home')
        return render(request, "youtube/download.html", {"ad": PY.title, "id": PY.video_id, 'views': PY.views})
