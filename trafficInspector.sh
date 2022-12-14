#!/bin/bash
n=4 #number of switches for linear and basic and tree

red=`tput setaf 1` # setting colour variables
green=`tput setaf 2`
reset=`tput sgr0`
echo "Script running..."
for i in {1..1000}
do
    # start at 2 for tree
    for((j = 1; j <= n; j++))
    do
        echo "Inspection no $i at s$j"
        # extract data >> to append to the end of the file
        sudo ovs-ofctl dump-flows s$j > data/base
        grep "nw_src" data/base> data/entries.csv
        # awk '{print $0}' data/base.csv
        packets=$(awk -F "," '{split($4,a,"="); print a[2]","}' data/entries.csv)
        bytes=$(awk -F "," '{split($5,b,"="); print b[2]","}' data/entries.csv)
        ipsrc=$(awk -F "," '{out=""; for(k=2;k<=NF;k++){out=out" "$k}; print out}' data/entries.csv | awk -F " " '{split($11,d,"="); print d[2]","}')
        ipdst=$(awk -F "," '{out=""; for(k=2;k<=NF;k++){out=out" "$k}; print out}' data/entries.csv | awk -F " " '{split($12,d,"="); print d[2]","}')

        # check if there's no traffic currently
        if test -z "$packets" || test -z "$bytes" || test -z "$ipsrc" || test -z "$ipdst" 
        then
            echo "no traffic"
            state=0
        else
            #echo "${green}Traffic flowing...${reset}"
            echo "$packets" > data/packets.csv
            echo "$bytes" > data/bytes.csv
            echo "$ipsrc" > data/ipsrc.csv
            echo "$ipdst" > data/ipdst.csv

            # python3 traffic-monitor.py
            python3 computation.py
            python3 check-traffic.py
            state=$(awk '{print $0;}' .result)
        fi

        if [ $state -eq 1 ];
        then
            echo "${red}^^ATTACK ON THE NETWORK AT switch:$j^^${reset}"
            echo "-------------------------"
            # cat data/realtime.csv
            #
            default_flow=$(sudo ovs-ofctl dump-flows s$j | tail -n 1) #gets the flow "action:CONTROLLER:65535" (just the port num of yours basic) sending unknown packet
            sudo ovs-ofctl del-flows s$j
            sudo ovs-ofctl add-flow s$j "$default_flow"
        else
            echo "${green}^^Clean traffic^^${reset}"
            echo "-------------------------"
        fi
    done
    sleep 3
done
            