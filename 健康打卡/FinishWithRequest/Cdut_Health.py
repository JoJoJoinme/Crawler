import datetime
import requests
import random
import math
import time
import json
import sys
import re
import os
from six.moves.urllib.parse import urlencode
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
from base64 import b64encode
from lxml.etree import HTMLParser
from lxml import etree



flowId = '4af305b270435b4801704c0c9eba007d'
formId = '4af305b270435b4801704c0c9e250054'

cur_path = os.path.dirname(os.path.abspath(__file__))
print("Cur path:", cur_path)
os.chdir(cur_path)  # 切换至当前路径
sys.path.append(cur_path)
from Message import CdutEmail, ft
from Cdut_logger import logger


with open('{}/data/instJson.json'.format(cur_path), 'r+', encoding='utf-8') as f:
    instJson = json.load(f)

with open('{}/data/formVerJson.json'.format(cur_path), 'r+', encoding='utf-8') as f:
    formVerJson = json.load(f)

with open('{}/data/flowVerJson.json5'.format(cur_path), 'r+', encoding='utf-8') as f:
    flowVerJson = json.load(f)

with open('{}/data/flowJson.json5'.format(cur_path), 'r+', encoding='utf-8') as f:
    flowJson = json.load(f)[0]

with open('{}/data/formJson.json'.format(cur_path), 'r+', encoding='utf-8') as f:
    formJson = json.load(f)[0]


# 按登录界面方式的随机数生成
def _rds(num):
    random_str = ''
    random_chars = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678'
    for i in range(num):
        random_str += random_chars[math.floor(random.random() * len(random_chars))]
    return random_str


# 密码加密函数
def encryptAES(data, key, iv):
    _data = str.encode(data)
    _key = str.encode(key)
    _iv = str.encode(iv)
    cipher = AES.new(_key, AES.MODE_CBC, _iv)
    ct = cipher.encrypt(pad(_data, 16))
    return b64encode(ct).decode('utf-8')


# 清洗JSON数据，整理成我们需要提交的数据
def formatter_json(former_formJson, former_formJson_template):
    _formJson = former_formJson
    _formJson_template = former_formJson_template
    keys = _formJson.keys()
    template_keys = _formJson_template.keys()
    dic = {}
    for key in keys:
        if key in template_keys:
            keyDM = key + 'DM'
            if keyDM in template_keys:
                if '@#@' in str(_formJson_template[keyDM]):
                    dic[key] = _formJson_template[keyDM]
                else:
                    if not _formJson_template[keyDM]:
                        dic[key] = ''
                    else:
                        dic[key] = str(_formJson_template[keyDM]) + '@#@' + str(_formJson_template[key])
            else:
                if _formJson_template[key]:
                    dic[key] = _formJson_template[key]
                else:
                    dic[key] = ""
    item = {
        '是': '1@#@是',
        '否': '2@#@否'
    }
    dic['TBRQ'] = datetime.datetime.now().strftime("%Y-%m-%d")
    dic['ZZMM'] = dic['ZZMM'] + '@#@' + dic['ZZMM']
    dic['XQGL'] = item[dic['XQGL']]
    dic['BQZ'] = item[dic['BQZ']]
    dic['SFQR'] = formJson['SFQR']
    dic['XH1'] = dic['XH']
    dic['formId'] = formJson['formId']
    dic['id'] = formJson['id']
    return dic


# 将密码用AES加密后登录网站
def login(session, response, username, passwd, url, headers):
    logger.info("开始尝试登录")
    s = session
    root = etree.HTML(response.text, HTMLParser())
    pwdDefaultEncryptSalt = root.xpath('//*[@id="pwdDefaultEncryptSalt"]/@value')[0]
    lt = root.xpath('//*[@id="casLoginForm"]/div/input[1]/@value')[0]
    dllt = root.xpath('//*[@id="casLoginForm"]/div/input[2]/@value')[0]
    execution = root.xpath('//*[@id="casLoginForm"]/div/input[3]/@value')[0]
    _evenetId = root.xpath('//*[@id="casLoginForm"]/div/input[4]/@value')[0]
    rmShown = root.xpath('//*[@id="casLoginForm"]/div/input[5]/@value')[0]
    data = _rds(64) + passwd
    key = pwdDefaultEncryptSalt
    iv = _rds(16)
    pwdEncryptSalt = encryptAES(data, key, iv)
    payload = {
        'username': username,
        'password': pwdEncryptSalt,
        'lt': lt,
        'dllt': dllt,
        'execution': execution,
        '_eventId': _evenetId,
        'rmShown': rmShown
    }
    payload = urlencode(payload)
    s.post(url, headers=headers, data=payload)


