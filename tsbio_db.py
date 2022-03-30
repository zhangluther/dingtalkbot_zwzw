import pymssql
from mysql_log import log

userName="user name"
pwd="password"
hosts="ip"
dbName="db name"

def get_all(sql):
    conn=pymssql.connect(hosts,userName,pwd,dbName,timeout=120)
    cur=conn.cursor(as_dict=True)
    cur.execute(sql)
    query_res=cur.fetchall()
    conn.close()
    return query_res

def execute(sql):
    conn = pymssql.connect(hosts, userName, pwd, dbName,timeout=120)
    cur = conn.cursor(as_dict=True)
    cur.execute(sql)
    conn.commit()
    conn.close()
    return True

#根据关键词查询化合物信息及库存
def get_compound_info_by_keyword(kwd:str):
    search_sql="""
SELECT TOP 10
    cas, 
    tsid, 
    en_name, 
    mf, 
    mw, 
    cn_name, 
    kucun
FROM
    compounds
    LEFT JOIN
    cas_kucun
    ON 
        compounds.compound_id = cas_kucun.compound_id
WHERE
    compound_id = '%s' OR
    ID = '%s' OR
    name_en = '%s' OR
    name_cn = '%s' 
    """ % (kwd,kwd,kwd,kwd)
    l_res=get_all(search_sql)
    return l_res