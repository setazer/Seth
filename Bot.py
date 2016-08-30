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


class MUCBot(slixmpp.ClientXMPP):
    """
    A simple Slixmpp bot that will greets those
    who enter the room, and acknowledge any messages
    that mentions the bot's nickname.
    """

    def __init__(self, jid, password, room, nick):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        msg_commands = []
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

    def muc_message(self, msg):
        """
        Process incoming message stanzas from any chat room. Be aware
        that if you also have any handlers for the 'message' event,
        message stanzas may be processed by both handlers, so check
        the 'type' attribute when using a 'message' event handler.

        Whenever the bot's nickname is mentioned, respond to
        the message.

        IMPORTANT: Always check that a message is not from yourself,
                   otherwise you will create an infinite loop responding
                   to your own messages.

        This handler will reply to messages that mention
        the bot's nickname.

        Arguments:
            msg -- The received message stanza. See the documentation
                   for stanza objects and the Message stanza to see
                   how it may be used.
        """
        if msg['mucnick'] == self.nick: return

        if self.nick in msg['body']:
            self.send_message(mto=msg['from'].bare,
                              mbody="%s:Што!?" % msg['mucnick'],
                              mtype='groupchat')
            print(msg)
        splitmsg = msg['body'].split(' ')
        firstword = splitmsg[0]
        otherwords = ' '.join(splitmsg[1:])
        '  asd '.strip()
        if msg['body'].startswith('!say'):
            self.send_message(mto=msg['from'].bare,
                              mbody=otherwords,
                              mtype='groupchat')
        if msg['body'].startswith('!jir'):
            self.send_message(mto=msg['from'].bare,
                              mbody=self.plugin['xep_0045'].getJidProperty(msg['from'].bare, otherwords, 'jid'),
                              mtype='groupchat')
        if msg['body'].startswith('!exec'):
            exec(otherwords)
        if msg['body'].startswith('!e'):
            try:
                res_msg=str(exec(otherwords))
            except Exception as e:
                res_msg='Error: ' + str(e)
            self.send_message(mto=msg['from'].bare,
                              mbody=res_msg,
                              mtype='groupchat')
        if msg['body'].startswith('!exit'):
            sys.exit()

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


def main():
    # Setup the command line arguments.
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

    # Connect to the XMPP server and start processing XMPP stanzas.
    xmpp.connect()
    xmpp.process()


if __name__ == '__main__':
    main()
