import requests
import json
import time
from hashlib import sha256
import base64
import hmac
from urllib import parse
import os

app_info={
    "app1":{
        "agent_id":"agent_id",
        "app_key":"app key",
        "app_secret":"app secret"
    }
}

def get_access_token(app="app1"):
    uri="info/"+app
    now_sec=int(time.time())
    with open(uri,"r",encoding="utf8") as f:
        j_token=json.loads(f.read())
    if now_sec-j_token["time"]>7000:
        print(app," token已过期")
        token=renew_access_token(app)
        j_token["token"]=token
        j_token["time"]=now_sec
        with open(uri, "w", encoding="utf8") as f:
            f.write(json.dumps(j_token))
            print(app," token已重新写入")
    token=j_token["token"]
    return token

def renew_access_token(app="app1"):
    app_key = app_info[app]["app_key"]
    app_secret = app_info[app]["app_secret"]
    url="https://oapi.dingtalk.com/gettoken?appkey=%s&appsecret=%s" % (app_key,app_secret)
    token_info=json.loads(requests.get(url).text)
    print(token_info)
    token=token_info["access_token"]
    return token

def get_userinfo_bytmpcode(tmp_code,app="app1",detail=True):
    app_key=app_info[app]["app_key"]
    app_secret=app_info[app]["app_secret"]
    time_stamp=int(time.time())*1000
    info=str(time_stamp)
    appsecret_encode = app_secret.encode('utf-8')
    data = info.encode('utf-8')
    signature = base64.b64encode(hmac.new(appsecret_encode, data, digestmod=sha256).digest())
    signature_urlencode=parse.quote(signature)
    url="https://oapi.dingtalk.com/sns/getuserinfo_bycode?accessKey=%s&timestamp=%s&signature=%s" % (app_key,info,signature_urlencode)
    payload='{"tmp_auth_code":"%s"}' % tmp_code
    user_info=requests.post(url,data=payload).text
    j_user_info=json.loads(user_info)["user_info"]
    if not detail:
        return j_user_info
    unionid=j_user_info["unionid"]
    access_token=get_access_token(app)
    userid=get_userid_by_unionid(unionid,app,access_token)
    j_user_info_detail=get_user_info_by_userid(userid,app,access_token)
    return j_user_info_detail

def get_userid_by_unionid(unionid,app="app1",access_token:str=None):
    if not access_token:
        access_token=get_access_token(app)
    url="https://oapi.dingtalk.com/topapi/user/getbyunionid?access_token=%s" % access_token
    payload='{"unionid":"%s"}' % unionid
    user_id_info = requests.post(url, data=payload).text
    j_user_info = json.loads(user_id_info)
    userid=j_user_info["result"]["userid"]
    return userid

def get_user_info_by_userid(userid:str,app="app1",access_token:str=None):
    if not access_token:
        access_token=get_access_token(app)
    url="https://oapi.dingtalk.com/topapi/v2/user/get?access_token=%s" % access_token
    payload='{"userid":"%s"}' % userid
    q_user_info = requests.post(url, data=payload).text
    user_info=json.loads(q_user_info)
    # j_user_info={}
    if user_info["errcode"]==0:
        j_user_info = user_info["result"]
        j_user_info["available"]=True
        with open("info/dingusers/" + userid, "w", encoding="utf8") as f:
            f.write(json.dumps(j_user_info).encode('latin-1').decode('unicode_escape'))
    elif user_info["errcode"]==60121:  #未找到用户, 可能是已离职
        if os.path.isfile("info/dingusers/"+userid):
            with open("info/dingusers/"+userid,"r",encoding="utf8") as f:
                j_user_info=json.loads(f.read().replace('"{','{').replace('}"','}'))
            j_user_info["available"]=False
            with open("info/dingusers/" + userid, "w", encoding="utf8") as f:
                f.write(json.dumps(j_user_info).encode('latin-1').decode('unicode_escape'))
                print("info/dingusers/" + userid + "已更新")
    return j_user_info
