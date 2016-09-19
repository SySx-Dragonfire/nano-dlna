#!/usr/bin/env python3
# encoding: UTF-8

import sys

if sys.version_info.major == 3:
    import urllib.request as urllibreq
else:
    import urllib2 as urllibreq

import os
import http.server
import html
import pkgutil


def send_dlna_action(device, data, action):

    action_data = pkgutil.get_data("nanodlna", "templates/action-{}.xml".format(action)).decode("UTF-8")
    action_data = action_data.format(**data).encode("UTF-8")

    headers = { 
      "Content-Type"   : "text/xml; charset=\"utf-8\"",
      "Content-Length" : "{}".format(len(action_data)),
      "Connection"     : "close",
      "SOAPACTION"     : "\"{}#{}\"".format(device["st"], action)
    } 

    request = urllibreq.Request(device["action_url"], action_data, headers)
    urllibreq.urlopen(request)


def play(files_urls, device):

    video_data = {
        "uri_video"  : files_urls["file_video"],
        "type_video" : os.path.splitext(files_urls["file_video"])[1][1:],
    }

    if "file_subtitle" in files_urls and files_urls["file_subtitle"]:

        video_data.update({
            "uri_sub"    : files_urls["file_subtitle"],
            "type_sub"   : os.path.splitext(files_urls["file_subtitle"])[1][1:]
        })

        metadata = pkgutil.get_data("nanodlna", "templates/metadata-video_subtitle.xml").decode("UTF-8")
        video_data["metadata"] = html.escape(metadata.format(**video_data))

    else:
        video_data["metadata"] = ""

    send_dlna_action(device, video_data, "SetAVTransportURI")
    send_dlna_action(device, video_data, "Play")

