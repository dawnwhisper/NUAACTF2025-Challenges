#!/bin/sh
docker build -t pwn1 .

docker run -it --rm -p 12345:12345 -e FLAG="your_flag_here" pwn1