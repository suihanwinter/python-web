from flask import Flask,request,url_for, jsonify
import pymysql
from flask_cors import *
import pandas as pd
from collections import Counter

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app, supports_credentials=True)

from flask.json import JSONEncoder as _JSONEncoder

class JSONEncoder(_JSONEncoder):
    def default(self, o):
        import decimal
        if isinstance(o, decimal.Decimal):

            return float(o)

        super(JSONEncoder, self).default(o)
app.json_encoder = JSONEncoder

@app.route('/page1',methods=['GET'])
def page1():
    if(len(request.args)!=0):
        data_year = request.args['year']
        data_month = request.args['month']
        sql = "SELECT SUM(box_office) from films where type LIKE '%喜剧%' and `year` = "+ data_year + " and `month` = " + data_month +\
              " UNION SELECT SUM(box_office) from films where type LIKE '%冒险%' and `year` = " + data_year + " and `month` = " + data_month +\
              " UNION SELECT SUM(box_office) from films where type LIKE '%传记%' and `year` = "+data_year+ " and `month` = " + data_month +\
              " UNION SELECT SUM(box_office) from films where type LIKE '%剧情%' and `year` = "+data_year+ " and `month` = " + data_month +\
              " UNION SELECT SUM(box_office) from films where type LIKE '%战争%' and `year` = "+data_year+ " and `month` = " + data_month +\
              " UNION SELECT SUM(box_office) from films where type LIKE '%奇幻%' and `year` = "+data_year+ " and `month` = " + data_month +\
              " UNION SELECT SUM(box_office) from films where type LIKE '%家庭%' and `year` = "+data_year+ " and `month` = " + data_month +\
              " UNION SELECT SUM(box_office) from films where type LIKE '%历史%' and `year` = "+data_year+ " and `month` = " + data_month +\
              " UNION SELECT SUM(box_office) from films where type LIKE '%科幻%' and `year` = "+data_year+ " and `month` = " + data_month +\
              " UNION SELECT SUM(box_office) from films where type LIKE '%惊悚%' and `year` = "+data_year+ " and `month` = " + data_month +\
              " UNION SELECT SUM(box_office) from films where type LIKE '%悬疑%' and `year` = "+data_year+ " and `month` = " + data_month +\
              " UNION SELECT SUM(box_office) from films where type LIKE '%爱情%' and `year` = "+data_year+ " and `month` = " + data_month +\
              " UNION SELECT SUM(box_office) from films where type LIKE '%犯罪%' and `year` = "+data_year+ " and `month` = " + data_month +\
              " UNION SELECT SUM(box_office) from films where type LIKE '%动画%' and `year` = "+data_year+ " and `month` = " + data_month +\
              " UNION SELECT SUM(box_office) from films where type LIKE '%运动%' and `year` = "+data_year+ " and `month` = " + data_month +\
              " UNION SELECT SUM(box_office) from films where type LIKE '%恐怖%' and `year` = "+data_year+ " and `month` = " + data_month +\
              " UNION SELECT SUM(box_office) from films where type LIKE '%纪录片%' and `year` = "+data_year+ " and `month` = " + data_month +\
              " UNION SELECT SUM(box_office) from films where type LIKE '%动作%' and `year` = "+data_year+ " and `month` = " + data_month
    else:
        sql = "SELECT SUM(box_office) from films where type LIKE '%喜剧%' " \
              "UNION SELECT SUM(box_office) from films where type LIKE '%冒险%'" \
              " UNION SELECT SUM(box_office) from films where type LIKE '%传记%'" \
              "UNION SELECT SUM(box_office) from films where type LIKE '%剧情%'" \
              " UNION SELECT SUM(box_office) from films where type LIKE '%战争%'" \
              "UNION SELECT SUM(box_office) from films where type LIKE '%奇幻%'" \
              " UNION SELECT SUM(box_office) from films where type LIKE '%家庭%'" \
              "UNION SELECT SUM(box_office) from films where type LIKE '%历史%'" \
              " UNION SELECT SUM(box_office) from films where type LIKE '%科幻%'" \
              "UNION SELECT SUM(box_office) from films where type LIKE '%惊悚%'" \
              " UNION SELECT SUM(box_office) from films where type LIKE '%悬疑%'" \
              "UNION SELECT SUM(box_office) from films where type LIKE '%爱情%'" \
              " UNION SELECT SUM(box_office) from films where type LIKE '%犯罪%'" \
              "UNION SELECT SUM(box_office) from films where type LIKE '%动画%'" \
              " UNION SELECT SUM(box_office) from films where type LIKE '%运动%'" \
              "UNION SELECT SUM(box_office) from films where type LIKE '%恐怖%'" \
              " UNION SELECT SUM(box_office) from films where type LIKE '%纪录片%'" \
              " UNION SELECT SUM(box_office) from films where type LIKE '%动作%'"
    conn = pymysql.connect(host='localhost', user='root', password='120650', port=3306, db='maoyan',
                           charset='utf8mb4')


    cursor = conn.cursor()
    cursor.execute(sql)
    values = cursor.fetchall()
    jsondata = {}
    xd = []
    yd = ['喜剧','冒险','传记','剧情','战争','奇幻','家庭','历史','科幻',
          '惊悚','悬疑','爱情','犯罪','动画','运动','恐怖','纪录片','动作']
    datas = []
    for index,i in enumerate(values):
        mydict = {}
        mydict["value"] = i[0]
        mydict["name"] = yd[index]
        datas.append(mydict)
        xd.append(i[0])
    jsondata['categories'] = yd
    jsondata['data'] = xd
    jsondata['datas'] = datas
    j = jsonify(jsondata)
    cursor.close()
    conn.close()
    return j

