import pymysql
import json
import hashlib

hosts="ip"
user="root"
pwd="password"
db_name="log"

def log(action,web_hosts,client="NA",detail=None):
    db=pymysql.connect(user=user,password=pwd,host=hosts,database=db_name)
    cursor=db.cursor()
    action=action.replace("'",'"')
    web_hosts=web_hosts.replace("'",'"')
    if detail:
        detail = detail.replace("'", '"')
        sql="""INSERT INTO webdoc(hosts,action,detail,client) VALUES ('%s','%s','%s','%s')""" % (web_hosts,action,detail,client)
    else:
        sql="""INSERT INTO webdoc(hosts,action,client) VALUES ('%s','%s','%s')""" % (web_hosts,action,client)

    cursor.execute(sql)
    db.commit()
    db.close()
    print("mysql log success")

def request_log(webhost,request):
    headers=request.headers
    url=request.url
    client_ip = request.client.host
    s_detail="URL: %s, %s" % (url,str(headers))
    log("web_request",webhost,client_ip,s_detail)