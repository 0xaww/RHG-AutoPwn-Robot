#coding=utf-8
# from heartbeat import heartbeat
# from get_ranking import get_ranking
# from sub_answer import sub_answer
# from reset_question import reset_question
# from get_machines_info import get_machines_info
# from download import download
# from init import init

from bin import *
from competion import *
from time import sleep

username = "AWW"
password = "102928wujiang"
url_get_machines = "https://anquan.baidu.com/bctf/get_machines_info"
url_get_question = "https://anquan.baidu.com/bctf/latest_round"
url_submit_flag   = "https://anquan.baidu.com/bctf/submit"
detect_time = 10 #比赛开始检测时间
round_time = 300 #每轮时间


r = robot(username,password,url_get_machines,url_get_question,url_submit_flag)
while 1:#检测比赛是否开始
    try:
        r.get_question()
        if r.challenge != {} : #没开始或接受错误回0
            break
        else:
            print("waiting game start")
            sleep(detect_time)
    except Exception as e:
        print(str(e))


while 1:#循环进行进行fuzz测试
    try:
        if r.get_question() != True:
            print("game breaking ,waiting restart")
            sleep(detect_time)
            continue
        for cha in r.challenge:
            # cha = r.challenge[1]
            # if cha["cb_id"]!="061837cd":
            #     continue
            b1 = bin(id = cha["cb_id"], round =r.round, ip = "none", port = "none", download_url = cha["cb_url"], submit_url = r.url_submit_flag, question_type = cha["score_method"], flag_path = "none",username = username,password = password, url_submit_flag = url_submit_flag)
            # b1进行并发，详细功能
            b1.auto()
            # break
        sleep(round_time)
    except Exception as e:
        print(str(e))
