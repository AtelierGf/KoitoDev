import json,config
import random
from requests_oauthlib import OAuth1Session

def main():
    TKey=config.TW_TOKEN.strip()
    TSKey=config.TW_TOKEN_SECRET.strip()
    CKey=config.TW_CONSUMER_KEY.strip()
    CSKey=config.TW_CONSUMER_SECRET.strip()
    User=config.USER.strip()

    twitter=OAuth1Session(CKey,CSKey,TKey,TSKey)

    reply_list=["ぴぇ！？","ぴゃ・・・！？","みんな、わたしがいないとだめなんですよー！"]

    men='https://api.twitter.com/1.1/statuses/mentions_timeline.json' 
    rep="https://api.twitter.com/1.1/statuses/update.json"

    params={"count":5}
    res=twitter.get(men,params=params)

    if res.status_code == 200:
        print("Success.")
    else:
        print("Failed. : %d"% res.status_code)

    mentions=json.loads(res.text)
    mention_me=False

    for mention in mentions:
        '''
        target = tweet id replying
        user = replied user @hogehoge
        '''

        #determine reply to me.
        mention_me=False
        for user in mention["entities"]["user_mentions"]:
            if user["screen_name"] == "TrendKoito":
                mention_me=True

        #If reply to me, reply.
        if mention_me:
            target=mention["id"]
            user=mention["user"]["screen_name"]
            r=random.randint(0,len(reply_list)-1)
            text="@"+user+"\n"+reply_list[r]
            tweet={"status":text,"in_reply_to_status_id":target}
            res=twitter.post(rep,params=tweet)
            if res.status_code == 200:
                print("Success.")
            else:
                print("Failed. : %d"% res.status_code)



    #MyId=t.users.show(screen_name=User)["id"]

if __name__=='__main__':
    main()