@app.route('/page2',methods=['GET'])
def page2():
    if(len(request.args)!=0):
        data_year = request.args['year']
        data_top = request.args['top']
        sql = "SELECT `name`,box_office from films WHERE `year` = "+data_year+" ORDER BY box_office DESC LIMIT 0," +data_top
    else:
        sql = "SELECT `name`,box_office from films ORDER BY box_office DESC LIMIT 0,20"
    conn = pymysql.connect(host='localhost', user='root', password='120650', port=3306, db='maoyan',
                           charset='utf8mb4')

    cursor = conn.cursor()
    cursor.execute(sql)
    values = cursor.fetchall()
    jsondata = {}
    datas = []
    for index,i in enumerate(values):
        mydict = {}
        mydict["value"] = i[1]
        mydict["name"] = i[0]
        datas.append(mydict)
    jsondata['datas'] = datas
    j = jsonify(jsondata)
    cursor.close()
    conn.close()
    return j

@app.route('/page3',methods=['GET'])
def page3():
    if(len(request.args)!=0):
        data_type = request.args['type']
        sql = "SELECT SUM(box_office) from films where `year` = 2015 and `type` LIKE '%" + data_type + "%' " \
              " UNION SELECT SUM(box_office) from films where `year` = 2016 and `type` LIKE '%" + data_type + "%' " \
              " UNION SELECT SUM(box_office) from films where `year` = 2017 and `type` LIKE '%" + data_type + "%' " \
              " UNION SELECT SUM(box_office) from films where `year` = 2018 and `type` LIKE '%" + data_type + "%' " \
              " UNION SELECT SUM(box_office) from films where `year` = 2019 and `type` LIKE '%" + data_type + "%' "
    else:
        sql = "SELECT SUM(box_office) from films where `year` = 2015" \
              " UNION SELECT SUM(box_office) from films where `year` = 2016" \
              " UNION SELECT SUM(box_office) from films where `year` = 2017" \
              " UNION SELECT SUM(box_office) from films where `year` = 2018" \
              " UNION SELECT SUM(box_office) from films where `year` = 2019"
    conn = pymysql.connect(host='localhost', user='root', password='120650', port=3306, db='maoyan',
                           charset='utf8mb4')

    cursor = conn.cursor()
    cursor.execute(sql)
    values = cursor.fetchall()
    jsondata = {}
    xd = []
    for index,i in enumerate(values):
        xd.append(i[0])
    jsondata['data'] = xd
    j = jsonify(jsondata)
    cursor.close()
    conn.close()
    return j


@app.route('/page4',methods=['GET'])
def page4():
    data_year = ''
    if(len(request.args)!=0):
        data_year = request.args['year']
        data_top = int(request.args['top'])
    else:
        data_top = 10
    sql = "select year,actor1,actor2,actor3,actor4 from films"
    conn = pymysql.connect(host='localhost', user='root', password='120650', port=3306, db='maoyan',
                           charset='utf8mb4')
    db_0 = pd.read_sql(sql, conn)
    if(len(data_year)!=0):
        db = db_0[(db_0.year == int(data_year))]
    else:
        db = db_0
    dict_ = dict(Counter(db['actor1'].append(db['actor2']).append(db['actor3']).append(db['actor4']).dropna()).most_common(data_top))
    x = list(dict_.keys())
    y = list(dict_.values())
    datas = []
    for index in range(len(x)):
        mydict = {}
        mydict["value"] = y[index]
        mydict["name"] = x[index]
        datas.append(mydict)
    jsondata = {}
    jsondata['data'] = datas
    jsondata['name'] = x
    jsondata['value'] = y
    j = jsonify(jsondata)
    return j

@app.route('/data',methods=['GET'])
def data():
    limit = int(request.args['limit'])
    page = int(request.args['page'])
    page = (page-1)*limit
    conn = pymysql.connect(host='localhost', user='root', password='120650', port=3306, db='maoyan',
                           charset='utf8mb4')

    cursor = conn.cursor()
    cursor.execute("select count(*) from films");
    count = cursor.fetchall()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    cursor.execute("select * from films limit "+str(page)+","+str(limit));
    data_dict = []
    result = cursor.fetchall()
    for field in result:
        data_dict.append(field)
    table_result = {"code": 0, "msg": None, "count": count[0], "data": data_dict}
    cursor.close()
    conn.close()
    return jsonify(table_result)



@app.route('/addUser',methods=['POST'])
def addUser():
    get_json = request.get_json()
    name = get_json['name']
    password = get_json['password']
    conn = pymysql.connect(host='localhost', user='root', password='120650', port=3306, db='maoyan',
                           charset='utf8mb4')
    cursor = conn.cursor()
    sql = "insert into `userinfo` values('"+name+"','"+password+"')"
    cursor.execute(sql);
    conn.commit()
    table_result = {"code": 200, "msg": "成功"}
    cursor.close()
    conn.close()
    return jsonify(table_result)

@app.route('/loginByPassword',methods=['POST'])
def loginByPassword():
    get_json = request.get_json()
    name = get_json['name']
    password = get_json['password']
    conn = pymysql.connect(host='localhost', user='root', password='120650', port=3306, db='maoyan',
                           charset='utf8mb4')
    cursor = conn.cursor()
    cursor.execute("select count(*) from `userinfo` where `name` = '" + name +"' and password = '" + password+"'");
    count = cursor.fetchall()
    if(count[0][0] != 0):
        table_result = {"code": 200, "msg": "成功"}
    else:
        table_result = {"code": 500, "msg": "失败"}
    cursor.close()
    conn.close()
    return jsonify(table_result)
    
if __name__ == "__main__":
   app.run(port=5000)