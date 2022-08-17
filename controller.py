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