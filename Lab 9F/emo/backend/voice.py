from aip import AipSpeech
APP_ID = '23474300'
API_KEY = 'sluLEi1xoOTdgC7hU570Pebl'
SECRET_KEY = 'YmQxWR9Cn5rex5LQbrwl8DGr3BbkMYTg'

vr = '/home/pi/1900012739/emo/assets/'  # voice root


def ttf():  # return the number of sentences.
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    content = []
    with open(vr+'calendar.txt', 'r', encoding='UTF-8') as f:
        line = f.read().strip()
        content = line.split('\n')
        print(content)

    from os import system
    l = len(content)
    for i in range(l):
        result = client.synthesis(content[i], 'zh', 1, {'spd': 4, 'per': 4})
        filename = vr + 'vol' + str(i+1) + '.wav'
        if not isinstance(result, dict):
            with open(filename, 'wb') as f:
                f.write(result)
                print(i+1, 'finished')
    return l

def ttf1(filename):
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    content = []
    with open(vr + 'temp.txt', 'r', encoding='UTF-8') as f:
        line = f.read().strip()
        content = line.split('\n')

    result = client.synthesis(content, 'zh', 1, {'spd': 4, 'per': 4})
    if not isinstance(result, dict):
        print("ttf yes")
        with open(filename, 'wb') as f:
            f.write(result)

import json
from urllib import request,parse

def get_token():
    API_Key = "ohkn8tH9GnFifw1ND0BRbE5W"            # 官网获取的API_Key
    Secret_Key = "7LLBMeEPcf8y9bs7Br5x7bUi6GGZPzNV" # 为官网获取的Secret_Key

    #拼接得到Url
    Url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id="+API_Key+"&client_secret="+Secret_Key
    try:
        resp = request.urlopen(Url)
        result = json.loads(resp.read().decode('utf-8'))
        # 打印access_token
        print("access_token:",result['access_token'])
        return result['access_token']
    except request.URLError as err:
        print('token http response http code : ' + str(err.code))

def speech_recog(filename):
    # 1、获取 access_token
    token = get_token()
    # 2、打开需要识别的语音文件
    speech_data = []
    filename = vr + "16k.wav"
    with open(filename, 'rb') as speech_file:
        speech_data = speech_file.read()
    length = len(speech_data)
    if length == 0:
        print('file', filename, 'length read 0 bytes')

    # 3、设置Url里的参数
    params = {'cuid': "tfhn44561745", # 用户唯一标识，用来区分用户，长度为60字符以内。
              'token': token,           # 我们获取到的 Access Token
              'dev_pid': 1537 }         # 1537 表示识别普通话
    # 将参数编码
    params_query = parse.urlencode(params)
    # 拼接成一个我们需要的完整的完整的url
    Url = 'http://vop.baidu.com/server_api' + "?" + params_query

    # 4、设置请求头
    headers = {
        'Content-Type': 'audio/wav; rate=16000',    # 采样率和文件格式
        'Content-Length': length
    }

    # 5、发送请求，音频数据直接放在body中
    # 构建Request对象
    req = request.Request(Url, speech_data, headers)
    # 发送请求
    res_f = request.urlopen(req)
    result = json.loads(res_f.read().decode('utf-8'))
    print(result)
    result = result['result']
    with open(vr + 'temp.txt', 'w', encoding='UTF-8') as f:
        f.write(result[0])
    ttf1(filename)
    
if __name__ == '__main__':
    ttf1(vr + 'test1.wav')