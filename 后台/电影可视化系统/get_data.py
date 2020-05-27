
import re
import time
import pymysql
import requests
from bs4 import BeautifulSoup
from hashlib import sha1
import random
import font
from lxml import etree

head = """
Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Accept-Encoding:gzip, deflate, br
Accept-Language:zh-CN,zh;q=0.8
Cache-Control:max-age=0
Connection:keep-alive
Host:maoyan.com
Upgrade-Insecure-Requests:1
Content-Type:application/x-www-form-urlencoded; charset=UTF-8
User-Agent:Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36
"""

def load(name,pwd):
    db = pymysql.connect(host='localhost',port=3306,user='root',passwd='120650',db='maoyan',charset='utf8')
# 接收用户输入
    res = name
    # 对密码加密
    # m = sha1()
    # s = m.update(pwd.encode("utf-8"))
    # print(s)
    pwd2=sha1(pwd.encode('utf-8')).hexdigest()
    # 根据用户名查询密码

    sql = 'select password from userinfo where name=%s'
    cursor = db.cursor()
    cursor.execute(sql,res)
    psw = cursor.fetchall()
    db.commit()
    cursor.close()
    db.close()
    if psw == ():
        return 0
    elif psw[0][0] == pwd2:
        return 1
    else:
        return 2

def str_to_dict(header):
    """
    构造请求头,可以在不同函数里构造不同的请求头
    """
    header_dict = {}
    header = header.split('\n')
    for h in header:
        h = h.strip()
        if h:
            k, v = h.split(':', 1)
            header_dict[k] = v.strip()
    return header_dict


def get_url():
    """
    获取电影详情页链接
    """
    for k in range(5):
        for i in range(0, 150, 30):
            time.sleep(10)
            url = 'https://maoyan.com/films?showType=3&sortId=3&yearId=' + str(k+14) + '&offset=' + str(i)
            host = 'Referer:https://maoyan.com/films?showType=3&yearId=10&sortId=3'
            header = head + host
            headers = str_to_dict(header)
            try:
                response = requests.get(url=url, headers=headers)
            except:
                continue
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            data_1 = soup.find_all('div', {'class': 'channel-detail movie-item-title'})
            data_2 = soup.find_all('div', {'class': 'channel-detail channel-detail-orange'})
            num = 0
            for item in data_1:
                num += 1
                time.sleep(random.random()*3)
                url_1 = item.select('a')[0]['href']
                if data_2[num-1].get_text() != '暂无评分':
                    print('********************',num,'start********************')
                    url = 'https://maoyan.com' + url_1
                    print(url)
                    for message in get_message(url):
                        print(message)
                        to_mysql(message)
                    print('********************',num,'end********************\n')
                else:
                    continue


