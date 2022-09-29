# 963906 
## MSc in Human-Centred Artificial Intelligence Project
### Exploration and Analysis of DDoS attacks in 5G-based Software Defined Networks

Making use of several pieces of software, currently:
- Ubuntu (22.04) OS
- Microsoft Visual Studio Code
- Python 3.10.4 (may need to change to 3.9 due to issue with eventlet.wsgi 'ALREADY_HANDLED')
- Mininet

Datasets:
- First dataset taken from (dataset-small.csv): https://www.researchgate.net/publication/324716038_SOFTWARE-DEFINED_SECURITY 
- Second dataset taken from (dataset-large.csv): https://github.com/dz43developer/sdn-network-ddos-detection-using-machine-learning 


Some additional notes:
- Dependencies are saved in requirements.txt
- Made use of a venv in this project 

To Run:
Start your environment with the correct requirements as laid out
- Run all machine learning files
- `ryu-manager controller.py`
- New terminal window
- `sudo python3 <any-topology>.py`
- In the mininet line
- `xterm <hostname i.e. h2>` and in that window `source gentraffic.sh` for as many hosts as you want
- New terminal
- source trafficInspector.sh
- New xterm window
- `sudo hping3 --flood --rand-source 10.0.0.<host to attack i.e. 1, 5, 10>`
- You can change which model is used for detection in the `check-traffic.py` file
- To edit packet generation go into `genTraffic.sh`, for certain topologies you'll have to change the `dst` value if you don't have many hosts i.e. basic-topo has 4hosts but tree has 10hosts
