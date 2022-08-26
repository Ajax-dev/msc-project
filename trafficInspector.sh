#!/bin/bash
echo "Script running..."
n=4 #number of switches
for i in {1..200}
do
    for((j = 1; j <= n; j++))
    do
        echo "Inspection no $i at s$j"
        # extract data
        sudo ovs-ofctl dump-flows s$j > data/base
        grep "nw_src" data/base > data/entries.csv
        packets=$(awk -F "," '{split($4,a,"="); print a[2]","}' data/StatsFile.csv)
        bytes=$(awk -F "," '{split($5,b,"="); print b[2]","}' data/StatsFile.csv)
        ipsrc=$(awk -F "," '{out=""; for(k=2;k<=NF;k++){out=out" "$k}; print out}' data/StatsFile.csv | awk -F " " '{split($11,d,"="); print d[2]","}')
        ipdst=$(awk -F "," '{out=""; for(k=2;k<=NF;k++){out=out" "$k}; print out}' data/StatsFile.csv | awk -F " " '{split($12,d,"="); print d[2]","}')

        # check if there's no traffic currently
        if test -z "$packets" || test -z "$bytes" || test -z "$ipsrc" || test -z "$ipdst"
        then
            # echo "no traffic"
            state=0
        else
            echo "Some traffic"
            echo "$packets" > data/packets.csv
            echo "$bytes" > data/bytes.csv
            echo "$ipsrc" > data/ipsrc.csv
            echo "$ipdst" > data/ipdst.csv

            # python3 traffic-monitor.py
            # python3 computation.py
            # python3 check-traffic-svc.py
            state=$(awk '{print $0;}' .result)
        fi

        if [ $state -eq 1 ];
        then
            echo "ATTACK ON THE NETWORK AT switch$j"
            #
            default_flow = $(sudo ovs-ofctl dump-flows s$j | tail -n 1) 
            sudo ovs-ofctl add-flow s$j "$default_flow" 
            sudo ovs-ofctl del-flows s$j

        fi
    done
    sleep 3
done
            