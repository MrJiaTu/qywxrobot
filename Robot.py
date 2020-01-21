#!/usr/bin/env python
#coding=utf-8
#根据场景方便做定时提醒和数据化播报
#作者 嘉图
#更改日志：支持文本消息和图片封装成类
import requests
import json
import hashlib
import base64

class WxTalk():
    """
     微信webhook消息发送
    """
    headers = {
        "Content-Type": "application/json"
    }
    req_message = {
        "errcode": 1,
        "errmessage": ""
    }
    def __init__(self, webhook):
        """
        :param webhook: webhook，只需要URL后面webhook=后面的值
        """
        self.webhook = webhook
    def sendmessage(self,user, message):
        """
        :param message: 发送的消息
        :return: errcode  1 正常，0失败
        """
        data = {
            ##"msgtype":"image"
            "msgtype": "text",
            "text": {
                "content": str(message)
            },
            "at": {
                "atMobiles": [
                    user
                ],
                "isAtAll": False
            }
        }
        post_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={0}".format(self.webhook)
        try:
            req = requests.post(post_url, data=json.dumps(data), headers=self.headers,timeout=10)
            if req.status_code == 200 and req.json()["errcode"] == 0:
                return self.req_message  # 发送成功
            else:
                self.req_message["errcode"] = 0
                self.req_message["errmessage"] = str(req.json())
                return self.req_message # 发送失败
        except Exception as e:
            self.req_message["errcode"] = 0
            self.req_message["errmessage"] = "请求微信企业失败，监测你的网络是否正常"
            return self.req_message  # 请求失败
    def sendImage(self, image_path):
        '''
        :param url:   传入企业微信机器人webhoot
        :param image_path:  本地图片路径
        :return:
        '''
        with open(image_path, "br") as f:
            fcont = f.read()
            # 转化图片的base64
            ls_f = base64.b64encode(fcont)
            # 计算图片的md5
            fmd5 = hashlib.md5(fcont)
        data = {"msgtype": "image", "image": {"base64": ls_f.decode('utf8'), "md5": fmd5.hexdigest()}}
        ##data_json = json.dumps(data)
        ##print('推送的json%s' % data_json)
        ##prequte = requests.post(url, data=data_json)
        ##return prequte.text
        post_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={0}".format(self.webhook)
        try:
            req = requests.post(post_url, data=json.dumps(data), headers=self.headers,timeout=10)
            if req.status_code == 200 and req.json()["errcode"] == 0:
                return self.req_message  # 发送成功
            else:
                self.req_message["errcode"] = 0
                self.req_message["errmessage"] = str(req.json())
                return self.req_message # 发送失败
        except Exception as e:
            self.req_message["errcode"] = 0
            self.req_message["errmessage"] = "请求微信企业失败，监测你的网络是否正常"
            return self.req_message  # 请求失败
