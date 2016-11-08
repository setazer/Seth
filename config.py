import logging
defaults = './config.defaults'


def parse(conf):
    cfg = open(conf, 'r', encoding='utf-8').read()
    exec(cfg, globals())


def init(conf):
    try:
        parse(defaults)
    except:
        logging.log(logging.FATAL,"Can't parse config.defaults: <%s>\n" % (defaults,))
        raise
    try:
        parse(conf)
    except:
        logging.log(logging.FATAL,"Can't parse configuration file: <%s>\n" % (conf,))
        raise
