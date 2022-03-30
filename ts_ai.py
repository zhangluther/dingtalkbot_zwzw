import json
import dingtalk_msg
import time
import re
import tsbio_db

def chat(req):

    content = req

    #json解析
    content_json=content
    sender_name=content_json.senderNick
    sessionWebhook=content_json.sessionWebhook
    msgId=content_json.msgId
    expire_ts=content_json.sessionWebhookExpiredTime
    createat_ts=content_json.createAt
    conversation_type = '单聊' if content_json.conversationType=='1' else '群聊'
    text=content_json.text.content
    contents = (sender_name, sessionWebhook, msgId, conversation_type, text)
    dingtalk_msg.text_to_group(str(req.json()).replace('"','').replace("'",""))
    res=query_router(text)
    return res

#意图判断_查询
def query_router(text):
    value=text.strip()
    value=value[:30]
    l_res=tsbio_db.get_compound_info_by_keyword(value)
    print("!!!LRES!!! ",l_res)
    res=product_stringfy(text,l_res)
    return res

#product类回答解析
def product_stringfy(text,l_j_products):

    btns = [{}, {}]
    btns[0]['title'] = '查询网站1'
    btns[1]['title'] = '查询网站2'
    btns[0]['actionURL'] = 'https://www.xxx.com/search?keyword=' + text
    btns[1]['actionURL'] = 'https://www.xxx.com/search?keyword=' + text

    if not l_j_products:
        title = '没有找到相关产品'
        content_md = '没找到与之相关的产品, 可点下面的**按钮**搜索在网站搜索'
    else:
        title='找到%s个可能的结果' % len(l_j_products)
        content_md=''
        for j_info in l_j_products:
            tsid=j_info["tsid"]
            cas=j_info["cas"]
            en_name=j_info["en_name"] if j_info["en_name"] else "unknown"
            cn_name=j_info["cn_name"] if j_info["cn_name"] else "unknown"
            kucun=j_info["kucun"] if j_info["kucun"] else 0
            content_md+='# %s/%s \n' % (tsid,cas)
            content_md+='**Name:** %s\n\n' % en_name
            content_md+='**名称:** %s\n\n' % cn_name
            content_md+='**库存:** %s\n\n' % kucun
    res=common_template(title,content_md,btns)
    return res

# json模板
def common_template(title,text,btns):

    template_common = {"msgtype": "actionCard"}
    action_card = {"hideAvatar": "0", "btnOrientation": "0"}

    action_card['title'] = title
    action_card['text'] = text
    action_card['btns'] = btns
    template_common['actionCard'] = action_card

    result = template_common
    return result