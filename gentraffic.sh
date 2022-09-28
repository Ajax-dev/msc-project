#!/bin/bash

# Simulate normal traffic
while true;
do
    packets=$(shuf -i 10-20 -n 1)
    bytes=$(shuf -i 150-200 -n 1)
    delay=$(shuf -i 1-5 -n 1)
    sudo hping3 -c $packets -d $bytes -k 10.0.0.1
    sleep $delay
done