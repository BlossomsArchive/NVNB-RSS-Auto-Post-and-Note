# coding: utf-8
import feedparser
import time

f = open("nvnb-ipa.txt", "r")
old_up = f.read()
f.close()

entries = feedparser.parse('https://www.ipa.go.jp/security/alert-rss.rdf')['entries']

print(old_up)
i = 0

while (True):
    now_entry = entries[i]
    if now_entry['date'] == old_up:
        new_up = entries[0]['date']
        g = open("nvnb-ipa.txt", "w")
        g.write(new_up)
        g.close
        break

    else:
        title = now_entry['title']
        page_url = now_entry['link']
        
        post_text ="【IPA】\n" +title + "\n" + page_url + "\n\nその他の情報はこちら\nhttps://nvnb.blossomsarchive.com/"
        print(post_text+"\n")
    i += 1
