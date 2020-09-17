# Mask-Bot 🤖
Mask Bot is a Twitter bot ([@maskPythonBot](https://twitter.com/maskPythonBot/with_replies)) used to reply to photographs posted of multiple people without masks. The bot filters through different tweets, looking for keywords related to people in groups (beach, lunch, etc), and uses a OpenCV/TensorFlow/Keras Computer Vision detection program to analyze the number of people with and without masks. If there are multiple people without masks, the bot will reply with the message "Put on a mask!"

## Twitter Filters
Due to rate-limiting on the Twitter API, the bot has a few restrictions in place so that it doesn't go overboard:
- The user must have at least 200 followers
- The user must be located in the US (where masks are apparently an issue for some people)

The bot currently only looks at Tweets with the following keywords:
- brunch
- breakfast
- beach
- lunch
- dinner
- outside
- hike
- anti-mask
- group
- party

## Creator
This bot was created by [Rohan Bhushan](https://www.linkedin.com/in/rohan-bhushan-a955b3194/)

## Credits
Adapts the Face Mask Detection Model by [Chandrika Deb](https://github.com/chandrikadeb7/Face-Mask-Detection)
