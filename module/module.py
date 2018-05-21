#!/usr/bin/python

# -*- coding: utf-8 -*-

# Copyright (C) 2009-2012:
#    Gabes Jean, naparuba@gmail.com
#    Gerhard Lausser, Gerhard.Lausser@consol.de
#    Gregory Starck, g.starck@gmail.com
#    Hartmut Goebel, h.goebel@goebel-consult.de
#
# This file is part of Shinken.
#
# Shinken is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Shinken is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Shinken.  If not, see <http://www.gnu.org/licenses/>.


from shinken.basemodule import BaseModule
from shinken.log import logger

properties = {
    'daemons': ['arbiter'],
    'type': 'poller_tag_address_as_macro',
    'external': False,
    'phases': ['late_configuration'],
    }


# called by the plugin manager to get a broker
def get_instance(plugin):
    logger.info("[Poller tag address as macro] Get a "
                "<Poller tag address as macro> module for plugin {}".
                format(plugin.get_name()))
    instance = PollerTagAddress(plugin)
    return instance


# Just print some stuff
class PollerTagAddress(BaseModule):
    def __init__(self, mod_conf):
        BaseModule.__init__(self, mod_conf)
        self.host_macro_name = mod_conf.host_macro_name

    # Called by Arbiter to say 'let's prepare yourself guy'
    def init(self):
        logger.info("[Poller tag address as macro] Initialization of the "
                    "<Poller tag address as macro> module")

    def __set_poller_address_macro(self, host, poller_conf):
        poller_name = poller_conf.poller_name
        poller_address = poller_conf.arb_satmap["address"]

        logger.info("[Poller tag address as macro] Adding _poller_tag_address"
                    " macro to host: {}".format(host.host_name))
        logger.info("    poller_name = {}".format(poller_name))
        logger.info("    poller_address = {}".format(poller_address))

        host.customs[self.host_macro_name.upper()] = poller_address

    def hook_late_configuration(self, arb):
        logger.info("[Poller tag address as macro] in hook late config")

        for poller_conf in arb.conf.pollers:
            logger.debug("[Poller tag address as macro] poller detected: "
                         "poller_name={}, address={}, tags={}".format(
                            poller_conf.poller_name,
                            poller_conf.arb_satmap["address"],
                            poller_conf.poller_tags))

        for h in arb.conf.hosts:

            set_poller_macro = (
                h.poller_tag != "None" and
                self.host_macro_name and
                self.host_macro_name.upper() not in h.customs
            )

            if set_poller_macro:
                for poller_conf in arb.conf.pollers:
                    for tag in poller_conf.poller_tags:
                        if h.poller_tag != "None" and h.poller_tag == tag:
                            self.__set_poller_address_macro(h, poller_conf)
