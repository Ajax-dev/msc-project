#!/usr/bin/env python
""" Attempting to generate a custom RYU controller for the purpose of completing this MSc project
Using the link below and external resources I am trying to create a controller that will be able to 
handle mininet traffic flowing through the Ubuntu terminal

The top line makes it possible to run the file as a script invoking the interpreter implicitly.
"""
#https://ryu.readthedocs.io/en/latest/writing_ryu_app.html
from ryu.base import app_manager # central management of Ryu apps
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, CONFIG_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ethernet, ether_types, in_proto, ipv4, icmp, tcp, udp


__author__ = "Alex Jones"
__maintainer__ = "Alex Jones"
__email__ = "ajwilt97@gmail.com"
__status__ = "Production"