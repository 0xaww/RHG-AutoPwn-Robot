#!/bin/sh

tar xvf ./afl-latest.tgz;
cp ./qemu-2.10.0.tar.xz ./afl-2.52b/qemu_mode;
cp ./build_qemu_support.sh ./afl-2.52b/qemu_mode/;
cd ./afl-2.52b;
make;
make install;

cd ./qemu_mode;
tar xvf ./qemu-2.10.0.tar.xz ;
apt-get install libtool-bin automake -y
export CPU_TARGET=i386;
./build_qemu_support.sh;
