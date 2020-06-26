import json,config,random
from requests_oauthlib import OAuth1Session

def main():

    CKey=config.TW_CONSUMER_KEY.strip()
    CSKey=config.TW_CONSUMER_SECRET.strip()
    TKey=config.TW_TOKEN.strip()
    TSKey=config.TW_TOKEN_SECRET.strip()

    twitter=OAuth1Session(CKey,CSKey,TKey,TSKey)
 
    trend_get = 'https://api.twitter.com/1.1/trends/place.json'
    update = "https://api.twitter.com/1.1/statuses/update.json"
    
    dame="{}、わたしがいないとだめなんですよー！"
    yoyu="い、いえ！{}はよゆーですよ\n全然平気です！"

    template=[dame,yoyu]

    res=None
    retry=0
    while(retry<100):
        res=twitter.get(trend_get,params={"id":23424856})

        if res.status_code == 200:
            print("Success.")
            break
        else:
            print("Failed. : %d"% res.status_code)
            retry+=1

    trend_list=[]
    trends=json.loads(res.text)

    for trend in trends:
        for one in trend["trends"]:
            trend_list.append(one["name"].lstrip('#'))

    #trend_list=list(filter(trend_list,))
    important=trend_list[random.randint(0,len(trend_list))]

    r=random.randint(0,1)
    tweet={"status":template[r].format(important)}

    res=twitter.post(update,params=tweet)
    if res.status_code == 200:
        print("Success.")
    else:
        print("Failed. : %d"% res.status_code)

if __name__=='__main__':
    main()
