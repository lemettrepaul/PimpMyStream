# -*- coding: utf-8 -*-

# Sample Python code for youtube.liveChatMessages.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors


class LiveChat:
    def __init__(self, url):
        self.url = url
        self.live_id = self.get_live_id(self.url)

        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "CLIENT_SECRET_FILE.json"

        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_console()
        self.youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        request = self.youtube.liveBroadcasts().list(
            part="snippet",
            id=self.live_id
        )
        response = request.execute()

        item = response['items']
        snippet = item[0]['snippet']
        self.live_chat_id = snippet['liveChatId']

        request = self.youtube.liveChatMessages().list(
            liveChatId=self.live_chat_id,
            part="snippet"
        )
        response = request.execute()
        self.next_page_tok = response['nextPageToken']

    def get_live_id(self, url):
        # get live id
        index_v = url.index('v')
        index_esp = 0
        esp = True
        try:
            index_esp = url.index('&')
        except:
            esp = False
        if esp:
            stream_id = url[index_v + 2:index_esp]
        else:
            stream_id = url[index_v + 2::]
        return stream_id

    def get_messages(self):
        req = self.youtube.liveChatMessages().list(
            liveChatId=self.live_chat_id,
            part="snippet",
            pageToken=self.next_page_tok
        )
        response = req.execute()

        rep = response['items']
        liste = []
        for x in rep:
            snipp = x['snippet']
            author = snipp['authorChannelId']
            textmdetails = snipp['textMessageDetails']
            message = textmdetails['messageText']
            liste.append((author, message))
            print(message)
        self.next_page_tok = response['nextPageToken']

        return liste
