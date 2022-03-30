from fastapi import FastAPI,Request
from fastapi.responses import HTMLResponse,RedirectResponse,PlainTextResponse
import time
from mysql_log import log,request_log
import tsbio_db
import json
import requests
import dingtalk_msg
import ts_ai

hostname=socket.gethostname()

app=FastAPI()
app.mount("/static",StaticFiles(directory="static"),name="static")
log("web_server_start",hostname)


class dingbot_query_text(BaseModel):
    content:str
class dingbot(BaseModel):
    conversationId:str
    chatbotCorpId:str
    chatbotUserId:str
    msgId:str
    senderNick:str
    isAdmin:str
    senderStaffId:str
    sessionWebhookExpiredTime:str
    createAt:str
    senderCorpId:str
    conversationType:str
    senderId:str
    sessionWebhook:str
    msgtype:st
    text:dingbot_query_text

@app.post('/dingrobot')
@app.get('/dingrobot')
def ding_robot(request:Request,o_query:dingbot):
    request_log(hostname, request)
    print("请求信息: ",o_query.json())
    res=ts_ai.chat(o_query)
    return res
