import numpy as np

from flask import Flask, request, abort

from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage, ImageMessage, ImageSendMessage)

#from keras.models import load_model
#from keras.preprocessing import image

# TensorFlow cpu == 2.3.1
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
#model = load_model("resnet50_imagenet.h5")
model = load_model('ResNet_32.h5')

import pandas as pd
import os

#import json
#json_open = open("imagenet_class_index.json", 'r')
#imagenet_classnames = json.load(json_open)

app = Flask(__name__)

ACCESS_TOKEN = "VzJxMa7DiVPzf3Z1y9+4OOIDBmRzhCdE3DHy/rkjGoSjoYhujyNxYLPOlji+uBgPZlcoGGv6RoTlZJ/IcJKGg2dAQV9AKIBAOM4RfGFxFHFq7g/IgS3WbMUCZz+/gv1IiZNhOTIHuJMpVquPWEv6NQdB04t89/1O/w1cDnyilFU="
SECRET = "4b4400f6e9a2fe31bb19fb5525b73d58"

#FQDN = "https://cats-vs-dogs-line-bot-naoya.herokuapp.com/callback"
FQDN = "https://udon-ai-bot.herokuapp.com/callback"

line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Requestbody: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

if __name__ == "__main__":
    app.run()