# post点击学生健康打卡的请求
def send_click_health(session):
    s = session
    health_url = "https://ehall.cdut.edu.cn/jsonp/sendRecUseApp.json"  # 发送点击请求的页面
    cur_time = int(time.time() * 1000)
    health_param = {
        'appId': 5815636435722423,
        '_': cur_time
    }
    s.get(url=health_url, params=urlencode(health_param))


# 来到学生打卡的主界面
def login_health_main_page(session):
    s = session
    health_main_page = 'http://s.cdut.edu.cn/EIP/tabPage.jsp?'  # 点击后的主页
    health_main_params = {
        'url': '/nonlogin/elobby/service/start.htm?sid =zqwipkbcfkhnrrcnerpex3r72jydyaej',
        'title': '学生健康情况登记',
        't_s': int(time.time() * 1000),
        'amp_sec_version': 1,
        'gid': 'VHNSdDZWUHNvcW5NUko0RG9XN0g5R0NGbVlqVFZPNXZ2SzhFVXNiRkdWQy9tSWkwNkMyaEFVWllKMURZQnZlTVY4Ymw1NTFYNHlMSXMxdnR0bU95L1E9PQ',
        'EMAP_LANG': 'zh',
        'THEME': 'indigo'
    }
    s.get(url=health_main_page, params=health_main_params)


# 测试登录打卡页面是否成功
def test_login(session):
    s = session
    test_login_url = 'http://s.cdut.edu.cn:80/EIP/nonlogin/login/isLogin.htm'
    s.post(test_login_url, params=None)
    find_name_url = 'http://s.cdut.edu.cn/EIP/nonlogin/anonymous/queryisAnonymous.htm'
    find_name_response = s.post(find_name_url)
    name = find_name_response.text
    if not name:
        logger.error("登录失败，尝试重新登陆")
    else:
        logger.info("登录成功！")
        logger.info("您的姓名是：%s" % name)
        print("您的姓名是：%s" % name)
    return name


# 得到用于区分身份的uuid
def get_uuid(session):
    s = session
    cooperative_url = 'http://s.cdut.edu.cn/EIP/cooperative/openCooperative.htm?flowId={}'
    cooperative_flowId = '4af305b2702997ca017029f040db0002'
    response_cooperate = s.get(cooperative_url.format(cooperative_flowId))  # 提取UUID, template
    try:
        uuid = re.findall('var uuid = (.*);', response_cooperate.text)[0]
    except Exception as e:
        logger.error("获取uuid失败，错误信息如下", e)
        return
    return uuid


# 得到用于区分事务的node_id
def get_node_id(session, node_headers):
    s = session
    parseDataSource_url = 'http://s.cdut.edu.cn/EIP/flowcfg/synergy_form/parseDataSource.htm'
    parse_payload = {
        'flowId': '4af305b270435b4801704c0c9eba007d'
    }
    parse_payload = urlencode(parse_payload)
    parse_response = s.get(parseDataSource_url, data=parse_payload)
    parse_json = json.loads(parse_response.text)  # 该json字段包含个人学号信息等，需要提取获取进一步数据
    node_id_url = 'http://s.cdut.edu.cn/EIP/flowNode/createNodeIdByNum.htm'
    node_id_url_payload = {
        'num': 1
    }
    response_node_id = s.post(url=node_id_url, headers=node_headers, data=urlencode(node_id_url_payload))
    try:
        node_id = json.loads(response_node_id.text)[0]
        logger.info("点击提交，成功获取到node_id")
    except Exception as e:
        logger.error("点击按钮错误，获取node_id失败, 错误信息如下", e)
        return
    return node_id


