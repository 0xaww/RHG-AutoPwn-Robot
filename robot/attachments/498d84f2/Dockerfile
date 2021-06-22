# sudo docker build -t bctf_test .
# sudo docker run -d --rm -it bctf_test

# use a 32-bit base image in case someone uses it on a 32-bit host
FROM i386/ubuntu:16.04

LABEL challenge="crash checksum" \
	  bin_arch="i386"

##### Docker Build Time CMD #######

#Should always RUN 'apt-get update && apt-get install -y ' together to avoid cache issue
#RUN apt-get update && \
#	apt-get install -y \
#			build-essential \
#			gcc gdb wget \
#			python

RUN useradd -d /home/bctf/ -m -p ctf -s /bin/bash bctf
RUN echo "bctf:bctf" | chpasswd

#COPY data/popcalc /bin/

WORKDIR /home/bctf

COPY bin/cb /home/bctf/
COPY seed/sample.in /home/bctf/

RUN chown -R bctf:bctf /home/bctf

USER bctf

####### Container Start Time CMD #######
#cmd to run once container starts
CMD ./cb - < sample.in > sample.out
