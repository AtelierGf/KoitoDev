import json,config,random
from requests_oauthlib import OAuth1Session

def main():
    TKey=config.TW_TOKEN.strip()
    TSKey=config.TW_TOKEN_SECRET.strip()
    CKey=config.TW_CONSUMER_KEY.strip()
    CSKey=config.TW_CONSUMER_SECRET.strip()
    User=config.USER.strip()

    twitter=OAuth1Session(CKey,CSKey,TKey,TSKey)

    reply_list=["ぴぇ！？","ぴゃ・・・！？","みんな、わたしがいないとだめなんですよー！"]

#    with open(r"./reply_log.txt",mode="r") as f:
#        temp=f.readline()
#        since_id=temp if temp!="" else 1

    mention_url='https://api.twitter.com/1.1/statuses/mentions_timeline.json' 
    update_url="https://api.twitter.com/1.1/statuses/update.json"
    params={"count":5}

    res=twitter.get(mention_url,params=params)
    if res.status_code == 200:
        print("Success getting mention!")
        mentions=json.loads(res.text)

        print(mentions)
        for mention in mentions:
            '''
            replying_tweet_id = tweet id replying now
            user_name = replied me user @screenname
            '''
            #get information to reply and record this id.
            target_tweet_id=mention["id"]
            user_name=mention["user"]["screen_name"]
            with  open(r"./reply_log.txt",mode="w") as f:
                print(target_tweet_id) 
                f.write(str(target_tweet_id))

            #generate reply text
            r=random.randint(0,len(reply_list)-1)
            reply_text="@"+user_name+"\n"+reply_list[r]
            tweet={"status":reply_text,"in_reply_to_status_id":target_tweet_id}

            #attempt a post request.
            res=twitter.post(update_url,params=tweet)
            if res.status_code == 200:
                print("Success!")
            else:
                print("Failed : %d"% res.status_code)
    else:
        print("Failed. : %d"% res.status_code)

        #determine reply to me.
        #for user in mention["entities"]["user_mentions"]:
            #if user["screen_name"] == "TrendKoito":
                #mention_me=True

if __name__=='__main__':
    main()
