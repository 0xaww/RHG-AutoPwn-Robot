#coding=utf-8
import requests
from requests.auth import HTTPBasicAuth
import base64
import json
import time
import sys
from competion import *


def submit_payload(payload,id,round,username,password,url_submit_flag):
    try:
        template = {"RoundID":round,
            "Payload":{
            "ChallengeID":id,
            "Crash":payload}}
        submit_data = {"username": username, "password": password, "verify": template}
        temstr = json.dumps(submit_data)
        headers = {'User-Agent': 'Mozilla/5.0'}

        ret = requests.post(url_submit_flag, json = submit_data, headers=headers,timeout = 30)
        print ret.json()
        return ret.json()['error_code']
    except Exception as e:
        print(str(e))
        return 1

    # 125 重复提交



def submit_test():
    username = "AWW"
    password = "102928wujiang"
    url_get_machines = "https://anquan.baidu.com/bctf/get_machines_info"
    url_get_question = "https://anquan.baidu.com/bctf/latest_round"
    url_submit_flag   = "https://anquan.baidu.com/bctf/submit"
    detect_time = 10 #比赛开始检测时间
    round_time = 60 #每轮时间

    r = robot(username,password,url_get_machines,url_get_question,url_submit_flag)
    r.get_question()
    #
    round = r.round
    print "round:",round

    for id in r.challenge:
        if id["cb_id"]=="baffa440":
            print id["cb_id"]
            # crashes = ['attachments/061837cd/out/crashes/id:000001,sig:11,src:000000,op:arith8,pos:25,val:-9', 'attachments/061837cd/out/crashes/id:000000,sig:11,src:000000,op:arith8,pos:21,val:-9']
            # for crash in crashes:
            #     file = open(crash,"rb").read()
            #     encodeStr = base64.b64encode(file)
            #     print encodeStr
            #     print id["cb_id"]
            #     print round
            #     print username
            #     print password
            #     print url_submit_flag
            encodeStr = "YXNkZmFzbGRqZmFsa3NkZmFzZGZhc2Rhc2RmYXNsZGpmYWxrc2RmYXNkZmFzZGFzZGZhc2xkamZhbGtzZGZhc2RmYXNkYXNkZmFzbGRqZmFsa3NkZmFzZGZhc2Rhc2RmYXNsZGpmYWxrc2RmYXNkZmFzZGFzZGZhc2xkamZhbGtzZGZhc2RmYXNkYXNkZmFzbGRqZmFsa3NkZmFzZGZhc2Rhc2RmYXNsZGpmYWxrc2RmYXNkZmFzZGFzZGZhc2xkamZhbGtzZGZhc2RmYXNkYXNkZmFzbGRqZmFsa3NkZmFzZGZhc2Rhc2RmYXNsZGpmYWxrc2RmYXNkZmFzZGFzZGZhc2xkamZhbGtzZGZhc2RmYXNkYXNkZmFzbGRqZmFsa3NkZmFzZGZhc2Rhc2RmYXNsZGpmYWxrc2RmYXNkZmFzZGFzZGZhc2xkamZhbGtzZGZhc2RmYXNkYXNkZmFzbGRqZmFsa3NkZmFzZGZhc2Rhc2RmYXNsZGpmYWxrc2RmYXNkZmFzZGFzZGZhc2xkamZhbGtzZGZhc2RmYXNkYXNkZmFzbGRqZmFsa3NkZmFzZGZhc2Rhc2RmYXNsZGpmYWxrc2RmYXNkZmFzZGFzZGZhc2xkamZhbGtzZGZhc2RmYXNkYXNkZmFzbGRqZmFsa3NkZmFzZGZhc2Rhc2RmYXNsZGpmYWxrc2RmYXNkZmFzZGFzZGZhc2xkamZhbGtzZGZhc2RmYXNkYXNkZmFzbGRqZmFsa3NkZmFzZGZhc2Rhc2RmYXNsZGpmYWxrc2RmYXNkZmFzZGFzZGZhc2xkamZhbGtzZGZhc2RmYXNkYXNkZmFzbGRqZmFsa3NkZmFzZGZhc2Rhc2RmYXNsZGpmYWxrc2RmYXNkZmFzZGFzZGZhc2xkamZhbGtzZGZhc2RmYXNkCg=="
            submit(encodeStr,id["cb_id"],round,username,password,url_submit_flag)


if __name__ == '__main__':
    submit_test()