# 得到上次提交的formJson 模板信息
def get_formJson_template(session, username):
    s = session
    query_url = 'http://s.cdut.edu.cn/EIP//queryservice/query.htm?'
    query_param = {
        'snumber': 'JK',
        'xh': username,
        '_': int(time.time() * 1000)
    }
    response_query = s.get(query_url, params=urlencode(query_param))
    formJson_template = json.loads(response_query.text)[0]
    return formJson_template


login_url = 'https://authserver.cdut.edu.cn/authserver/login?service=https%3A%2F%2Fehall.cdut.edu.cn%3A443%2Flogin%3Fservice%3Dhttps%3A%2F%2Fehall.cdut.edu.cn%2Fnew%2Findex.html'
login_headers = {
    'Content-Type': "application/x-www-form-urlencoded",
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    'Accept-Encoding': 'gzip,deflate',
    'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36 Edg/85.0.564.51",
    'Connection': 'keep-alive'
}


def main():
    with requests.Session() as s:
        response = s.get(login_url, headers=login_headers)
        username = item["username"]
        password = item["pwd"]
        login(s, response, username, password, login_url, login_headers)
        send_click_health(s)
        login_health_main_page(s)
        name = test_login(s)
        uuid = get_uuid(s)

        node_headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'Accept': "text/html, */*; q=0.01",
            'Accept-Encoding': 'gzip,deflate',
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36 Edg/85.0.564.51",
            'Connection': 'keep-alive',
            'Referer': 'http://s.cdut.edu.cn/EIP/cooperative/openCooperative.htm?flowId=4af305b2702997ca017029f040db0002'
        }
        node_id = get_node_id(s, node_headers)
        if not name or not uuid or not node_id:
            return
        flowForm_url = 'http://s.cdut.edu.cn/EIP/flow/flowForm/07092d757f8c4d81a6858875a50b780d.htm?'
        flowForm_param = {
            '_t': int(random.random() * 1000000),
            '_winid': 'w' + str(int(random.random() * 100000))
        }
        s.get(flowForm_url, params=urlencode(flowForm_param))
        formJson_template = get_formJson_template(s, username)
        formJson_changed = formatter_json(formJson, formJson_template)
        flowJson['id'] = node_id
        flowJson['name'] = username  # 学号
        flowJson['title'] = name  # 姓名
        instJson['uniqueIdentify'] = uuid[1:-1]
        send_payload = {
                            'taskTypeId': '',
                            'instJson': instJson,  # 固定值
                            'formJson': [formJson_changed],  #
                            'flowJson': [flowJson],
                            'defaultFormContent': '',
                            'annexJson': [],
                            'makeCopeJson': '',
                            'auditJson': [],
                            'flowVerJson': flowVerJson,
                            'formVerJson': formVerJson,
                            'flowId': flowId,
                            'starterFormId': formId,
                            'px': '',
                            'py': '',
        }
        send_url = 'http://s.cdut.edu.cn/EIP/cooperative/sendCooperative.htm'
        response = s.post(send_url, headers=node_headers, data=urlencode(send_payload))
        return json.loads(response.text)


if __name__ == '__main__':
    with open('{}/config.json'.format(cur_path), 'r+', encoding='utf-8') as f:
        config_list = json.load(f)
    for item in config_list:
        if item:
            count = 1
            while count <= 3:
                print("当前进行第%d次尝试打卡，共3次" % count)
                results = main()
                if results["code"] == '200':
                    print("学号: {} 打卡成功".format(item["username"]))
                    break
                print("打卡失败，正在重试")
                logger("失败返回状态码为{}, 原因是{}".format(results["code"], results["desc"]))
            if count > 3:
                if item["messageType"] == 1:
                    CdutEmail.sendEmail(item["email"])
                else:
                    ft.sendft(item["SCKEY"])
                print("方糖或者邮箱提醒")