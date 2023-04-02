import logging
from flask import Flask

from flask import request
import sys
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException, InvalidAppIdException
from wechatpy import parse_message
from wechatpy.replies import create_reply
from wechatpy.replies import TextReply
from wechatpy import WeChatClient

from threading import Thread

client = WeChatClient('wxe1ce7221aa9b8225', '7eb79a6a232ebeab03fa840b74f1513f')
app = Flask(__name__)
app.debug = True
handler = logging.StreamHandler()
app.logger.addHandler(handler)

wechatToken = "peterli2015"

def asyncTask(userId, content):
    response = "hello world"
    print("ask a quesion with userId:{}, content:{}".format(userId, content))
    print("chat-GLB replay:{}".format(response))
    client.message.send_text(userId, response)


@app.route('/wechat', methods=['GET', 'POST'])
def wechat():
    timestamp = request.args.get("timestamp")
    nonce = request.args.get("nonce")
    if request.method == 'GET':
        # token, signature, timestamp, nonce
        echostr = request.args.get("echostr")
        signature = request.args.get("signature")
        if echostr:
            print("request timestamp:{},nonce:{}, echostr:{}, signature:{}".format(timestamp, 
                         nonce, echostr, signature))
            try:
                check_signature(wechatToken, signature, timestamp, nonce)
                return echostr
            except InvalidSignatureException:
                print("invalid message from request")
    else:
        xml = request.data
        if xml:
            try:
                msg = parse_message(xml)
                print("message from wechat msg:{}".format(msg))

                t1 = Thread(target=asyncTask, args=(msg.source, msg.content))
                t1.start()
                
                return "success"
            except (InvalidAppIdException, InvalidSignatureException):
                print("cannot decrypt message!")
        else:
            print("no xml body, invalid request!")
    return ""
if __name__ == '__main__':
    print('starting wechat of chatGLM')
    print('completed to load chatGLM')
    app.run(host='127.0.0.1', port=6006, debug=True)
    
