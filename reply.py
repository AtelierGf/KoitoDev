import json,config,random,os
from requests_oauthlib import OAuth1Session

def main():
    TKey=config.TW_TOKEN.strip()
    TSKey=config.TW_TOKEN_SECRET.strip()
    CKey=config.TW_CONSUMER_KEY.strip()
    CSKey=config.TW_CONSUMER_SECRET.strip()
    User=config.USER.strip()
    twitter=OAuth1Session(CKey,CSKey,TKey,TSKey)

    log_path=config.REPLY_LOG_PATH.strip()
    reply_list=["ぴぇ！？","ぴゃ・・・！？","い、いえ！わたしはよゆーですよ\n全然平気です！"]
    params={"count":5}

    with open(log_path,mode="r") as f:
        line=f.readline()
        id=int(line) if line!="" else 0
        if id:
            params["since_id"]=id

    mention_url='https://api.twitter.com/1.1/statuses/mentions_timeline.json' 
    update_url="https://api.twitter.com/1.1/statuses/update.json"

    res=twitter.get(mention_url,params=params)
    replied_id=[]

    if res.status_code == 200:
        print("Success getting mention!")
        mentions=json.loads(res.text)
        for mention in mentions:
            '''
            replying_tweet_id = tweet id replying now
            user_name = replied me user @screenname
            '''
            #get information to reply and record this id.
            if mention["user"]["screen_name"]==User: continue
            target_tweet_id=mention["id"]
            user_name=mention["user"]["screen_name"]

            #generate reply text
            r=random.randint(0,len(reply_list)-1)
            reply_text="@"+user_name+"\n"+reply_list[r]
            tweet={"status":reply_text,"in_reply_to_status_id":target_tweet_id}

            replied_id.append(target_tweet_id)
   #        attempt a post request.
            res=twitter.post(update_url,params=tweet)
            if res.status_code == 200:
                print("Success!")
            else:
                print("Failed : %d"% res.status_code)
    else:
        print("Failed. : %d"% res.status_code)

    if replied_id !=[]:
        with open(log_path,mode="w") as f:
            replied_id=sorted(replied_id)
            f.write(str(replied_id[-1]))

if __name__=='__main__':
    main()
