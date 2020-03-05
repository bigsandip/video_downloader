#!/usr/bin/env python3
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .forms import AnyVideoDownloadForm
import youtube_dl
import os
import re
from django.contrib import messages
from pyembed.core import PyEmbed
from mimetypes import MimeTypes
from urllib.request import pathname2url
from django.http import HttpResponse
# from pyoembed import oEmbed, PyOembedException
URL_LIST = ''

# Create your views here.


def home(request):
    global URL_LIST
    if request.method == 'POST':
        form = AnyVideoDownloadForm(request.POST)
        if form.is_valid():
            URL_LIST = form.cleaned_data['url']
            return redirect('anydownload')
    else:
        form = AnyVideoDownloadForm()
        return render(request, 'anyvideo/home.html', {'form': form})


def serve_file_helper():
    file_path = '/home/bigsandip/Downloads/video.mp4'
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
    # f.close()
    # os.remove(file_path)
    return response


def remove_file():
    os.remove('/home/bigsandip/Downloads/video.mp4')


def anydownload(request):
    # MusicPath = os.path.expanduser("~") + "/Desktop/"
    if request.method == 'GET':
        ydl_opts = {
            # 'logger': MyLogger(),
            'quiet': True,
            'skip_download': True,
            'match_filter': youtube_dl.utils.match_filter_func("!is_live"),
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            meta = ydl.extract_info(URL_LIST, download=False)
            new_url1 = PyEmbed().embed(URL_LIST)
            new_url = (re.search("(?P<url>https?://[^\s]+)", new_url1).group("url"))

            context = {
                'title': (f"{meta['title']}"),
                'uploader': (f"{meta['uploader']}"),
                # 'duration': (f"{duration1}"),
                'url': new_url,
                'videos_1080': f"youtube-dl -f 137 --skip-download  {URL_LIST} ",
                'videos_720': (f"youtube-dl -f 22 --skip-download  {URL_LIST}"),
                'videos_normal': (f"youtube-dl -f best --skip-download  {URL_LIST} "),
            }

            return render(request, 'anyvideo/anydownload.html', context)

    if request.method == 'POST':
        amd = request.POST['type']
        if amd == '1080p':
            videos_1080 = os.system(f"youtube-dl -f 137 --skip-download  {URL_LIST} ")
            if videos_1080 is None:
                (f"youtube-dl -f best --output ~/Downloads/%(title)s.%(ext)s  -ik --format mp4  --yes-playlist {URL_LIST} ")
                # (f"youtube-dl -f best --output os.path.expanduser("~")/%(title)s.%(ext)s  -ik --format mp4  --yes-playlist {URL_LIST} ")

            else:
                (f"youtube-dl -f 137 --output ~/Downloads/%(title)s.%(ext)s  -ik --format mp4  --yes-playlist {URL_LIST} ")
            return render(request, "anyvideo/anydownload.html")

        elif amd == '720p':
            videos_720 = (f"youtube-dl -f 22 --skip-download {URL_LIST} ")
            if videos_720 is None:
                os.system(f"youtube-dl -f best --output ~/Downloads/%(title)s.%(ext)s  -ik --format mp4  --yes-playlist {URL_LIST} ")
            else:
                (f"youtube-dl -f 22 --output ~/Downloads/%(title)s.%(ext)s  -ik --format mp4  --yes-playlist {URL_LIST} ")
            return render(request, "anyvideo/anydownload.html")

        else:
            remove_file()
            ydl_opts = {
                'format': 'best',
                'outtmpl': '~/Downloads/video.mp4',
                'noplaylist': True,
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([URL_LIST])
            messages.success(request, 'Video has been successfully downloaded !')
            return serve_file_helper()
            # return redirect('anyhome')
        return render(request, "anyvideo/anydownload.html")
