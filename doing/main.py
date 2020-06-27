# -*- coding: utf-8 -*-
import json,config,random
from requests_oauthlib import OAuth1Session
import re
import ng_word

def main():

    CKey=config.TW_CONSUMER_KEY.strip()
    CSKey=config.TW_CONSUMER_SECRET.strip()
    TKey=config.TW_TOKEN.strip()
    TSKey=config.TW_TOKEN_SECRET.strip()

    twitter=OAuth1Session(CKey,CSKey,TKey,TSKey)

    trend_url = 'https://api.twitter.com/1.1/trends/place.json'
    update_url = "https://api.twitter.com/1.1/statuses/update.json"
    follower_url = "https://api.twitter.com/1.1/followers/ids.json"
    user_tl_url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    
    dame="{}、わたしがいないとだめなんですよー！"
    yoyu="い、いえ！{}はよゆーですよ\n全然平気です！"
    template=[dame,yoyu]
    trend_list=[]

    res=twitter.get(trend_url,params={"id":23424856})

    follower=twitter.get(follower_url)
    ids=(json.loads(follower.text))["ids"]
    p = re.compile('[\u3041-\u309F]+')
    for i in ids[0:10]:
        timeline=twitter.get(user_tl_url,params={"user_id":i})
        if res.status_code == 200:
            for tweet in ((json.loads(timeline.text))):
                print(p.search(tweet["text"]))
        else:
            print("Failed : %d"% res.status_code)
 

    if res.status_code == 200:
        print("Success!")
        response=json.loads(res.text)

        for trends in response:
            for trend in trends["trends"]:
                trend_list.append(trend["name"].lstrip('#'))

        trend_list=ng_word.filtering(trend_list)
        to_be_embedded=trend_list[random.randint(0,len(trend_list))]

        r=random.randint(0,1)
        tweet={"status":template[r].format(to_be_embedded)}

       #res=twitter.post(update_url,params=tweet)
        if res.status_code == 200:
            print("Success!")
        else:
            print("Failed : %d"% res.status_code)
    else:
        print("Failed : %d"% res.status_code)

if __name__=='__main__':
    main()
