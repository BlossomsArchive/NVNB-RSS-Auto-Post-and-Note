#!/usr/bin/env python3
# coding: utf-8

import feedparser
import requests
import os
from misskey import misskey


# ブログのURL
blog_url = ''

# WordPressのユーザー名
api_user = ''

# アプリケーションパスワード
api_password = ''

local_path = ""
old_up = ""
if os.path.exists(local_path):
    with open(local_path) as f:
        old_up = f.read()
        f.close

entries = feedparser.parse('https://jvn.jp/rss/jvn.rdf')['entries']

api = misskey('misskey.io')
api.token = ''

i = 0

while (True):
    now_entry = entries[i]
    if now_entry['date'] == old_up:
        new_up = entries[0]['date']
        with open(local_path, mode='w') as f:
            f.write(new_up)
            f.close
        break

    else:
        title = now_entry['title']
        page_url = now_entry['link']
        if now_entry['date'] != now_entry['issued']:
            update_date_base = now_entry['date'][:-15]
            update_date_split = update_date_base.split('-')
            update_date = update_date_split[0]+"年"+update_date_split[1]+"月"+update_date_split[2]
            post_text = "[JVN] ("+update_date+" 更新)"+title

            # 送信する記事データ
            post_data = {
                'title': post_text,
                'content': "<p>JVNの記事リンク</p>"+"<a href= \""+page_url+"\">"+page_url+"</a>",
                'categories': '0',
                'status': 'publish',  # draft=下書き、publish=公開　省略時はdraftになる
                'featured_media':000,
            }

            # Post APIのURL
            post_api_url = f'{blog_url}/wp-json/wp/v2/posts'

            # 記事投稿リクエスト
            response = requests.post(post_api_url, json=post_data, auth=(api_user, api_password))

            api.notes_create(text="[JVN] ("+update_date+" 更新)\n"+title+"\n"+page_url +"\n\nその他の情報はこちら\nnvnb.blossomsarchive.com")

            
        else:
            # 送信する記事データ
            post_data = {
                'title': "[JVN] "+title,
                'content': "<p>JVNの記事リンク</p>"+"<a href= \""+page_url+"\">"+page_url+"</a>",
                'categories': '0',
                'status': 'publish',  # draft=下書き、publish=公開　省略時はdraftになる
                'featured_media':000,
            }

            # Post APIのURL
            post_api_url = f'{blog_url}/wp-json/wp/v2/posts'

            # 記事投稿リクエスト
            response = requests.post(post_api_url, json=post_data, auth=(api_user, api_password))

            api.notes_create(text="[JVN]\n"+title+"\n"+page_url +"\n\nその他の情報はこちら\nnvnb.blossomsarchive.com")

        l = 0
    i += 1
