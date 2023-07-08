# coding: utf-8

import feedparser
import requests
import time
import os
from misskey import Misskey

# ブログのURL
blog_url = "https://nvnb.blossomsarchive.com/"

# WordPressのユーザー名
wordpress_user = os.environ.get("WORDPRESS_USER")
api_user = wordpress_user

# アプリケーションパスワード
wordpress_api_password = os.environ.get("WORDPRESS_API_PASSWORD")
api_password = wordpress_api_password
f = open("nvnb-jvn.txt", "r")
old_up = f.read()
f.close()

entries = feedparser.parse('https://jvn.jp/rss/jvn.rdf')['entries']

i = 0

while (True):
    now_entry = entries[i]
    if now_entry['date'] == old_up:
        new_up = entries[0]['date']
        g = open("nvnb-jvn.txt", "w")
        g.write(new_up)
        g.close()
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
                'categories': '10',
                'status': 'publish',  # draft=下書き、publish=公開　省略時はdraftになる
                'featured_media':528,
            }

            # Post APIのURL
            post_api_url = f'{blog_url}/wp-json/wp/v2/posts'

            # 記事投稿リクエスト
            #response = requests.post(post_api_url, json=post_data, auth=(api_user, api_password))

            post_text ="【IPA】("+update_date+" 更新)\n" +title + "\n" + page_url + "\n\nその他の情報はこちら\nhttps://nvnb.blossomsarchive.com/"
            print(post_text+"\n")
            try:
                #SNS投稿API
                # Misskey
                misskey_address = os.environ.get("MISSKEY_SERVER_ADDRESS")
                misskey_token = os.environ.get("MISSKEY_TOKEN")
                api = Misskey(misskey_address)
                api.token = misskey_token
                #api.notes_create(text=post_text)
            except:
                pass
            time.sleep(10)
            
        else:
            # 送信する記事データ
            post_data = {
                'title': "[JVN] "+title,
                'content': "<p>JVNの記事リンク</p>"+"<a href= \""+page_url+"\">"+page_url+"</a>",
                'categories': '10',
                'status': 'publish',  # draft=下書き、publish=公開　省略時はdraftになる
                'featured_media':528,
            }

            # Post APIのURL
            post_api_url = f'{blog_url}/wp-json/wp/v2/posts'

            # 記事投稿リクエスト
            #response = requests.post(post_api_url, json=post_data, auth=(api_user, api_password))

            post_text ="【IPA】\n" +title + "\n" + page_url + "\n\nその他の情報はこちら\nhttps://nvnb.blossomsarchive.com/"
            print(post_text+"\n")
            try:
                #SNS投稿API
                # Misskey
                misskey_address = os.environ.get("MISSKEY_SERVER_ADDRESS")
                misskey_token = os.environ.get("MISSKEY_TOKEN")
                api = Misskey(misskey_address)
                api.token = misskey_token
                #api.notes_create(text=post_text)
            except:
                pass
            time.sleep(10)
    i += 1
