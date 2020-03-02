#!/usr/bin/env python3
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .forms import AnyVideoDownloadForm
import youtube_dl
import os
import re
from django.contrib import messages
from pyembed.core import PyEmbed
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


def anydownload(request):
    MusicPath = os.path.expanduser("~") + "/Desktop/"
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

            # 137  22  18    best 18 worse

            # ("title       : {}".format((meta['title'])))
            # ("upload date : {}".format((meta['upload_date'])))
            # ("uploader    : {}".format((meta['uploader'])))
            # ("uploader_id : {}".format((meta['uploader_id'])))
            # ("channel_id  : {}".format((meta['channel_id'])))
            # ("duration    : {}".format((meta['duration'])))
            # ("description : {}".format((meta['description'])))

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
            ydl_opts = {
                'format': 'best',
                'outtmpl': '~/Downloads/%(title)s.%(ext)s',
                'noplaylist': True,
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([URL_LIST])

            '''
            f"youtube-dl -f best --output ~/Desktop/%(title)s.%(ext)s  -ik --format mp4  --yes-playlist  {URL_LIST}"'''
            messages.success(request, 'Video has been successfully downloaded !')
            return redirect('anyhome')
        return render(request, "anyvideo/anydownload.html")

# os.system("youtube-dl -f best --output ~/Downloads/%(title)s.%(ext)s  -cik --format mp4  --yes-playlist -a aa.txt ")
# -f best forthe besst quality
