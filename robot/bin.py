#coding=utf-8
from multiprocessing import Process
import subprocess
import os
from time import sleep
import fuzz_afl
from sub_answer import submit_payload
import base64

class bin(object):

    def __init__(self, id, round, ip, port, download_url, submit_url, question_type, flag_path,username,password,url_submit_flag):
        super(bin, self).__init__()
        self.id = id
        self.round = round
        self.ip = ip
        self.port = port
        self.download_url = download_url
        self.submit_url = submit_url
        self.question_type = question_type
        self.flag_path = flag_path
        self.submited = 0
        self.time_limit = 300 #second
        self.bin_dir = ""
        self.crashes = []
        self.new_crashes = []
        self.username = username
        self.password = password
        self.url_submit_flag = url_submit_flag
        self.submited_data = ""
    def log(self,content):
        try:
            f = open("log.txt","a")
            f.write(content+"\n")
            f.close
        except Exception as e:
            return 0

    def get_pid(self,pid_name):
        try:
            p = subprocess.Popen(["ps -ef | grep -v 'grep'  | grep '"+pid_name+"' |  awk '{print $2}' "], shell=True,close_fds = True,stdout=subprocess.PIPE)
            list = p.stdout.readlines()
            if len(list) != 0:
                return True
            else:
                return False
        except Exception as e:
            return False


    def download(self):
        try:
            self.dir = "attachments/"+str(self.id)
            self.bin_dir = self.dir+"/cb"
            self.bin_in = self.dir+"/in"
            self.bin_out = self.dir+"/out"
            self.submited_data = self.dir+"/submited.txt"
            file_addr = self.dir +"/"+ str(self.id)

            # 先检测本地是否已经下载
            if not os.path.isfile(self.bin_dir):
                os.system("mkdir "+self.dir )
                os.system("wget {url} -O {dir} --no-check-certificate --timeout=10 --tries=3".format(url = self.download_url,dir = file_addr ))
                os.system("tar xvf {file_addr} -C  {dir}/ --strip-components=1".format(file_addr = file_addr,dir = self.dir ))
            if not os.path.isfile(self.bin_dir):
                os.system("cp "+ self.dir+"/bin/cb " + self.bin_dir)

            if not os.path.isdir(self.bin_out):
                os.system("mkdir "+ self.bin_out)

            if not os.path.isfile(self.submited_data):
                os.system("touch "+ self.submited_data)

            if not os.path.isdir(self.bin_in):
                os.system("cp -r "+ self.dir+"/seed " + self.bin_in)
                #拷贝以前的seed
                os.system("cp ./seed/* "+self.bin_in)
            #可能还需要解压功能
            if os.path.isfile(self.bin_dir):
                self.log(self.dir + " download ok")
                return True
            else:
                self.log(self.dir + " download failed")
                return False

        except Exception as e:
            self.log(self.dir + " download failed")
            return False


    def fuzz(self):
        try:
            if not self.get_pid(self.id):
                self.log(self.dir + " start fuzz")
                print(self.bin_dir,self.bin_in,self.bin_out)
                fuzz_afl.main(self.id,self.bin_dir)
            else:
                self.log(self.dir + " is fuzzing in backend")
        except Exception as e:
            print(str(e))


    def exploit(self):
        # exploit为核心调用，传入题目信息，返回flag
        print("exploit")
        self.flag = "flag"

    def get_crashes(self):
        try:
            if not os.path.exists(self.bin_out+ "/" +"crashes"):
                return []
            crashes=[]
            for crashes_dir in os.listdir(self.bin_out):
                if crashes_dir.find("crashes") != -1:
                    for crash in os.listdir(self.bin_out+ "/" +crashes_dir):
                        if crash != 'README.txt':
                            crashes.append(self.bin_out+ "/" +crashes_dir+ "/" +crash)
            # 保存新的crashes，用于提交
            if crashes != self.crashes:
                last_crashes = self.crashes
                self.crashes = crashes
                for crash in last_crashes:
                    crashes.remove(crash)
                self.new_crashes = crashes
            else:
                self.new_crashes = []
        except Exception as e:
            print(str(e))


    def submit(self):
        try:
            self.get_crashes()
            if self.new_crashes != []:
                self.log(self.dir + " get new crashes")
                print(self.new_crashes)
                self.log(self.dir + " start submit")
                # 倒序先提交新的
                f_submited = open(self.submited_data,"r")
                submited_data = f_submited.read().split("\n")
                f_submited.close()
                for crash in reversed(self.new_crashes):
                    file = open(crash,"rb").read()
                    payload = base64.b64encode(file)
                    if payload in submited_data:
                        print("check has submited data")
                        continue
                    # print(payload,self.id,self.round,self.username,self.password,self.url_submit_flag)
                    error_code = submit_payload(payload,self.id,self.round,self.username,self.password,self.url_submit_flag)
                    if error_code==125 or error_code == 0:
                        f = open(self.submited_data,"a")
                        f.write(payload+"\n")
                        f.close()
                        print("wocao,youchongful")
                    print(error_code)
                    sleep(30)
                self.log(self.dir + " submit success")
        except Exception as e:
            print(str(e))




    def attack(self):
        self.download()
        self.fuzz()
        for i in range(0,300/5):
            self.submit()
            sleep(5)


    def timeout(self):
        for i in range(self.time_limit):
            # print("wait timeout " + str(i))
            sleep(1)
        self.p.terminate()
        print("sorrry, timeout")

    def auto(self):
        # k process用于超时检测
        # 因为BCTF一直运行fuzz,所以取消超时
        self.p = Process(target=self.attack) #, args=(str(i),))
        # self.k = Process(target=self.timeout)
        self.p.start()
        # self.k.start()
