#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Slixmpp: The Slick XMPP Library
    Copyright (C) 2010  Nathanael C. Fritz
    This file is part of Slixmpp.

    See the file LICENSE for copying permission.
"""

import logging
from config import *
from argparse import ArgumentParser

import slixmpp
import sys

def say_handler(bot,msg,cmd):
    param = msg['body'][len(cmd):]
    bot.send_message(mto=msg['from'].bare,
                              mbody=param.lstrip(),
                              mtype='groupchat')

def exec_handler(bot,msg,cmd):
    param = msg['body'][len(cmd):]
    exec(param.lstrip())

def exit_handler(bot,msg,cmd):
    sys.exit()

class MUCBot(slixmpp.ClientXMPP):
    """
    A simple Slixmpp bot that will greets those
    who enter the room, and acknowledge any messages
    that mentions the bot's nickname.
    """

    def __init__(self, jid, password, room, nick):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.commands = {}
        self.room = room
        self.nick = nick

        # The session_start event will be triggered when
        # the bot establishes its connection with the server
        # and the XML streams are ready for use. We want to
        # listen for this event so that we we can initialize
        # our roster.
        self.add_event_handler("session_start", self.start)

        # The groupchat_message event is triggered whenever a message
        # stanza is received from any chat room. If you also also
        # register a handler for the 'message' event, MUC messages
        # will be processed by both handlers.
        self.add_event_handler("groupchat_message", self.muc_message)

        # The groupchat_presence event is triggered whenever a
        # presence stanza is received from any chat room, including
        # any presences you send yourself. To limit event handling
        # to a single room, use the events muc::room@server::presence,
        # muc::room@server::got_online, or muc::room@server::got_offline.
        # self.add_event_handler("muc::%s::got_online" % self.room,
        #                       self.muc_online)

    def start(self, event):
        """
        Process the session_start event.

        Typical actions for the session_start event are
        requesting the roster and broadcasting an initial
        presence stanza.

        Arguments:
            event -- An empty dictionary. The session_start
                     event does not provide any additional
                     data.
        """
        self.get_roster()
        self.send_presence()
        self.plugin['xep_0045'].joinMUC(self.room,
                                        self.nick,
                                        password=ROOM_PWD,
                                        wait=True)

    def hasCommand(self, msg, cmd):
        if msg['body'].startswith(self.nick + ': '):
            print(msg['body'] + '2' + msg['mucnick'])
            msg['body']=msg['body'].replace(self.nick + ': ', '', 1)
            print(msg['body'] + '3')
        return msg['body'].startswith(cmd)

    def muc_message(self, msg):
        # Ignore self messages
        if msg['mucnick'] == self.nick: return

        # Plugin commands handler
        for cmd in self.commands:
            if self.hasCommand(msg, cmd):
                self.commands[cmd](self,msg,cmd)

        if self.nick in msg['body']:
            self.send_message(mto=msg['from'].bare,
                              mbody="%s: Што!?" % msg['mucnick'],
                              mtype='groupchat')


    def muc_online(self, presence):
        """
        Process a presence stanza from a chat room. In this case,
        presences from users that have just come online are
        handled by sending a welcome message that includes
        the user's nickname and role in the room.

        Arguments:
            presence -- The received presence stanza. See the
                        documentation for the Presence stanza
                        to see how else it may be used.
        """
        if presence['muc']['nick'] != self.nick:
            self.send_message(mto=presence['from'].bare,
                              mbody="Hello, %s %s" % (presence['muc']['role'],
                                                      presence['muc']['nick']),
                              mtype='groupchat')

    def register_cmd_handler(self,handler,cmd):
        self.commands[cmd]=handler

def main():
    # Setup the hasCommand line arguments.
    parser = ArgumentParser()

    # Output verbosity options.
    parser.add_argument("-q", "--quiet", help="set logging to ERROR",
                        action="store_const", dest="loglevel",
                        const=logging.ERROR, default=logging.INFO)
    parser.add_argument("-d", "--debug", help="set logging to DEBUG",
                        action="store_const", dest="loglevel",
                        const=logging.DEBUG, default=logging.INFO)

    args = parser.parse_args()

    # Setup logging.
    logging.basicConfig(level=args.loglevel,
                        format='%(levelname)-8s %(message)s')

    # Setup the MUCBot and register plugins. Note that while plugins may
    # have interdependencies, the order in which you register them does
    # not matter.
    xmpp = MUCBot(JID, PASSWORD, ROOM, NICK)
    xmpp.register_plugin('xep_0030')  # Service Discovery
    xmpp.register_plugin('xep_0045')  # Multi-User Chat
    xmpp.register_plugin('xep_0199')  # XMPP Ping

    xmpp.register_cmd_handler(say_handler,'.say')
    xmpp.register_cmd_handler(exec_handler, '.exec')
    xmpp.register_cmd_handler(exit_handler, '.exit')
    # Connect to the XMPP server and start processing XMPP stanzas.
    xmpp.connect()
    xmpp.process()


if __name__ == '__main__':
    main()
