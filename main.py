# -*- coding: utf-8 -*-
import json
import requests

#账户
EMAIL = '2941325451@qq.com'
PASSWORD = 'gpcsw555'
DOMAIN = 'https://ikuuu.co'


# 企业微信配置
QYWX_CORPID = "ww332b9c0ef46cc2f0"
QYWX_AGENTID = "1000003"
QYWX_CORPSECRET = "P4I9rz3_U8B1LYwT94VXWc7W_5q4i-Cxhf9kR5DZqHY"
QYWX_TOUSER = "gengpengcheng"
QYWX_MEDIA_ID = ""

class SSPANEL:
    name = "SSPANEL"

    def __init__(self, check_item):
        self.check_item = check_item
        self.qywx_corpid = QYWX_CORPID
        self.qywx_agentid = QYWX_AGENTID
        self.qywx_corpsecret = QYWX_CORPSECRET
        self.qywx_touser = QYWX_TOUSER
        self.qywx_media_id = QYWX_MEDIA_ID

    def message2qywxapp(self, qywx_corpid, qywx_agentid, qywx_corpsecret, qywx_touser, qywx_media_id, content):
        print("企业微信应用消息推送开始")
        res = requests.get(
            f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={qywx_corpid}&corpsecret={qywx_corpsecret}"
        )
        token = res.json().get("access_token", False)
        if qywx_media_id:
            data = {
                "touser": qywx_touser,
                "msgtype": "mpnews",
                "agentid": int(qywx_agentid),
                "mpnews": {
                    "articles": [
                        {
                            "title": "ikuuu 签到通知",
                            "thumb_media_id": qywx_media_id,
                            "content_source_url": "https://ikuuu.co/",
                            "content": content.replace("\n", "<br>"),
                            "digest": content,
                        }
                    ]
                },
            }
        else:
            data = {
                "touser": qywx_touser,
                "agentid": int(qywx_agentid),
                "msgtype": "textcard",
                "textcard": {
                    "title": "ikuuu 签到通知",
                    "description": content,
                    "url": "https://ikuuu.co/",
                },
            }
        result = requests.post(url=f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={token}",
                               data=json.dumps(data))
        # print(result)
        return

    def sign(self, email, password, url):
        email = email.replace("@", "%40")
        try:
            session = requests.session()
            session.get(url=url, verify=False)
            login_url = url + "/auth/login"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            }
            post_data = "email=" + email + "&passwd=" + password + "&code="
            post_data = post_data.encode()
            session.post(login_url, post_data, headers=headers, verify=False)
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
                "Referer": url + "/user",
            }
            response = session.post(url + "/user/checkin", headers=headers, verify=False)
            msg = response.json().get("msg")
        except Exception as e:
            msg = "签到失败"
        return msg

    def main(self):
        email = self.check_item.get("email")
        password = self.check_item.get("password")
        url = self.check_item.get("url")
        qywx_corpid = self.qywx_corpid
        qywx_agentid = self.qywx_agentid
        qywx_corpsecret = self.qywx_corpsecret
        qywx_touser = self.qywx_touser
        qywx_media_id = self.qywx_media_id
        sign_msg = self.sign(email=email, password=password, url=url)
        msg = [
            {"name": "帐号信息", "value": email},
            {"name": "签到信息", "value": f"{sign_msg}"},
        ]
        msg = "\n".join([f"{one.get('name')}: {one.get('value')}" for one in msg])
        self.message2qywxapp(qywx_corpid=qywx_corpid, qywx_agentid=qywx_agentid, qywx_corpsecret=qywx_corpsecret,
                             qywx_touser=qywx_touser, qywx_media_id=qywx_media_id, content=msg)
        return msg



if __name__ == "__main__":
    _check_item = {'email': EMAIL, 'password': PASSWORD, 'url': DOMAIN}
    SSPANEL(check_item=_check_item).main()
