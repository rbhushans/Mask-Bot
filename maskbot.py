import tweepy
import logging
import json
import requests
import os
import time

from config import create_api
from detect_mask_image import mask_image

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class MaskBot(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me() 

    def on_status(self, tweet):
        logger.info(f"MASKBOT: Processing tweet id {tweet.id}")
        if hasattr(tweet, 'retweeted_status') or tweet.in_reply_to_status_id is not None or \
            tweet.user.id == self.me.id or tweet.user.followers_count < 200 or (hasattr(tweet.user, 'derived') and tweet.user.derived.locations.country != "United States"):
            return
        
        for media in tweet.entities.get("media",[{}]):
            #checks if there is any media-entity
            if media.get("type",None) == "photo":
                # checks if the entity is of the type "photo"
                try:
                    r = requests.get(media["media_url"])
                except:
                    logger.error("MASKBOT: ERROR WITH IMAGE DOWNLOAD")
                    return
                    #r = e.partial

                filename = './tweet_img.jpg'
                headers = r.headers
                try:
                    contentType = str(headers['content-type'])
                except:
                    return

                if contentType == 'image/gif':
                    return
                with open(filename, 'wb') as f:
                    f.write(r.content)

                val = [-1, -1]
                try:
                    val = mask_image(filename)
                except:
                    logger.error("MASKBOT: ERROR WITH MASK DETECTION")
                    return
                #mask, noMask
                total = val[0] + val[1]
                if (total > 1 and val[1] > 0) or val[1] > 1:
                    try:
                        self.api.update_status(
                            status="Put on a mask!",
                            in_reply_to_status_id=tweet.id,
                            auto_populate_reply_metadata=True
                        )
                        logger.info("MASKBOT: TWEET REPLIED TO")
                        logger.info(f"MASKBOT: Replied to tweet  {tweet.text}")
                        logger.info(f"MASKBOT: Mask Detection: {val}")
                        logger.info(f"MASKBOT: There are {val[0]} people with a mask")
                        logger.info(f"MASKBOT: There are {val[1]} people with no mask")
                    except (tweepy.error.TweepError) as e:
                        logger.error("MASKBOT: ERROR WITH RESTRICTED TWEET")
                        return
                    #time.sleep(60)

                if os.path.exists("tweet_img.jpg"):
                    os.remove("tweet_img.jpg")
                else:
                    logger.info("MASKBOT: The file does not exist")

        

                # save to file etc.
    def on_error(self, status):
        logger.error(status)

def main(keywords):
    api = create_api()
    tweets_listener = MaskBot(api)
    stream = tweepy.Stream(api.auth, tweets_listener)
    stream.filter(track=keywords, languages=["en"])

if __name__ == "__main__":
    main(["brunch", "Brunch", "Group", "party", "Party", "group", "breakfast", "friends", "beach", "Beach", "lunch", "Lunch", "dinner", "outside", "hike", "anti-mask"])
