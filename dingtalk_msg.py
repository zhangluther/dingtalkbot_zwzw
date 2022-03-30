import requests
import time
import dingtalkOuth
import json

#钉钉群消息
def text_to_group(content):
    url = 'https://oapi.dingtalk.com/robot/send?access_token=access_token'
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    content = '\n' + now +"\n" + content
    msg = '''{"msgtype": "text",  
                "text": {
                     "content": "new_web_doc: %s"
                }
                    }''' % ( content)
    msg = msg.encode('utf-8')
    header = {"Content-Type": "application/json"}
    msg_send = requests.post(url, data=msg, headers=header)
    return (msg_send.text)

#工作通知
def dingWorkMsgText(appName,l_userid,msg):
    s_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    msgContent='''{
        "msgtype": "text",
        "text": {
            "content": "'''+s_time+'''  '''+msg+'''"
        }
    }'''
    j_appInfo=dingtalkOuth.app_info
    access_token=dingtalkOuth.get_access_token(appName)
    agentId=j_appInfo[appName]['agent_id']
    userIds=','.join(l_userid)
    url='https://oapi.dingtalk.com/topapi/message/corpconversation/asyncsend_v2'
    params={'access_token':access_token,'agent_id':agentId,'userid_list':userIds,'msg':msgContent}
    msgSend=requests.post(url,params)
    sendResult=msgSend.json()
    return sendResult
