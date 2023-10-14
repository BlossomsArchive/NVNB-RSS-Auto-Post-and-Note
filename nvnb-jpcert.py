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

f = open("nvnb-jpcert.txt", "r")
old_up = f.readline().replace("\n", "")
f.close()

entries = feedparser.parse('https://www.jpcert.or.jp/rss/jpcert.rdf')['entries']

new_up = entries[0]['date']
g = open("nvnb-jpcert.txt", "w")
g.write(new_up)
g.close()

i = 0
max_entry = len(entries)

while (True):
    now_entry = entries[i]
    if now_entry['date'] == old_up or i+1 == max_entry:
        break

    else:
        title = now_entry['title']
        page_url = now_entry['link']

        # 送信する記事データ
        post_data = {
            'title': "[JPCERT/CC] "+title,
            'content': "<p>JPCERT/CCの記事リンク</p>"+"<a href= \""+page_url+"\">"+page_url+"</a>",
            'categories': '12',
            'status': 'publish',  # draft=下書き、publish=公開　省略時はdraftになる
            'featured_media':2620,
        }

        # Post APIのURL
        post_api_url = f'{blog_url}/wp-json/wp/v2/posts'

        # 記事投稿リクエスト
        response = requests.post(post_api_url, json=post_data, auth=(api_user, api_password))
        
        post_text ="【JPCERT/CC】\n" +title + "\n" + page_url + "\n\nその他の情報はこちら\nhttps://nvnb.blossomsarchive.com/"
        print(post_text)
        try:
            #SNS投稿API
            # Misskey
            misskey_address = os.environ.get("MISSKEY_SERVER_ADDRESS")
            misskey_token = os.environ.get("MISSKEY_TOKEN")
            api = Misskey(misskey_address)
            api.token = misskey_token
            api.notes_create(text=post_text)
        except:
            pass
        time.sleep(30)
        
    i += 1