def get_message(url):
    """
    获取电影详情页里的信息
    """
    time.sleep(10)
    data = {}
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-encoding': 'gzip',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
        'Refer' : 'https://maoyan.com/films?showType=3&sortId=3&yearId=2019&offset=1',
        'Cookie': '__mta=247316155.1581853653774.1582702289490.1582702374809.54; uuid_n_v=v1; uuid=1DF1110050B211EA89902D76E6C64D3F296D2156E1AF4B8CB0E6E6EE438CACCB; mojo-uuid=45d9f36068c74a6b609863a95a248613; _lxsdk_cuid=1704dd33adbc8-03de413d58b73e-51402e1a-144000-1704dd33adcc8; _lxsdk=1DF1110050B211EA89902D76E6C64D3F296D2156E1AF4B8CB0E6E6EE438CACCB; _csrf=a8c8cc6cb2a62e2a772facb576c15e6271cc633f3c2f1bb32106933bac3b23c8; mojo-session-id={"id":"7614e3978d73d253a208ef4679af2e48","time":1582701434185}; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1581916149,1581916163,1582259637,1582701434; __mta=247316155.1581853653774.1582701470506.1582701571282.50; mojo-trace-id=12; Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1582702375; _lxsdk_s=170805b5694-1c1-22-677%7C%7C22'
    }
    try:
        resp = requests.get(url=url, headers=header)
    except:
        return data
    resp = resp.text
    print(resp)
    #获取编码字典
    font_dict = font.getFont(resp)
    #替换页面中的编码
    for key in font_dict.keys():
        resp = resp.replace(key, font_dict[key])

    # 下面是额外内容：
    # 获取评分、票房等数据
    body = etree.HTML(resp)
    mark_info = body.xpath('//div[@class="movie-index"]/div')
    mark = mark_info[0].xpath('string(.)').replace(' ', '')
    mark = re.sub(r'\n+', '|', mark)[1:-1].split('|')
    if len(mark) < 2:
        myMark = ''
        myNum = ''
    else:
        myMark = mark[0]
        myNum = mark[1][:-3]
    boxOffice = mark_info[1].xpath('string(.)').replace(' ', '').replace('\n', '')
    print(myMark,myNum,boxOffice)
    # 获取电影信息
    soup = BeautifulSoup(resp, "html.parser")
    ell = soup.find_all('li', {'class': 'ellipsis'})
    name = soup.find_all('h1', {'class': 'name'})
    people = soup.find_all('a', {'class': 'name'})
    # 返回电影信息
    if name:
        data["name"] = name[0].get_text()
    data["time"] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    if ell:
        type = ell[0].get_text().strip().split('\n')
        if len(type)>0:
            data["type1"] = type[0]
        if len(type)>1:
            data["type2"] = type[1]
        if len(type)>2:
            data["type3"] = type[2]
        if len(type)>3:
            data["type4"] = type[3]
        if len(type) > 4:
            data["type5"] = type[4]
        if len(ell[1].get_text().split('/'))>0:
            data["country"] = ell[1].get_text().split('/')[0].replace('\n','').replace(' ','')
        if len(ell[1].get_text().split('/'))>1:
            data["length"] = ell[1].get_text().split('/')[1].replace('\n','').replace(' ','')
        try:
            if ell[2].get_text()[:10]:
                string = ell[2].get_text()[:10]
            if string.split('-')[0]:
                data['year'] = int(string.split('-')[0])
            if string.split('-')[0]:
                data['month'] = int(string.split('-')[1])
            if string.split('-')[2]:
                data['day'] = int(string.split('-')[2])
        except:
            pass
    if people:
        data['director'] = people[0].get_text().replace('\n', '').replace(' ','')
        if len(people) > 2:
            data['actor1'] = people[1].get_text().replace('\n', '').replace(' ','')
        if len(people) > 3:
            data['actor2'] = people[2].get_text().replace('\n', '').replace(' ','')
        if len(people) > 4:
            data['actor3'] = people[3].get_text().replace('\n', '').replace(' ','')
        if len(people) > 5:
            data['actor4'] = people[4].get_text().replace('\n', '').replace(' ','')
    # 因为会出现没有票房的电影,所以这里需要判断
    data["score"] = myMark
    boxOffice = boxOffice.replace('美元','')
    if '万' in myNum:
        data["people"] = int(float(myNum.replace('万', '')) * 10000)
    elif len(myNum) ==0:
        data["people"] = 0
    else:
        data["people"] = int(float(myNum))
    if '万' in boxOffice:
        data["box_office"] = int(float(boxOffice.replace('万', '')) * 10000)
    elif '暂无' in boxOffice:
        data["box_office"] = 0
    elif '亿' in boxOffice:
        data["box_office"] = int(float(boxOffice.replace('亿', '')) * 100000000)
    else:
        data["box_office"] = int(float(boxOffice))
    yield data


def to_mysql(data):
    """
    信息写入mysql
    """
    table = 'films'
    keys = ', '.join(data.keys())
    values = ', '.join(['%s'] * len(data))
    db = pymysql.connect(host='localhost', user='root', password='120650', port=3306, db='maoyan')
    cursor = db.cursor()
    sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=table, keys=keys, values=values)
    try:
        if cursor.execute(sql, tuple(data.values())):
            print("Successful")
            db.commit()
    except:
        print('Failed')
        db.rollback()
    db.close()


def main():
    get_url()


if __name__ == '__main__':
    main()
