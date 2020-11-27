import json,config
import random
from requests_oauthlib import OAuth1Session

TKey=config.TW_TOKEN.strip()
TSKey=config.TW_TOKEN_SECRET.strip()
CKey=config.TW_CONSUMER_KEY.strip()
CSKey=config.TW_CONSUMER_SECRET.strip()
User=config.USER.strip()

tl="https://api.twitter.com/1.1/statuses/user_timeline.json"
des="https://api.twitter.com/1.1/statuses/destroy/{}.json"

twitter=OAuth1Session(CKey,CSKey,TKey,TSKey)
res=twitter.get(tl,params={"count":100,"screen_name":User})

if res.status_code == 200:
    timeline=json.loads(res.text)
    for tweet in timeline:
        target_id=tweet["id"]
        params={"id":target_id}
        res2=twitter.post(des.format(target_id),params=params)
        if res2.status_code == 200:
            print("Sucess")
        else:
            print("Failed. : %d"% res2.status_code)

else:
    print("Failed. : %d"% res.status_code)
