#!/usr/bin/env python3
from django.shortcuts import render, redirect
from .forms import YtDownloaderForm
from pytube import YouTube
import os
from django.contrib import messages
from mimetypes import MimeTypes
from urllib.request import pathname2url
from django.http import HttpResponse
import youtube_dl
PY = ''
url=''

# Create your views here.

def serve_file_helper():
    file_path = '/home/bigsandip/video.mp4'
    filename = os.path.basename(file_path)
    mime = MimeTypes()
    url = pathname2url(file_path)
    mimetype, encoding = mime.guess_type(url)
    f = open(file_path, 'rb')
    # response = HttpResponse(f, content_type='application/force-download')
    response = HttpResponse(f.read(), content_type=mimetype)
    response['Content-Length'] = os.path.getsize(file_path)
    # encodes the filename parameter of Content-Disposition header
    # http://stackoverflow.com/a/20933751
    response['Content-Disposition'] = \
        "attachment; filename=\"%s\"; filename*=utf-8''%s" % \
        (filename, filename)
    return response


def remove_file():
    os.remove('/home/bigsandip/Downloads/ytvideo.mp4')


def home(request):
    global PY
    global url
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
    MusicPath = "/home/bigsandip/Downloads"
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
            remove_file()
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio',
                'outtmpl': '~/Downloads/ytvideo.mp4',
                'noplaylist': True,
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                return serve_file_helper()
                messages.success(request, 'Video has been successfully downloaded !')
                return redirect('home')
            return render(request, "youtube/download.html", {"ad": PY.title, "id": PY.video_id, 'views': PY.views})

        elif amd == '720p':
            remove_file()
            videos_720 = PY.streams.get_by_itag('22')
            if videos_720 is None:
                videos_720 = PY.streams.filter(progressive=True, subtype='mp4').first()
                messages.success(request, 'Video has been successfully downloaded !')
                videos_720.download(MusicPath)
                return redirect('home')
            else:
                videos_720.download(output_path=MusicPath, filename='ytvideo')
                return serve_file_helper()
                messages.success(request, 'Video has been successfully downloaded !')
                return redirect('home')
            return render(request, "youtube/download.html", {"ad": PY.title, "id": PY.video_id, 'views': PY.views})

        else:
            remove_file()
            videos_normal = PY.streams.filter(progressive=True, subtype='mp4').first()
            videos_normal.download(output_path=MusicPath, filename='ytvideo')
            return serve_file_helper()
            messages.success(request, 'Video has been successfully downloaded !')
            return redirect('home')
        return render(request, "youtube/download.html", {"ad": PY.title, "id": PY.video_id, 'views': PY.views})
