#!/usr/bin/env python
""" Attempting to generate a custom RYU controller for the purpose of completing this MSc project
Using the link below and external resources I am trying to create a controller that will be able to 
handle mininet traffic flowing through the Ubuntu terminal

The top line makes it possible to run the file as a script invoking the interpreter implicitly.
"""
#https://ryu.readthedocs.io/en/latest/writing_ryu_app.html
# Theses are imports from ~./local/lib/python3.10/site-packages/ryu and then the necessary things
# https://github.com/pymedusa/Medusa/issues/10253
import collections
try:
    from collections import abc
    collections.MutableMapping = abc.MutableMapping
except:
    pass

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, CONFIG_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_5
from ryu.lib.packet import packet, ethernet, ether_types, in_proto, ipv4, icmp, tcp, udp


__author__ = "Alex Jones"
__maintainer__ = "Alex Jones"
__email__ = "ajwilt97@gmail.com"
__status__ = "Production"


class RyuController(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_5.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(RyuController, self).__init__(*args,**kwargs)
        self.mac_to_port = {}
        print("made it to the initialisation")


    # Decorated event handler effectively, see docs above, openflow protocol api and then the related messages and structures version
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self,ev):
        msg = ev.msg

        self.logger.debug(
            'OFPSwitchFeatures received: '
            'datapath_id=0x%016x n_buffers=%d '
            'n_tables=%d auxiliary_id=%d '
            'capabilities=0x%08x',
            msg.datapath_id, msg.n_buffers, msg._tables, msg.auxiliary_id, msg.capabilities
        )
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,ofproto.OFPCL_NO_BUFFER)]
        self.send_flow_mod(datapath, 0, match, actions)

    # adding a new flow to the switch, effectively just a rule
    #   the priority is the packet matching the highest and then using the action to be dealt with
    #   match is setting of the condition
    # https://ryu.readthedocs.io/en/latest/ofproto_v1_5_ref.html?highlight=OFPFlowMod#ryu.ofproto.ofproto_v1_5_parser.OFPFlowMod 

    def send_flow_mod(self, datapath, priority, match, actions, buffer_id=None, idle=0, hard=0):
        ofp = datapath.ofproto
        ofp_parser = datapath.ofproto_parser

        inst = [ofp_parser.OFPInstructionActions(ofp.OFPIT_APPLY_ACTIONS, actions)]

        if buffer_id:
            flow_mod = ofp_parser.OFPFlowMod(
                datapath=datapath, 
                buffer_id=buffer_id,
                idle_timeout = idle,
                hard_timeout = hard,
                priority = priority,
                match = match,
                instructions = inst
            )
        else:
            flow_mod = ofp_parser.OFPFlowMod(
                datapath=datapath, 
                idle_timeout = idle,
                hard_timeout = hard,
                priority = priority,
                match = match,
                instructions = inst
            )
        datapath.send_msg(flow_mod)

    # send packet out not necessary right now


    # Event handler for packet sent to the controller from the switch
    #   dp: datapath
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self,ev):
        msg = ev.msg
        dp = msg.datapath
        ofp = dp.ofproto
        ofp_parser = dp.ofproto_parser

        # get received port num from packet_in msg
        in_port = msg.match['in_port']

        # Analyse packets received wth packet lib
        pkt = packet.Packet(msg.data)
        eth_pkt = pkt.get_protocols(ethernet.ethernet)[0]
        dst = eth_pkt.dst
        src = eth_pkt.src

        if eth_pkt.ethertype == ether_types.ETH_TYPE_LLDP:
            #ignore this packet
            return
        
        # get DatapathID to identify the switches in OpenFlow
        dpid = dp.id
        self.mac_to_port.setdefault(dpid,{})

        self.logger.info("Packet in %s %s %s %s", dpid, src, dst, in_port)
        
        # Learn particular MAC address to avoid attack next time
        self.mac_to_port[dpid][src] = in_port

        # if destination mac address is learned
        # decide which port to output packet, otherwise FLOOD all ports

        if dst not in self.mac_to_port[dpid]:
            out_port = ofp.OFPP_FLOOD
        else:
            out_port = self.mac_to_port[dpid][dst]

        # OFPctionOutput used with packet_out message to specify switch port you want to send packet from
        #   Uses OFPP_FLOOD flag to indicate packet should be sent on all ports
        # construct actions list
        actions = [ofp_parser.OFPActionOutput(out_port)]

        # install flow to avoid packet_in
        if out_port != ofp.OFPP_FLOOD:
            
            # check the IP Protocol and create IP match
            if eth_pkt.ethertype == ether_types.ETH_TYPE_IP:
                ip = pkt.get_protocol(ipv4.ipv4)
                src_ip = ip.src
                dst_ip = ip.dst
                protocol = ip.protocol

                # IP TCP Protocol
                if protocol == in_proto.IPPROTO_TCP:
                    return

                # IP UDP Protocol
                elif protocol == in_proto.IPPROTO_UDP:
                    return
                
                # IP ICMP Protocol
                elif protocol == in_proto.IPPROTO_ICMP:
                    return


            match = ofp_parser.OFPMatch(in_port=in_port, eth_dst=dst)
            self.send_flow_mod(dp, 1, match, actions)

        # construct packet_out msg and send
        out = ofp_parser.OFPPacketOut(
            datapath = dp,
            buffer_id = ofp.OFP_NO_BUFFER,
            in_port = in_port,
            actions = actions,
            data = msg.data
        )


        dp.send_msg(out)

def main():
    RC = RyuController()
    RC.__init__()

if __name__ == "__main__":
    main()