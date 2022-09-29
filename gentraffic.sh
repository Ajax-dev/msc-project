#!/bin/bash

# Simulate normal traffic
while true;
do
    packets=$(shuf -i 10-30 -n 1)
    bytes=$(shuf -i 128-256 -n 1)
    delay=$(shuf -i 1-5 -n 1)
    # dst=$(shuf -i 1-10 -n 1) # for tree
    dst=$(shuf -i 1-4 -n 1) # for others
    sudo hping3 -c $packets -d $bytes -s 80 -k 10.0.0.${dst}
    # sudo hping3 -c $packets -d $bytes -s 80 -k 10.0.0.10
    sleep $delay
done