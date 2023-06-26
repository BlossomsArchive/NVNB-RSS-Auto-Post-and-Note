#!/usr/bin/env python3
# coding: utf-8

import feedparser
import requests
import os
from misskey import misskey


# ブログのURL
blog_url = '(例:https://nvnb.blossomsarchive.com)'

# WordPressのユーザー名
api_user = ''

# アプリケーションパスワード
api_password = ''

# 前回チェック時の最新の投稿が入っているテキストファイルのパス
local_path = ""

if os.path.exists(local_path):
    with open(local_path) as f:
        old_up = f.read()
        f.close

entries = feedparser.parse('https://jvndb.jvn.jp/ja/rss/jvndb.rdf')['entries']

api = misskey('misskey.io')
#MisskeyのAPIトークン
api.token = ''

new_up = entries[0]['date']
with open(local_path, mode='w') as f:
    f.write(new_up)
    f.close

i = 0

while (True):
    now_entry = entries[i]
    if now_entry['date'] == old_up:
        break

    else:
        title = now_entry['title']
        page_url = now_entry['link']
        if now_entry['date'] != now_entry['issued']:
            update_date_base = now_entry['date'][:-12]
            update_date_split = update_date_base.split('-')
            update_date = update_date_split[0]+"年"+update_date_split[1]+"月"+update_date_split[2]+"日"
            post_text = "[JVN iPedia] ("+update_date+" 更新)"+title

            # 送信する記事データ
            post_data = {
                'title': post_text,
                'content': "<p>JVN iPediaの記事リンク</p>"+"<a href= \""+page_url+"\">"+page_url+"</a>",
                'categories': '0', #投稿カテゴリのid
                'status': 'publish',  # draft=下書き、publish=公開　省略時はdraftになる
                'featured_media':000, #サムネ画像のid
            }

            # Post APIのURL
            post_api_url = f'{blog_url}/wp-json/wp/v2/posts'

            # 記事投稿リクエスト
            response = requests.post(post_api_url, json=post_data, auth=(api_user, api_password))
            
            api.notes_create(text="[JVN iPedia] ("+update_date+" 更新)\n"+title+"\n"+page_url +"\n\nその他の情報はこちら\nnvnb.blossomsarchive.com")

            
        else:
            # 送信する記事データ
            post_data = {
                'title': "[JVN iPedia] "+title,
                'content': "<p>JVN iPediaの記事リンク</p>"+"<a href= \""+page_url+"\">"+page_url+"</a>",
                'categories': '0',
                'status': 'publish',  # draft=下書き、publish=公開　省略時はdraftになる
                'featured_media':000,
            }

            # Post APIのURL
            post_api_url = f'{blog_url}/wp-json/wp/v2/posts'

            # 記事投稿リクエスト
            response = requests.post(post_api_url, json=post_data, auth=(api_user, api_password))

            api.notes_create(text="[JVN iPedia]\n"+title+"\n"+page_url +"\n\nその他の情報はこちら\nnvnb.blossomsarchive.com")
        l = 0
    i += 1
