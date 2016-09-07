import logging
from seth import sethbot
import config
from argparse import ArgumentParser

# Setup the hasCommand line arguments.
parser = ArgumentParser()

# Output verbosity options.
parser.add_argument("-q", "--quiet", help="set logging to ERROR",
                    action="store_const", dest="loglevel",
                    const=logging.ERROR, default=logging.INFO)
parser.add_argument("-d", "--debug", help="set logging to DEBUG",
                    action="store_const", dest="loglevel",
                    const=logging.DEBUG, default=logging.INFO)

parser.add_argument('config', help ='path to config file', default='./seth.cfg')
args = parser.parse_args()

# Setup logging.
logging.basicConfig(format='%(levelname)-8s %(message)s',
                    level=args.loglevel)

# Setup the MUCBot and register plugins. Note that while plugins may
# have interdependencies, the order in which you register them does
# not matter.
config.init(args.config)
config.env=globals()
bot = sethbot(config)
bot.register_plugin('xep_0030')  # Service Discovery
bot.register_plugin('xep_0045')  # Multi-User Chat
bot.register_plugin('xep_0199')  # XMPP Ping
bot.plug.load_all()


# Connect to the XMPP server and start processing XMPP stanzas.
bot.connect()
bot.process()
