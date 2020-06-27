# -*- coding:utf-8 -*-
import MeCab 
import json,config,random,re
from requests_oauthlib import OAuth1Session

def main():
    CKey=config.TW_CONSUMER_KEY.strip()
    CSKey=config.TW_CONSUMER_SECRET.strip()
    TKey=config.TW_TOKEN.strip()
    TSKey=config.TW_TOKEN_SECRET.strip()

    twitter=OAuth1Session(CKey,CSKey,TKey,TSKey)

    home_url="https://api.twitter.com/1.1/statuses/home_timeline.json"
    update_url = "https://api.twitter.com/1.1/statuses/update.json"

    dame="{}、わたしがいないとだめなんですよー！"
    #yoyu="い、いえ！{}はよゆーですよ\n全然平気です！"
    yoyu="{}テスト2"
    template=[dame,yoyu] 

    t=MeCab.Tagger("-Ochasen")
    #t=MeCab.Tagger("-Ochasen-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd")

    t.parse("")
    res=twitter.get(home_url)
    if res.status_code == 200:
        timeline=(json.loads(res.text))
        tweet = timeline[random.randint(0,len(timeline)-1)]
        m = t.parseToNode(tweet["text"])
        nouns = []
        while m:
            if m.feature.split(',')[0] == '名詞':
                nouns.append(m.surface)
            m = m.next

        r1=random.randint(1,1)
        r2=random.randint(0,len(nouns)-1)
        tweet={"status":template[r1].format(nouns[r2])}

        res=twitter.post(update_url,params=tweet)
        if res.status_code == 200:
            print("Success!")
        else:
            print("Failed : %d"% res.status_code)

    else:
        print("Failed: %d"% timeline.status_code)

if __name__=='__main__':
    main()
