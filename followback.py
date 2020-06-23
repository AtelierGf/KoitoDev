import config
from twitter import *

def main():
    #文字列前後の余計な空白を削除
    TKey=config.TW_TOKEN.strip()
    TSKey=config.TW_TOKEN_SECRET.strip()
    CKey=config.TW_CONSUMER_KEY.strip()
    CSKey=config.TW_CONSUMER_SECRET.strip()
    User=config.USER.strip()

    t=Twitter(auth=OAuth(TKey,TSKey,CKey,CSKey))
    

    followers=t.followers.list()
    for follower in followers["users"]:
        if ("智代子" in follower["description"]) | ("シャニ" in follower["description"]):
            t.friendships.create(user_id=follower["id"])

if __name__=='__main__':
    main()
