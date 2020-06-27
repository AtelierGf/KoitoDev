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

    follower_url = "https://api.twitter.com/1.1/followers/ids.json"
    user_tl_url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    update_url = "https://api.twitter.com/1.1/statuses/update.json"

    dame="{}、わたしがいないとだめなんですよー！"
    yoyu="い、いえ！{}はよゆーですよ\n全然平気です！"
    template=[dame,yoyu]

    t = MeCab.Tagger("-Ochasen -d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd")
    follower=twitter.get(follower_url)

    ids=(json.loads(follower.text))["ids"]
    i=random.randint(0,len(ids)-1)

    timeline=twitter.get(user_tl_url,params={"user_id":i})
    if timeline.status_code == 200:
        tweets = ((json.loads(timeline.text)))
        tweet = tweets[random.randint(0,len(tweets)-1)]
        m = t.parseToNode(tweet["text"])
        nouns = []
        while m:
            if m.feature.split(',')[0] == '名詞':
                nouns.append(m.surface)
            m = m.next

        r1=random.randint(0,1)
        r2=random.randint(0,len(nouns)-1)
        tweet={"status":template[r1].format(nouns[r2])}

        print(tweet["status"])

        res=twitter.post(update_url,params=tweet)
        if res.status_code == 200:
            print("Success!")
        else:
            print("Failed : %d"% res.status_code)

    else:
        print("Failed: %d"% timeline.status_code)

if __name__=='__main__':
    main()
