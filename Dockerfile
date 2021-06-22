FROM ubuntu:16.04

RUN sed -i "s/http:\/\/archive.ubuntu.com/http:\/\/mirrors.tuna.tsinghua.edu.cn/g" /etc/apt/sources.list
RUN sed -i "s/http:\/\/security.ubuntu.com/http:\/\/mirrors.tuna.tsinghua.edu.cn/g" /etc/apt/sources.list

RUN apt-get update && apt-get -y dist-upgrade
RUN apt-get install -y lib32z1 xinetd
RUN apt-get install -y openssh-server vim zsh git curl wget screen

RUN apt-get install -y python python-dev python-pip python-numpy
RUN apt-get install -y libtool libtool-bin automake bison libglib2.0-dev

#更改pip源
RUN mkdir /root/.pip
RUN echo "[global]\nindex-url = https://pypi.tuna.tsinghua.edu.cn/simple\n[install]\ntrusted-host=mirrors.aliyun.com" > /root/.pip/pip.conf

RUN pip install requests numpy

# oh-my-zsh
RUN sh -c "$(curl -fsSL https://gitee.com/awwwj/zsh/raw/master/install.sh)"

# 指定文件夹
WORKDIR /home/ctf

# 写入配置文件
RUN mkdir /home/ctf/robot
COPY ./robot /home/ctf/robot
COPY ./start.sh /

# 配置afl-fuzz
RUN chmod 755 /home/ctf/robot/afl-fuzz/setup_x32.sh
WORKDIR /home/ctf/robot/afl-fuzz
RUN sh -v -c /home/ctf/robot/afl-fuzz/setup_x32.sh


# 给start.sh可执行权限
RUN chmod 755 /start.sh
WORKDIR /home/ctf/robot/

#启动docker
CMD ["/start.sh"]
