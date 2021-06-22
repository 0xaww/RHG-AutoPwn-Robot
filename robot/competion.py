#coding=utf-8
import requests
import base64
import json

class robot(object):
    def __init__(self, username,password,url_get_machines,url_get_question,url_submit_flag):
        super(robot, self).__init__()
        self.username = username
        self.password = password
        self.url_get_machines = url_get_machines
        self.url_get_question = url_get_question
        self.url_submit_flag = url_submit_flag
        self.challenge = {}
        self.round = 0
        self.local_env = False

    def get_question(self):
        try:
            if self.local_env == True:
                resp = open("local_info.txt","r").read()
                ret_con = json.loads(resp)
                self.challenge = ret_con['CurrentChallenge']
                self.round = ret_con['CurrentRound']
                return True
            elif self.local_env == False:
                header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)     Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'}
                resp = requests.get(self.url_get_question, headers=header, timeout=30, verify=False)
                ret_con = json.loads(resp.content)
                self.challenge = ret_con['CurrentChallenge']
                self.round = ret_con['CurrentRound']
                return True
        except Exception as e:
            print(str(e))
            return False

if __name__ == '__main__':
    r = robot("student01","VXAdUBmb","url_get_machines","https://anquan.baidu.com/bctf/latest_round"," https://anquan.baidu.com/bctf/submit")
    r.get_question()
    print(r.challenge)
    print(r.round)
