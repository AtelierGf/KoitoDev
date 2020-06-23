import json,config
import random
from requests_oauthlib import OAuth1Session

def main():

    CKey=config.TW_CONSUMER_KEY.strip()
    CSKey=config.TW_CONSUMER_SECRET.strip()
    TKey=config.TW_TOKEN.strip()
    TSKey=config.TW_TOKEN_SECRET.strip()

    twitter=OAuth1Session(CKey,CSKey,TKey,TSKey)
 
    trend_get = 'https://api.twitter.com/1.1/trends/place.json'
    update = "https://api.twitter.com/1.1/statuses/update.json"
    
    #dame="わたし、{}がいないとだめなんですよー!"
    yoyu="い、いえ！{}はよゆーですよ\n全然平気です!"

    template=[yoyu]
            
    res=twitter.get(trend_get,params={"id":23424856})

    if res.status_code == 200:
        print("Success.")
    else:
        print("Failed. : %d"% res.status_code)

    trend_list=[]
    trends=json.loads(res.text)

    for trend in trends:
        for one in trend["trends"]:
            trend_list.append(one["name"].lstrip('#'))
                
    important=trend_list[random.randint(0,len(trend_list))]

    r=random.randint(0,0)
    tweet={"status":template[r].format(important)}

    res=twitter.post(update,params=tweet)
    if res.status_code == 200:
        print("Success.")
    else:
        print("Failed. : %d"% res.status_code)

if __name__=='__main__':
    main()
