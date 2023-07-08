# coding: utf-8

import feedparser
import time

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
        g.close
        break

    else:
        title = now_entry['title']
        page_url = now_entry['link']
        if now_entry['date'] != now_entry['issued']:
            update_date_base = now_entry['date'][:-15]
            update_date_split = update_date_base.split('-')
            update_date = update_date_split[0]+"年"+update_date_split[1]+"月"+update_date_split[2]

            post_text ="【IPA】("+update_date+" 更新)\n" +title + "\n" + page_url + "\n\nその他の情報はこちら\nhttps://nvnb.blossomsarchive.com/"
            print(post_text+"\n")
            time.sleep(10)
            
        else:

            post_text ="【IPA】\n" +title + "\n" + page_url + "\n\nその他の情報はこちら\nhttps://nvnb.blossomsarchive.com/"
            print(post_text+"\n")
            time.sleep(10)
    i += 1
