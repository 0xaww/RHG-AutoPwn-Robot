#coding=utf-8
import subprocess
import os
import stat
import signal
import re
import time
import config
import sys


class AFL(object):
    bin_addr = None
    bin_dir = None
    afl_dir = None
    afl_bin_addr = None
    afl_proc = None
    in_dir = None
    out_dir = None
    dic_dir = None

    __debug = False


    def __init__(self, id, binary, afl='/home/ctf/robot/afl-fuzz/afl-2.52b/afl-fuzz', debug=False):
        self.__id = id
        self.bin_addr = binary
        self.afl_bin_addr = afl
        self.afl_dir = os.path.dirname(afl)
        self.bin_dir = os.path.dirname(binary)
        self.in_dir = os.path.join(self.bin_dir, 'in')
        self.out_dir = os.path.join(self.bin_dir, 'out')
        self.dic_dir = os.path.join(self.bin_dir, 'dic')
        self.__debug = False


    def _generate_afl_dic(self):
        afl_dic_script = """#!/bin/bash

objdump -d "${1}" | grep -Eo '$0x[0-9a-f]+' | cut -c 2- | sort -u | while read const; do echo $const | python -c 'import sys,   struct; sys.stdout.write("".join(struct.pack("<I" if   len(l) <= 11 else "<Q", int(l,0)) for l in   sys.stdin.readlines()))' > ${2}/$const; done
i=0; strings "${1}"| while read line; do echo -n "$line" > ${2}/string_${i} ; i=$[ $i + 1 ] ; done
"""
        afl_dic_script_path = os.path.join(self.afl_dir, 'afl_dic.sh')
        if not os.path.exists(afl_dic_script_path):
            with open(afl_dic_script_path, 'w') as f:
                f.write(afl_dic_script)
        os.chmod(afl_dic_script_path, 0775)

        if not os.path.exists(self.dic_dir):
            os.mkdir(self.dic_dir)

        return subprocess.call([afl_dic_script_path, self.bin_addr, self.dic_dir])

    def start(self):
        self._generate_afl_dic()
        for f in os.listdir(self.dic_dir):
            filename = os.path.join(self.dic_dir, f)
            if os.stat(filename).st_size > 128:
                os.remove(filename)
        if not os.path.exists(self.in_dir):
            os.mkdir(self.in_dir)
            with open(os.path.join(self.in_dir, 'demo.txt'), 'w') as f:
                f.write('DEMO')
        if os.path.exists(self.out_dir+"/crashes"):
            self.in_dir = '-'

        os.chmod(self.bin_addr, 0775)

        if self.__debug:
            print "this function is debuging!"
            print self.afl_bin_addr, '-i', self.in_dir
            print "afl command:", self.afl_bin_addr, '-i', self.in_dir, '-o', self.out_dir, '-x', self.dic_dir, '-m none', '-Q', '--', self.bin_addr

            self.__afl_process = subprocess.Popen(
                [self.afl_bin_addr, '-i', self.in_dir, '-o', self.out_dir, '-x', self.dic_dir,
                 '-m', 'none', '-Q', '--', self.bin_addr])
        else:
            print("screen -dmS {id} bash -c '{afl_path} -i {input} -o {output} -x {dic} -m none -Q -- {bin}'".format(id=self.__id,afl_path=self.afl_bin_addr,input=self.in_dir,output=self.out_dir,dic=self.dic_dir,bin=self.bin_addr ))
            self.__afl_process = subprocess.Popen(["screen -dmS {id} bash -c '{afl_path} -i {input} -o {output} -x {dic} -m none -Q -- {bin}'".format(id=self.__id,afl_path=self.afl_bin_addr,input=self.in_dir,output=self.out_dir,dic=self.dic_dir,bin=self.bin_addr )],shell=True, stdout=subprocess.PIPE)


    def stop(self):
        self.__afl_process.kill()
        self.__afl_process.wait()

    def is_alive(self):
        return self.__afl_process.poll() is None




def main(id,file_name):
    try:
        afl_path = "/home/ctf/robot/afl-fuzz/afl-2.52b/afl-fuzz"
        start_time = time.time()
        max_run_time = 7200
        afl = AFL(id,file_name, afl=afl_path, debug=True )
        print "now fuzzing  ", file_name
        afl.start()
        while True:
            if time.time() - start_time >max_run_time:
                break
            time.sleep(10)
        self.__afl_process.kill()
    except Exception as e:
        print(str(e))
        print("fuzz failed")

if __name__ == '__main__':
    print(main(sys.argv[1]))
