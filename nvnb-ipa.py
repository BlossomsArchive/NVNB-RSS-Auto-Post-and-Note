# coding: utf-8
import feedparser
import time

f = open("nvnb-ipa.txt", "r")
old_up = f.read()
f.close()

entries = feedparser.parse('https://www.ipa.go.jp/security/alert-rss.rdf')['entries']
i = 0

while (True):
    if old_up == entries[i]["updated"] :
        new_up = entries[0]["updated"]
        g = open("nvnb-ipa.txt", "w")
        g.write(new_up)
        g.close
        break
    else:
        title = entries[i]['title']
        page_url = entries[i]['link']
        
        post_text ="【IPA】\n" +title + "\n" + page_url + "\n\nその他の情報はこちら\nhttps://nvnb.blossomsarchive.com/"
        print(post_text+"\n")
    print(entries[i]["updated"])
    i = i+1
