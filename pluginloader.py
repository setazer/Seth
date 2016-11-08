#!/usr/bin/env python
# -*- coding: utf8 -*-
# ~#######################################################################
# ~ Copyright (c) 2008 Burdakov Daniel <kreved@kreved.org>               #
# ~                                                                      #
# ~ This file is part of FreQ-bot.                                       #
# ~                                                                      #
# ~ FreQ-bot is free software: you can redistribute it and/or modify     #
# ~ it under the terms of the GNU General Public License as published by #
# ~ the Free Software Foundation, either version 3 of the License, or    #
# ~ (at your option) any later version.                                  #
# ~                                                                      #
# ~ FreQ-bot is distributed in the hope that it will be useful,          #
# ~ but WITHOUT ANY WARRANTY; without even the implied warranty of       #
# ~ MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the        #
# ~ GNU General Public License for more details.                         #
# ~                                                                      #
# ~ You should have received a copy of the GNU General Public License    #
# ~ along with FreQ-bot.  If not, see <http://www.gnu.org/licenses/>.    #
# ~#######################################################################

import os
import sys
import logging

class pluginloader:
    def __init__(self, bot):
        self.bot = bot
        self.env = bot.env
        self.plugin_dir = bot.config.PLUGINS_DIR
        self.sqlite = bot.config.ENABLE_SQLITE
        self.pluginlist = os.listdir(bot.config.PLUGINS_DIR)

    def load_all(self):
        logging.log(logging.INFO,'Loading Bot Plugins: ')
        for i in self.pluginlist:
            self.load(i)
        logging.log(logging.INFO,'Loading Complete')

    def load(self, p):

        tl = os.listdir(self.plugin_dir + '/' + p)
        tl = [i for i in tl if i.endswith('.py')]
        for i in tl:
            fn = '%s/%s/%s' % (self.plugin_dir, p, i)
            fp = open(fn, 'r', encoding='utf-8')
            pc = fp.read()
            fp.close()
            if self.sqlite or not pc.count('__NEED_DB__'):
                try:
                    exec(pc, self.env)
                except:
                    logging.log(logging.ERROR,"\nCan't load plugin %s:\n" % (fn,))
                    raise
                logging.log(logging.INFO,"Loaded Bot Plugin: {}/{}".format(p,i))
            else:
                # this plugin needs database, but it is disabled
                logging.log(logging.ERROR, "Cannot load {}/{}, due to disabled SQLite".format(p, i))
