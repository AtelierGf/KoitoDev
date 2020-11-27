# -*- cod1ing:utf-8 -*-
import MeCab 
import json,config,random,re,time
from requests_oauthlib import OAuth1Session

def main():
    CKey=config.TW_CONSUMER_KEY.strip()
    CSKey=config.TW_CONSUMER_SECRET.strip()
    TKey=config.TW_TOKEN.strip()
    TSKey=config.TW_TOKEN_SECRET.strip()
    dic_path=config.MECAB_DIC_PATH.strip()

    #setting twitter api
    twitter=OAuth1Session(CKey,CSKey,TKey,TSKey)
    home_url="https://api.twitter.com/1.1/statuses/home_timeline.json"
    update_url = "https://api.twitter.com/1.1/statuses/update.json"
    fav_url= "https://api.twitter.com/1.1/favorites/create.json"

    #setting mecab's morphological analysis
    t=MeCab.Tagger(r"-Ochasen -d {}".format(dic_path))
    t.parse("")

    #declare tweet utils
    placeholder_1=["{}、わたしがいないとだめなんですよー！","わ、わたしも・・・・・・！\n{}がいないとだめだめかもしれないです・・・・・・"]
    placeholder_2=["{}、わたしがいないと{}なんですよー！","わ、わたしも・・・・・・！\n{}がいないと{}かもしれないです・・・・・・"]
    template=random.choice([placeholder_1,placeholder_2])

    removing = re.compile('[1-9a-z!"#$%&\'\\\\()*+,-./:;<=>?@[\\]^_`{|}~「」〔〕“”〈〉『』【】＆＊・（）＄＃＠。、？！｀＋￥％ー回時間分人週０１２３４５６７８９…。]+')
    url_pattern=re.compile("https?://[\w/:%#\$&\?\(\)~\.=\+\-]+")

    nouns=[]
    adjs=[]

    while True:
      res=twitter.get(home_url,params={"count":10})
      if res.status_code == 200:
        timeline=list(filter(lambda line:line["retweet_count"]==0 and line["in_reply_to_user_id"]==None,json.loads(res.text)))
        random.shuffle(timeline)
        for line in timeline:
            if url_pattern.search(line["text"]):
              continue
            m = t.parseToNode(line["text"])

            # extract a tweet 
            noun = ""
            while m:
                features=m.feature.split(',')
                print(features)
                if features[0] == '名詞' and features[1]=='固有名詞':
                    noun+=m.surface
                elif features[0] == '形容詞':
                    adjs.append(m.surface)
                else:
                    #名詞が続く限り、一つの名詞とする。
                    if noun!="" :
                      nouns.append([line["id"],noun])
                      noun = ""
                m = m.next

        nouns = [nouns[i] for i in range(len(nouns)) if not removing.fullmatch(nouns[i][1]) and 1<len(nouns[i][1])]
        adjs = [adjs[i] for i in range(len(adjs)) if not removing.fullmatch(adjs[i]) and 1<len(adjs[i])]

        print(nouns)
        print(adjs)

        #If getting nouns and adjs succeed, then this loop break.
        if nouns!=[] or adjs!=[]:
           break
        time.sleep(1)
      else:
        print("Failed: %d"% res.status_code)

    which=random.randint(0,1)
    tweet={"status":template[which].format(random.choice(nouns)[1],random.choice(adjs))}

    res1=twitter.post(update_url,params=tweet)
    if res1.status_code == 200:
      print("tweet:Success!")
      res2=twitter.post(fav_url,params={"id":nouns[r2][0]})
      if res2.status_code == 200:
        print("fav:Success!")
      else:
       print("fav:Failed %d"% res2.status_code)
    else:
      print("fav:Failed : %d"% res1.status_code)

if __name__=='__main__':
    main()
